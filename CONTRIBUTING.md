# Contributing to FLUX MCP

Thanks for helping improve the FLUX MCP server.

This repo is the **public-facing surface** for the FLUX MCP server hosted at
`https://mcp.bfl.ai`. It contains the README, install instructions, registry
metadata, and supporting assets. The server itself is hosted by Black Forest
Labs and is not open source.

## What belongs here

Issues and PRs in this repo are for:

- Install / setup problems with a specific MCP client.
- Errors in the README or examples.
- Suggestions for new install paths, tool documentation, or showcase content.
- Documentation feedback on `docs.bfl.ai/api_integration/mcp_integration`.

## What goes elsewhere

| You're hitting... | File it at... |
| --- | --- |
| A bug in the FLUX API itself (wrong output, billing, account) | [help.bfl.ai](https://help.bfl.ai) |
| `mcp.bfl.ai` is unreachable or OAuth is broken | Check [status.bfl.ai](https://status.bfl.ai) first, then [help.bfl.ai](https://help.bfl.ai) |
| Prompt quality / model output tips | [black-forest-labs/skills](https://github.com/black-forest-labs/skills) |

## Filing an issue

Use one of the [issue templates](https://github.com/black-forest-labs/flux-mcp/issues/new/choose):

- **Bug report** — for things that don't work.
- **Feature request** — for things you wish worked differently.

Please include your MCP client + version, your OS, and any error logs.

## Submitting a PR

1. Fork the repo.
2. Create a branch from `main`. Branch naming: `<your-handle>/<short-description>`.
3. Make your change. Keep the diff focused — one logical change per PR.
4. Open a PR against `main`.

`main` is protected: every change lands via PR.

### Style notes

- **No trailing slashes** on `bfl.ai` URLs anywhere — write `https://mcp.bfl.ai`, not `https://mcp.bfl.ai/`.
- **Always** capitalize **FLUX**. Models use bracketed variants: FLUX.2 [pro], FLUX.2 [max], FLUX.2 [klein], FLUX.2 [flex].
- The README's install snippets are kept in sync with `docs.bfl.ai/api_integration/mcp_integration` — please update both if you're changing install flow.

## License

By contributing, you agree your contributions are licensed under the [MIT License](./LICENSE).
