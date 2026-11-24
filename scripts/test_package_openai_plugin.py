import os
import tempfile
import unittest
from pathlib import Path

from package_openai_plugin import asset_errors, mcp_submission_schema, package_files, schema_errors, server_errors


CORE_SCHEMA = {
    "$defs": {
        "streamableHttpServer": {
            "type": "object",
            "properties": {"type": {"const": "streamable-http"}, "url": {"type": "string"}},
            "required": ["type", "url"],
            "additionalProperties": False,
        }
    },
    "$ref": "#/$defs/streamableHttpServer",
}
DCR = {"com.openai": {"auth": {"type": "oauth", "client": {"mode": "dcr"}}}}


class SubmissionValidationTests(unittest.TestCase):
    def setUp(self):
        self.server = {"type": "streamable-http", "url": "https://mcp.bfl.ai/"}
        self.schema = mcp_submission_schema(CORE_SCHEMA)

    def test_approved_oauth_extension_is_valid(self):
        self.server["extensions"] = DCR
        self.assertEqual(schema_errors(self.server, self.schema), [])

    def test_generic_server_still_valid(self):
        self.assertEqual(schema_errors(self.server, self.schema), [])

    def test_does_not_modify_core_schema(self):
        self.assertNotIn("extensions", CORE_SCHEMA["$defs"]["streamableHttpServer"]["properties"])

    def test_unknown_fields_remain_invalid(self):
        self.server["urll"] = self.server["url"]
        self.assertTrue(schema_errors(self.server, self.schema))

    def test_unknown_extensions_and_auth_modes_remain_invalid(self):
        for extension in [{"unknown.vendor": {}}, {"com.openai": {"auth": {"type": "none"}}}]:
            with self.subTest(extension=extension):
                self.server["extensions"] = extension
                self.assertTrue(schema_errors(self.server, self.schema))

    def test_https_endpoint_with_or_without_slash(self):
        for url in ["https://mcp.bfl.ai/", "https://mcp.bfl.ai"]:
            self.assertEqual(server_errors({"mcpServers": {"bfl": {"url": url}}}), [])

    def test_http_endpoint_remains_invalid(self):
        self.assertTrue(server_errors({"mcpServers": {"bfl": {"url": "http://mcp.bfl.ai/"}}}))

    def test_https_scheme_is_case_insensitive(self):
        self.assertEqual(server_errors({"mcpServers": {"bfl": {"url": "HTTPS://mcp.bfl.ai"}}}), [])

    def test_https_endpoint_needs_a_host(self):
        for url in ["https://", "https:///mcp", "https://:443"]:
            with self.subTest(url=url):
                self.assertTrue(server_errors({"mcpServers": {"bfl": {"url": url}}}))

    def test_server_without_url_is_invalid(self):
        self.assertTrue(server_errors({"mcpServers": {"bfl": {}}}))


class PackageContentsTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.package = self.root / "openai-plugin"
        (self.package / "assets").mkdir(parents=True)
        (self.package / "plugin.json").write_text("{}")
        (self.package / "mcp.json").write_text("{}")
        (self.package / "assets" / "icon.png").write_bytes(b"png")

    def packaged(self):
        return [path.relative_to(self.package).as_posix() for path in package_files(self.package)]

    def test_manifests_and_assets_are_packaged(self):
        self.assertEqual(self.packaged(), ["plugin.json", "mcp.json", "assets/icon.png"])

    def test_hidden_files_and_directories_are_not_packaged(self):
        (self.package / "assets" / ".DS_Store").write_bytes(b"x")
        (self.package / "assets" / ".cache").mkdir()
        (self.package / "assets" / ".cache" / "token.txt").write_text("secret")
        self.assertEqual(self.packaged(), ["plugin.json", "mcp.json", "assets/icon.png"])

    def test_symlinked_asset_is_not_packaged(self):
        (self.root / "secret.txt").write_text("secret")
        try:
            os.symlink(self.root / "secret.txt", self.package / "assets" / "link.png")
        except (OSError, NotImplementedError):
            self.skipTest("symlinks are not available here")
        self.assertEqual(self.packaged(), ["plugin.json", "mcp.json", "assets/icon.png"])

    def test_packaged_asset_reference_is_valid(self):
        self.assertEqual(asset_errors({"logo": "./assets/icon.png"}, self.package), [])

    def test_missing_asset_is_reported(self):
        errors = asset_errors({"logo": "./assets/missing.png"}, self.package)
        self.assertEqual(errors, ["./assets/missing.png: file not found"])

    def test_parent_directory_reference_is_reported(self):
        (self.root / "secret.txt").write_text("secret")
        errors = asset_errors({"logo": "../secret.txt"}, self.package)
        self.assertEqual(errors, ["../secret.txt: points outside openai-plugin/"])

    def test_asset_the_zip_would_leave_out_is_reported(self):
        (self.package / "docs").mkdir()
        (self.package / "docs" / "icon.png").write_bytes(b"png")
        (self.package / "assets" / ".hidden.png").write_bytes(b"png")
        for reference in ["./docs/icon.png", "./assets/.hidden.png"]:
            with self.subTest(reference=reference):
                errors = asset_errors({"logo": reference}, self.package)
                self.assertEqual(len(errors), 1)
                self.assertIn("not included in the ZIP", errors[0])


if __name__ == "__main__":
    unittest.main()
