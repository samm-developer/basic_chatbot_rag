# Brightpath Engineering Onboarding

Welcome to engineering. This guide covers your first two weeks, our repos, how we ship, and on-call. Pair it with the employee handbook for HR topics and the IT policy for laptop setup.

## Day 0–1: accounts

IT will ship a MacBook with Jamf. After FileVault and Okta, install:

- 1Password, Slack, Google Workspace, GitHub (SSO), Linear, Notion, Tailscale
- Homebrew, `direnv`, Docker Desktop, VS Code or Cursor, `fnm` for Node 22, Python 3.12 via `uv`

Join Slack channels: `#eng-all`, `#deploys`, `#incidents`, `#pulse-backend`, `#pulse-frontend`. Set your GitHub username in the eng-onboarding Linear project so we can add you to the `brightpath-eng` org.

## Repositories

The product lives in GitHub org `brightpath-eng`:

- `pulse-api` — Python FastAPI service (primary backend)
- `pulse-web` — Next.js agent console
- `pulse-ingest` — document workers and embeddings jobs
- `pulse-infra` — Terraform for AWS (ap-south-1) and Cloudflare
- `pulse-eval` — RAG quality fixtures and offline evals

Default branch is `main`. Protected: 1 approval, CI green, no force-push. Commit messages follow Conventional Commits (`feat:`, `fix:`, `chore:`).

Clone with SSH after adding your key to GitHub. Run `make bootstrap` in `pulse-api` and `pnpm install` in `pulse-web`.

## Local development

`pulse-api` needs Postgres 16, Redis, and a local OpenAI key in `.env`. Docker Compose in that repo starts Postgres and Redis. Never point a laptop at production databases.

Feature flags live in LaunchDarkly. Dev environment is `pulse-dev`. Staging is `pulse-staging` (auto-deploys from `main`). Production deploys from annotated git tags `vX.Y.Z`.

## How we ship

1. Pick a Linear ticket in the current cycle (two-week cycles, Monday kickoff)
2. Branch `feat/<ticket-id>-short-name`
3. Open a PR; request review from the CODEOWNERS of the paths you touched
4. After merge, staging updates in about 12 minutes via GitHub Actions + ECS
5. Production: the day’s **ship captain** (rotates weekly, posted in `#deploys`) cuts a tag after 10:00 IST once staging soak looks healthy

Hotfixes skip the cycle but still need one approval and a post-merge Linear ticket.

## Environments and URLs

- Dev: `http://localhost:8000` (API), `http://localhost:3000` (web)
- Staging: `https://staging-api.brightpath.example`, `https://staging.console.brightpath.example`
- Production: `https://api.brightpath.example`, `https://console.brightpath.example`

Staging shares no customer data. It is seeded with synthetic tenants named `acme-demo` and `northwind-demo`.

## On-call

Backend and platform engineers join the PagerDuty rotation after **30 days** on the team (not during probation unless you opt in). Rotation is **one week**, Monday 11:00 IST to the next Monday 11:00 IST. Primary and secondary are paired.

- Sev-1 (API down, data loss risk): acknowledge in **15 minutes**, join the Zoom bridge from the PagerDuty note
- Sev-2 (elevated errors, single-tenant outage): acknowledge in 30 minutes
- Sev-3: next business day

On-call stipend is ₹8,000 per week. Overnight pages that take more than 30 minutes of work earn a recovery day, booked with your manager. The runbook is in Notion: “Pulse Incident Runbook”. Never debug production from a café network without Tailscale.

## Architecture snapshot

Inbound tickets hit `pulse-api`. Retrieval uses OpenAI `text-embedding-3-small` and Postgres pgvector in RDS. Generation uses `gpt-4o-mini` by default; Enterprise tenants can pin `gpt-4o`. Embeddings are stored per-tenant in schema-separated tables. Do not query another tenant’s schema, even in staging.

## First-week checklist

- Pair on a “good first issue” labeled `onboarding`
- Ship one staging deploy (even a docs PR)
- Watch one production deploy with the ship captain
- Read the last two incident write-ups in `#incidents`
- Schedule a 30-minute 1:1 with your manager and your onboarding buddy
