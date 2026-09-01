# Brightpath Solutions — IT and Security Policy

Owner: Information Security team. Last review: 15 March 2026. Violations may result in device lockout and disciplinary action. Report incidents immediately to security@brightpath.example or #sec-incidents on Slack.

## Account and password rules

Every employee receives a Google Workspace account (`first.last@brightpath.example`) and Okta SSO. Passwords must be:

- At least **14 characters**
- A unique passphrase, not reused from personal accounts
- Rotated every **90 days**
- Stored only in the company 1Password vault

SMS is not an accepted second factor. Use a hardware key (YubiKey) or an authenticator app. Sharing passwords in Slack, email, or screenshots is forbidden.

## Devices

Company-issued MacBooks are the default. Personal laptops may not access production systems. Disk encryption (FileVault) must stay enabled. OS updates must be installed within 7 days of release. Lost or stolen devices must be reported within **2 hours** so MDM can remote-wipe the machine.

USB storage is blocked on company laptops. Use Google Drive or the approved S3 buckets for file transfer.

## Network and VPN

Office Wi-Fi SSIDs are `Brightpath-Corp` (staff) and `Brightpath-Guest` (visitors). Staff Wi-Fi uses certificate authentication via Jamf. When off-network, connect to **Tailscale** before opening internal tools (Grafana, admin dashboards, staging). Public coffee-shop Wi-Fi is allowed only with Tailscale connected.

## Data classification

- **Public:** marketing site, published docs
- **Internal:** handbook, sprint boards, non-customer metrics
- **Confidential:** customer names, contracts, source code
- **Restricted:** production credentials, PII, payment data

Restricted data must never be copied to personal email, WhatsApp, or unsanctioned SaaS tools. Customer PII stays in the EU/India regions configured in the product.

## Production access

Production SSH and Kubernetes access is granted via Okta + Teleport, not static keys. Access reviews happen every quarter. Engineers who leave a squad lose production access within 24 hours. Copying production databases to laptops is not allowed; use anonymized staging snapshots.

## Incident response

If you suspect a phish, malware, or leaked secret:

1. Do not click further links or enter credentials
2. Message #sec-incidents and email security@brightpath.example
3. The security on-call will open a PagerDuty incident within 15 minutes during business hours
4. Password resets and token revocation are handled by IT; do not “test” the stolen credential

The target acknowledgement time for a Sev-1 security incident is **15 minutes**; containment target is 4 hours.

## Software installs

Only apps in the Jamf Self Service catalog may be installed without a ticket. Shadow IT (personal Dropbox, unsanctioned ChatGPT plugins with customer data, random Chrome extensions) is not permitted. Need a new tool? File an IT request; Security reviews it within 5 business days.

## Phishing simulations

Security runs quarterly phishing tests. Failing two tests in a year requires a 30-minute awareness session. Reporting a real phish via the “Report phish” Gmail button earns a shout-out in the monthly all-hands.
