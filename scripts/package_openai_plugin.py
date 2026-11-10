"""Validate the OpenAI plugin package in openai-plugin/ and build its ZIP.

Checks, in order:
- plugin.json and mcp.json validate against the Agent Plugins schema each
  one declares in `$schema` (fetched over HTTPS);
- every relative asset path in plugin.json exists inside openai-plugin/;
- the MCP server URL is HTTPS;
- the review test cases are present (counted, not run: running them needs
  a reviewer account in ChatGPT, see OPENAI_PLUGIN_RELEASE.md).

Then it writes a deterministic ZIP with plugin.json, mcp.json and assets/
at the archive root, plus package-info.json (version, source commit,
SHA-256). Uploading the ZIP to the OpenAI portal stays manual.

    pip install jsonschema==4.26.0
    python3 scripts/package_openai_plugin.py --out dist [--base-ref origin/main]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "openai-plugin"
MANIFESTS = ("plugin.json", "mcp.json")
EXPECTED_CASES = {"positive": 5, "negative": 3}  # OPENAI_PLUGIN_RELEASE.md
ZIP_DATE = (1980, 1, 1, 0, 0, 0)


def fetch_schema(url: str) -> dict:
    if not url.startswith("https://"):
        raise ValueError(f"$schema must be an HTTPS URL, got {url!r}")
    request = Request(url, headers={"User-Agent": "flux-mcp-package-check"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def schema_errors(document: dict, schema: dict) -> list[str]:
    from jsonschema import Draft202012Validator

    validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
    return [
        f"{'/'.join(map(str, error.absolute_path)) or '(root)'}: {error.message}"
        for error in sorted(validator.iter_errors(document), key=lambda e: list(map(str, e.absolute_path)))
    ]


def relative_paths(node, found=None) -> list[str]:
    """Every string in the manifest that is a `./` relative path."""
    found = [] if found is None else found
    if isinstance(node, dict):
        for value in node.values():
            relative_paths(value, found)
    elif isinstance(node, list):
        for value in node:
            relative_paths(value, found)
    elif isinstance(node, str) and node.startswith("./"):
        found.append(node)
    return found


def asset_errors(plugin: dict, package: Path) -> list[str]:
    errors = []
    for reference in relative_paths(plugin):
        target = (package / reference).resolve()
        if package.resolve() not in target.parents:
            errors.append(f"{reference}: points outside openai-plugin/")
        elif not target.is_file():
            errors.append(f"{reference}: file not found")
    return errors


def server_errors(mcp: dict) -> list[str]:
    servers = mcp.get("mcpServers") or {}
    if not servers:
        return ["mcp.json: no mcpServers entry"]
    return [
        f"mcp.json: server {name!r} URL must be HTTPS without a trailing slash, got {server.get('url')!r}"
        for name, server in servers.items()
        if not str(server.get("url", "")).startswith("https://") or str(server.get("url")).endswith("/")
    ]


def review_warnings(plugin: dict) -> list[str]:
    cases = plugin.get("extensions", {}).get("com.openai", {}).get("review", {}).get("test_cases", {})
    return [
        f"{kind} review test cases: {len(cases.get(kind, []))}, release checklist expects {count}"
        for kind, count in EXPECTED_CASES.items()
        if len(cases.get(kind, [])) != count
    ]


def package_files(package: Path) -> list[Path]:
    files = [package / name for name in MANIFESTS]
    files += sorted(p for p in (package / "assets").rglob("*") if p.is_file() and not p.name.startswith("."))
    return files


def build_zip(package: Path, destination: Path) -> list[str]:
    """Deterministic: fixed order, timestamps and permissions."""
    names = []
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in package_files(package):
            name = path.relative_to(package).as_posix()
            info = zipfile.ZipInfo(name, date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
            names.append(name)
    return names


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def version_warning(plugin: dict, base_ref: str | None) -> str | None:
    """Package changes reach the portal only as a new upload; the version
    shown there is plugin.json's. Warn when the package changed but the
    version did not."""
    if not base_ref:
        return None
    try:
        changed = git("diff", "--name-only", f"{base_ref}...HEAD", "--", "openai-plugin")
        base = json.loads(git("show", f"{base_ref}:openai-plugin/plugin.json"))
    except (subprocess.CalledProcessError, ValueError):
        return None
    if changed and base.get("version") == plugin.get("version"):
        return f"openai-plugin/ changed but plugin.json version is still {plugin.get('version')}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--base-ref", help="Warn if openai-plugin/ changed since this ref without a version bump")
    args = parser.parse_args()

    documents = {name: json.loads((PACKAGE / name).read_text()) for name in MANIFESTS}
    errors = []
    for name, document in documents.items():
        errors += [f"{name}: {e}" for e in schema_errors(document, fetch_schema(document.get("$schema", "")))]
    errors += asset_errors(documents["plugin.json"], PACKAGE)
    errors += server_errors(documents["mcp.json"])
    warnings = review_warnings(documents["plugin.json"])
    if warning := version_warning(documents["plugin.json"], args.base_ref):
        warnings.append(warning)

    for warning in warnings:
        print(f"::warning::{warning}")
    for error in errors:
        print(f"::error::{error}")
    if errors:
        return 1

    version = documents["plugin.json"]["version"]
    commit = git("rev-parse", "HEAD")
    args.out.mkdir(parents=True, exist_ok=True)
    archive = args.out / f"flux-openai-plugin-{version}-{commit[:7]}.zip"
    names = build_zip(PACKAGE, archive)
    info = {
        "version": version,
        "source_commit": commit,
        "zip": archive.name,
        "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
        "files": names,
        "mcp_url": next(iter(documents["mcp.json"]["mcpServers"].values()))["url"],
        "manual_steps": [
            "Run the review test cases in ChatGPT with the reviewer account and record results.",
            "Upload this ZIP in the OpenAI portal (Metadata & Skills) and resolve findings.",
        ],
    }
    (args.out / "package-info.json").write_text(json.dumps(info, indent=2) + "\n")
    print(json.dumps(info, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
