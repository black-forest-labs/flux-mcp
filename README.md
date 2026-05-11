# FLUX MCP

Generate, edit, vary, and browse FLUX images from any MCP-compatible client.
All FLUX.2 models, OAuth sign-in, no API keys to manage.

**Server URL:** `https://mcp.bfl.ai`
**Docs:** https://docs.bfl.ai/api_integration/mcp_integration

---

## What you get

- Generate up to 8 images in parallel from a single prompt
- Edit attached images directly in chat
- Branch into N variations from any past generation
- Browse and reuse your full generation history
- All FLUX.2 models: Pro, Max, Klein (4B & 9B), Flex
- OAuth — your billed BFL organization is selected at sign-in, no API keys

You pay BFL directly. Current rates: https://bfl.ai/pricing

---

## Install

### Claude (Desktop & claude.ai)

Settings → Connectors → **Add custom connector**

- **Name:** `FLUX`
- **URL:** `https://mcp.bfl.ai`

Click **Connect**, sign in with your BFL account, choose the billed organization.

### Claude Code

```bash
claude mcp add --transport http FLUX https://mcp.bfl.ai
```

A browser opens on first use for OAuth.

### Cursor

One-click install: [![Add to Cursor](https://img.shields.io/badge/Add%20to-Cursor-black)](cursor://anysphere.cursor-deeplink/mcp/install?name=FLUX&config=eyJ1cmwiOiJodHRwczovL21jcC5iZmwuYWkifQ==)

Or paste into `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "FLUX": {
      "url": "https://mcp.bfl.ai"
    }
  }
}
```

### Codex

```bash
codex mcp add flux --url https://mcp.bfl.ai/
codex mcp login flux
```

Or append to `~/.codex/config.toml`:

```toml
[mcp_servers.flux]
url = "https://mcp.bfl.ai/"
```

### Windsurf

Edit `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "FLUX": {
      "serverUrl": "https://mcp.bfl.ai"
    }
  }
}
```

Note Windsurf uses `serverUrl`, not `url`.

### Other MCP clients (stdio bridge)

For clients that support stdio MCP but don't handle the OAuth flow themselves (e.g. Hermes / Nous Research, and similar tools that only accept static bearer tokens):

```json
{
  "mcpServers": {
    "FLUX": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.bfl.ai"]
    }
  }
}
```

`mcp-remote` opens a browser for OAuth, caches tokens to `~/.mcp-auth/`, and refreshes them automatically.

---

## Tools

Your client picks which tool to call based on your prompt — you don't need to invoke them by name.

| Tool | Purpose |
| --- | --- |
| `generate_image` | Generate 1–8 images in parallel. Text-to-image, edits, multi-reference composition, style transfer, inpainting, outpainting — all via prompt. |
| `generate_variations` | Produce N more images in the same direction as a previous generation (identified by `request_id`). |
| `get_history` | List recent generations as a thumbnail grid, with per-tile Variations / Edit / copy / download actions. |
| `get_credits` | Return your remaining BFL credit balance. |

### Models

Available on `generate_image`:

- `flux2_pro_preview` (default) — best balance of quality and speed
- `flux2_max` — highest quality, slower
- `flux2_klein_9b_preview` — faster, accepts up to 4 input images
- `flux2_klein_4b` — fastest
- `flux2_flex` — best for typography and readable text

The full catalog and per-model reference-image limits are also exposed as the `bfl://models` MCP resource.

---

## Prompt tips

- **Front-load the subject.** Put the most important object, person, or scene first.
- **Describe lighting.** "Soft golden hour light" or "overcast diffused studio light" gives the model useful direction.
- **Use hex colors.** `#FF6B6B (coral pink)` is more precise than "pinkish red".
- **Quote rendered text.** Use exact quoted strings for typography, labels, posters, and signs.
- **Avoid negative prompts.** FLUX responds to what you describe, not a list of what to avoid.
- **Iterate from results.** Use Variations for alternatives, or Edit to keep refining a generated image.

---

## Troubleshooting

**Tools don't appear after connecting**
- In Claude Desktop / claude.ai: Settings → Connectors, confirm FLUX shows as **Connected**. Remove and re-add if needed.
- In Claude Code: `claude mcp list` should show the server.
- In Codex: `codex mcp list` should show `flux`. Start a new Codex session after adding.

**Refreshing tools or reconnecting**
- **Claude.ai / Desktop:** Settings → Connectors → toggle off/on or **Reconnect**.
- **Claude Code:** `/mcp` shows status and reauth. Full reset: `claude mcp remove FLUX && claude mcp add --transport http FLUX https://mcp.bfl.ai`.
- **Codex:** `codex mcp login flux`. Full reset: `codex mcp remove flux && codex mcp add flux --url https://mcp.bfl.ai/`.
- **mcp-remote clients:** `rm -rf ~/.mcp-auth` and restart the client to force a fresh OAuth.
- Quick smoke test: ask your client *"check my BFL credits"*.

**Authentication or billing errors**
- Make sure you have a BFL account at https://bfl.ai.
- Disconnect and reconnect to redo OAuth.
- Check the selected organization has sufficient credits.

**A generation keeps loading**
Large batches, FLUX.2 [max], or complex edits take longer. Visual MCP clients update the image view automatically.

**Attached image editing fails**
Your client needs permission to upload attached images to BFL. If your client blocks outbound HTTPS from its sandbox, allow `*.bfl.ai` or use a public image URL instead.

**Switching the billed organization**
Disconnect the connector and reconnect — the OAuth flow will prompt you to pick an organization again.

---

## Registry

This server is published to the official MCP Registry as `ai.bfl/mcp`, which means it auto-appears on:

- https://github.com/mcp/ai.bfl/mcp
- https://glama.ai
- https://mcp.so
- https://pulsemcp.com
- Smithery, LobeHub, and other aggregators

See [`server.json`](./server.json) for the registry entry.

---

## Links

- **Docs:** https://docs.bfl.ai/api_integration/mcp_integration
- **Pricing:** https://bfl.ai/pricing
- **Help:** https://help.bfl.ai
- **Status:** https://status.bfl.ai
- **BFL:** https://bfl.ai

---

## License

MIT — see [LICENSE](./LICENSE).
