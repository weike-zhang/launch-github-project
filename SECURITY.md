# Security and public-release safety

This project prepares local release artifacts. It does not publish, push, change repository visibility, or send external messages by itself.

At the public-release gate:

1. Run `python skills/launch-github-project/scripts/check_secrets.py . --json`.
2. Read every redacted finding and decide whether to remove, replace, keep local, or obtain permission.
3. Do not paste full secrets into an issue or chat. Rotate a credential if it was exposed.
4. Treat third-party images, fonts, datasets, logos, and copied README text as ownership decisions.

Report a security issue privately to the repository owner rather than opening a public issue with sensitive data.
