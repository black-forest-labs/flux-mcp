# OpenAI plugin release checks

The package lives in `openai-plugin/`. ZIP that directory's contents so `plugin.json`, `mcp.json`, and `assets/` are at the archive root. Do not include this release guide or credentials in the ZIP.

The `OpenAI plugin package` workflow (`.github/workflows/openai-plugin-package.yml`) does this on every change to `openai-plugin/`: it validates both manifests against their declared schemas, checks asset paths, and uploads the ZIP plus `package-info.json` (version, source commit, SHA-256) as a run artifact. Use that ZIP rather than zipping by hand; the review cases and the portal upload stay manual.

## Code and package

- Merge the image release and public README changes first.
- Validate both JSON manifests against their declared Agent Plugins schemas and confirm every asset path exists.
- The manifest contains five positive and three negative review cases. Run them with a dedicated BFL reviewer account before submission and record the results. The presence of a test case is not evidence it passed.

## Hosted connection

1. Merge and deploy bfl-mcp #94.
2. Set `OPENAI_APPS_CHALLENGE_TOKEN` on the service serving `mcp.bfl.ai` to the portal's exact token.
3. Verify `https://mcp.bfl.ai/.well-known/openai-apps-challenge` returns only that token, then complete domain verification in the portal.
4. Connect with OAuth, complete the authenticated tool scan, and resolve its findings.
5. Run the review cases in ChatGPT. Check tool selection, the image viewer, and history with the reviewer account.
6. Supply reviewer login instructions and the walkthrough recording in the portal. Confirm the account and business requirements, including prepaid generation-credit eligibility, before requesting public review.

These hosted checks need the relevant BFL and OpenAI account access; local schema validation does not complete them.

Sources: [connect and test](https://developers.openai.com/plugins/deploy/connect-chatgpt), [submission requirements](https://developers.openai.com/plugins/deploy/submission).
