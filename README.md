<p align="center">
  <a href="https://bfl.ai">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://bfl.ai/brand/logotype-white.svg">
      <source media="(prefers-color-scheme: light)" srcset="https://bfl.ai/brand/logotype-black.svg">
      <img alt="Black Forest Labs" src="https://bfl.ai/brand/logotype-black.svg" width="220">
    </picture>
  </a>
</p>

<h1 align="center">FLUX MCP</h1>

<p align="center">
  <strong>Bring FLUX into the tools you already use.</strong><br>
  Generate, edit, vary, and browse FLUX images from any MCP-compatible client.
</p>

<p align="center">
  <a href="https://registry.modelcontextprotocol.io/?q=io.github.black-forest-labs%2Fflux-mcp"><img alt="MCP Registry" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fregistry.modelcontextprotocol.io%2Fv0.1%2Fservers%2Fio.github.black-forest-labs%252Fflux-mcp%2Fversions%2Flatest&query=%24.server.version&label=MCP%20Registry&logo=modelcontextprotocol&color=b9b5d0"></a>
  <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-07130e.svg"></a>
  <a href="https://docs.bfl.ai/api_integration/mcp_integration"><img alt="Docs" src="https://img.shields.io/badge/Docs-docs.bfl.ai-07130e"></a>
</p>

<p align="center">
  <a href="#install">Install</a> ·
  <a href="#showcase">Showcase</a> ·
  <a href="#tools">Tools</a> ·
  <a href="#example-prompts">Examples</a> ·
  <a href="#troubleshooting">Troubleshooting</a>
</p>

<p align="center">
  <video src="https://github.com/black-forest-labs/flux-mcp/raw/main/assets/demo.mp4" controls width="100%"></video>
</p>

---

