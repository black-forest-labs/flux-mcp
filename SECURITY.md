# Security Policy

## Reporting a Vulnerability

If you've found a security issue in the FLUX MCP server (`https://mcp.bfl.ai`),
the OAuth flow, or anything in this repository — **please don't open a public
GitHub issue**.

Report it privately via GitHub's [Security Advisories](https://github.com/black-forest-labs/flux-mcp/security/advisories/new),
or email `security@blackforestlabs.ai`.

We'll acknowledge receipt within 3 business days and keep you posted as we
investigate and ship a fix.

## Scope

In scope:

- The hosted FLUX MCP server at `https://mcp.bfl.ai` (auth, OAuth flow, tool
  exposure, data handling).
- This repository's docs and install instructions (e.g. anything that could
  trick users into running unsafe configurations).

Out of scope (please report via [docs.bfl.ai](https://docs.bfl.ai) instead):

- The FLUX REST API itself (non-MCP).
- The FLUX models' outputs or behavior.
- Other Black Forest Labs products.

## Public disclosure

Coordinated disclosure is appreciated. We'll work with you on a disclosure
timeline and credit you in the advisory if you'd like.
