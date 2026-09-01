# Brightpath Pulse — Product FAQ

Brightpath Pulse is our B2B customer-support copilot. It drafts replies, searches a company’s knowledge base, and routes tickets. This FAQ is for employees answering prospects and customers. Public pricing pages may lag this document; internal figures below are the source of truth as of 1 August 2026.

## What does Pulse do?

Pulse sits on top of Zendesk, Freshdesk, or Intercom. It retrieves answers from the customer’s help center and internal macros, then suggests a reply for the human agent. Agents can accept, edit, or reject the draft. Pulse also tags tickets (billing, bug, how-to) and can auto-close duplicates when confidence is above 0.92.

Pulse does **not** send replies without an agent click, except on the Enterprise “autopilot” add-on for how-to tickets only.

## Pricing tiers (USD, billed annually)

| Plan | Price | Agents | Knowledge sources | Support |
| --- | --- | --- | --- | --- |
| Starter | **$12 / agent / month** | Up to 8 | 1 help center + 50 macros | Email, 1 business day |
| Pro | **$29 / agent / month** | Up to 50 | Unlimited articles, Slack, Notion | Chat + email, 8-hour response |
| Enterprise | Custom (starts at **$48 / agent / month**) | Unlimited | All Pro sources plus Confluence, Google Drive, Salesforce | Dedicated CSM, 1-hour Sev-1 |

Monthly billing is 20% more than the annual price. A 14-day free trial is available on Starter and Pro. No credit card is required for the trial.

## Usage limits

Starter includes 2,000 AI drafts per month for the workspace. Pro includes 15,000. Enterprise is unlimited with a fair-use cap of 250,000 drafts per month. Extra Starter drafts can be purchased in packs of 1,000 for $40.

File uploads for knowledge: PDFs, Markdown, DOCX, and HTML. Maximum file size is **25 MB**. Pulse does not ingest video or spreadsheets in v3.

## Languages

Pulse drafts in English, Hindi, Spanish, French, German, Portuguese, and Japanese. Starter is English-only. Hindi and Japanese require Pro or higher.

## Integrations

Native connectors: Zendesk, Freshdesk, Intercom, Slack, Notion, Confluence (Enterprise), Salesforce Service Cloud (Enterprise). Jira and Linear are on the Q4 2026 roadmap; do not promise them on sales calls.

SSO (SAML/OIDC) and SCIM are Enterprise-only. Pro supports Google Workspace login.

## Support and SLAs

Customers email support@brightpath.example. Pro customers may use in-app chat, 09:00–21:00 IST, Monday–Friday. Enterprise Sev-1 (full outage) has a **1-hour** first-response SLA, 24/7. Status page: status.brightpath.example.

If a customer asks for on-premise deployment: Pulse is SaaS-only. A private VPC deploy (AWS Dedicated) is an Enterprise option with a 12-week lead time and a $25,000 onboarding fee.

## Data and retention

Ticket text used for drafting is retained 30 days for debugging, then deleted. Customers on Enterprise can request zero-retention mode (no prompt logs). Pulse is trained on public data and licensed corpora; customer tickets are **not** used to train foundation models.

## Common objections

- “We already have macros.” Pulse ranks macros and knowledge together so agents stop hunting across three tabs.
- “Hallucinations.” Drafts include source citations. The agent UI highlights sentences that are not grounded; those are shown in amber.
- “Security.” SOC 2 Type II report is in the sales Drive folder. Data is encrypted at rest (AES-256) and in transit (TLS 1.2+).