The **FLUX MCP server** exposes the full FLUX.2 toolkit — text-to-image, image editing, multi-reference composition, variations, and history — to any client that speaks the [Model Context Protocol](https://modelcontextprotocol.io). Generate options in parallel, edit attached images through prompts, and branch into variations from any result you like. No API code, no keys pasted into the conversation.

- **Hosted, remote, OAuth-only.** Connect to `https://mcp.bfl.ai`. Sign in with your BFL account, pick the org to bill — done.
- **Every FLUX.2 model.** Pro, Max, Klein (4B & 9B), Flex. Your client picks the right one for the task.
- **Built for chat.** Up to 8 images in parallel per prompt. Edit attached images. Browse and reuse history.
- **You pay BFL directly.** No middleman, no shared quotas. Current rates: [bfl.ai/pricing](https://bfl.ai/pricing).

---

## Install

<details open>
<summary><strong>Claude — Desktop &amp; claude.ai</strong></summary>

1. Open [Settings → Connectors](https://claude.ai/settings/connectors).
2. Click **Add custom connector**.
3. Name it `FLUX`, URL `https://mcp.bfl.ai`.
4. Click **Connect**, sign in, choose the BFL organization to bill.

</details>

<details>
<summary><strong>Claude Code</strong></summary>

```bash
claude mcp add --transport http FLUX https://mcp.bfl.ai
```

A browser opens on first use for OAuth. Tokens refresh automatically.

</details>

<details>
<summary><strong>Cursor</strong></summary>

**One-click:** [Add to Cursor](cursor://anysphere.cursor-deeplink/mcp/install?name=FLUX&config=eyJ1cmwiOiJodHRwczovL21jcC5iZmwuYWkifQ==) — opens Cursor with the FLUX server pre-filled.

**Manual** — add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "FLUX": {
      "url": "https://mcp.bfl.ai"
    }
  }
}
```

</details>

<details>
<summary><strong>Codex</strong></summary>

```bash
codex mcp add flux --url https://mcp.bfl.ai
codex mcp login flux
```

Or append to `~/.codex/config.toml`:

```toml
[mcp_servers.flux]
url = "https://mcp.bfl.ai"
```

</details>

<details>
<summary><strong>Windsurf</strong></summary>

Edit `~/.codeium/windsurf/mcp_config.json` (note Windsurf uses `serverUrl`, not `url`):

```json
{
  "mcpServers": {
    "FLUX": {
      "serverUrl": "https://mcp.bfl.ai"
    }
  }
}
```

Reload plugins from the Cascade panel. The first FLUX call opens a browser for sign-in.

</details>

<details>
<summary><strong>Other MCP clients (stdio bridge via <code>mcp-remote</code>)</strong></summary>

For clients that support stdio MCP but don't handle the OAuth flow themselves — for example **Hermes** (Nous Research) and similar tools that only accept static bearer tokens:

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

</details>

---

## Showcase

### Generate a batch of options in one prompt

> *"Generate 4 editorial portrait variants — varied lighting, palette, and mood."*

<p align="center">
  <img src="https://cdn.sanity.io/images/2gpum2i6/production/c3f2d4e1211258390694350b73564199b0ec1f9b-1440x1792.jpg" width="24%">
  <img src="https://cdn.sanity.io/images/2gpum2i6/production/a4016c043d3afb049d51381b0695d52411030026-1440x1792.jpg" width="24%">
  <img src="https://cdn.sanity.io/images/2gpum2i6/production/d3e95a7892d15aa647ea098bdf66256cc5d4de31-1440x1792.jpg" width="24%">
  <img src="https://cdn.sanity.io/images/2gpum2i6/production/f6eaa9ed0645cdd9df0ceeaf5962477958c15be4-1440x1792.jpg" width="24%">
</p>

### Or just one — when a single hero shot is what you need

> *"A top-down aerial photograph of shallow desert salt pools, intense direct sunlight."*

<p align="center">
  <img src="https://cdn.sanity.io/images/2gpum2i6/production/0dc6f45f41c1e8d2b6606285b4c785d6cfc586e0-1920x1440.jpg" width="100%">
</p>

### Edit any image directly in chat

> *"Add a camel on the sand."*

<table>
  <tr>
    <td align="center"><strong>Before</strong></td>
    <td align="center"><strong>After</strong></td>
  </tr>
  <tr>
    <td><img src="https://cdn.sanity.io/images/2gpum2i6/production/0dc6f45f41c1e8d2b6606285b4c785d6cfc586e0-1920x1440.jpg"></td>
    <td><img src="https://cdn.sanity.io/images/2gpum2i6/production/627eb91f1da5299c96c1d591b0bbc48368c4e2f2-1920x1440.jpg"></td>
  </tr>
</table>

### Browse and reuse your full generation history

> *"Show me my recent FLUX generations."*

Every generation is saved. Tap any tile to edit, vary, or download. Variations branch off any past image in one click.

---

## Tools

Your client picks which tool to call based on your prompt — you don't need to invoke them by name.

| Tool | What it does |
| --- | --- |
| `generate_image` | Generate **1–8 images in parallel**. Covers text-to-image, edits, multi-reference composition, style transfer, inpainting-style edits, and outpainting — all through prompts. |
| `generate_variations` | Produce N more images **in the same direction** as a previous generation (identified by `request_id`). Defaults to 4, max 8. |
| `get_history` | List recent generations as a **thumbnail grid** with per-tile Variations / Edit / copy / download actions. Keyset pagination, date filters. |
| `get_credits` | Return your remaining BFL credit balance. |

### Models

Available on `generate_image`:

| Model | Use it for |
| --- | --- |
| `flux2_pro_preview` *(default)* | Everyday work — best balance of quality and speed |
| `flux2_max` | Hero shots, final assets — highest quality |
| `flux2_klein_9b_preview` | Faster iterations, up to 4 input images |
| `flux2_klein_4b` | Fastest option |
| `flux2_flex` | Typography and readable text |

The full catalog and per-model reference-image limits are also exposed as the `bfl://models` MCP resource.

---

## Example prompts

Try these in your client once FLUX is connected:

```
Generate 4 editorial portrait variants — varied lighting, palette, and mood.
Use FLUX.2 [pro] at 1440×1792.
```

```
A top-down aerial photograph of shallow desert salt pools at golden hour,
intense direct sunlight, #FF6B6B and #F5E6D3 mineral deposits, FLUX.2 [max].
```

```
[attach an image]
Add a camel on the sand. Preserve the rest of the composition exactly.
```

```
Generate a movie poster with the title "MIRAGE" in 1970s grindhouse type,
high-contrast cyan and orange. Use FLUX.2 [flex].
```

```
Show me my recent FLUX generations.
```

```
[click Variations on a past image]
4 more like this one, vary the lighting.
```

---

## Prompt tips

- **Front-load the subject.** Put the most important object, person, or scene first.
- **Describe lighting.** *"Soft golden hour light"* or *"overcast diffused studio light"* gives the model useful direction.
- **Use hex colors.** `#FF6B6B (coral pink)` is more precise than *"pinkish red"*.
- **Quote rendered text.** Use exact quoted strings for typography, labels, posters, and signs.
- **Avoid negative prompts.** FLUX responds to what you describe, not a list of what to avoid.
- **Iterate from results.** Use Variations for alternatives, or Edit to keep refining a generated image.

For the full FLUX prompting playbook, see [black-forest-labs/skills](https://github.com/black-forest-labs/skills).

---

## Troubleshooting

<details>
<summary><strong>Tools don't appear after connecting</strong></summary>

- **Claude Desktop / claude.ai:** Settings → Connectors, confirm FLUX shows as **Connected**. If it failed silently, remove and re-add — make sure pop-ups aren't blocked so the OAuth window can open.
- **Claude Code:** `claude mcp list` should show the server.
- **Codex:** `codex mcp list` should show `flux`. Start a new Codex session after adding.
- Quick smoke test: ask your client *"check my BFL credits"*.

</details>

<details>
<summary><strong>Refreshing tools or reconnecting the server</strong></summary>

- **Claude.ai / Desktop:** Settings → Connectors → toggle FLUX off and on, or click **Reconnect**.
- **Claude Code:** `/mcp` shows status and reauth. Full rebuild:
  ```bash
  claude mcp remove FLUX
  claude mcp add --transport http FLUX https://mcp.bfl.ai
  ```
- **Codex:** `codex mcp login flux`. Full rebuild:
  ```bash
  codex mcp remove flux
  codex mcp add flux --url https://mcp.bfl.ai
  ```
- **mcp-remote clients:** `rm -rf ~/.mcp-auth` and restart the client to force a fresh OAuth.

</details>

<details>
<summary><strong>Authentication or billing errors</strong></summary>

- Make sure you have a BFL account at [bfl.ai](https://bfl.ai).
- Disconnect and reconnect the connector to redo OAuth.
- Check the selected organization has sufficient credits.
- Ask your client to check your BFL credits to verify the balance.

</details>

<details>
<summary><strong>A generation keeps loading</strong></summary>

Large batches, FLUX.2 [max], or complex edits take longer than smaller generations. Visual MCP clients update the image view automatically.

</details>

<details>
<summary><strong>Attached image editing fails</strong></summary>

Your MCP client needs permission to upload attached images to BFL. If your client blocks outbound HTTPS from its sandbox, allow `*.bfl.ai` or pass a public image URL instead.

</details>

<details>
<summary><strong>Switching the billed organization</strong></summary>

Disconnect the FLUX connector in your client and reconnect it. The OAuth flow will prompt you to select an organization again.

</details>

---

## Agent Skills (companion repo)

MCP and Agent Skills solve different problems:

|  | MCP (this repo) | [Agent Skills](https://github.com/black-forest-labs/skills) |
| --- | --- | --- |
| **What it does** | Generates, edits, varies, and browses images directly in chat | Teaches your coding agent how to write FLUX API code |
| **Best for** | Creative work inside Claude or another MCP client | Building applications that call the FLUX API |

Use both. They complement each other.

---

## Links

- **Docs** — [docs.bfl.ai](https://docs.bfl.ai)
- **Pricing** — [bfl.ai/pricing](https://bfl.ai/pricing)
- **Status** — [status.bfl.ai](https://status.bfl.ai)
- **Black Forest Labs** — [bfl.ai](https://bfl.ai)

---

## License

[MIT](./LICENSE) © Black Forest Labs
