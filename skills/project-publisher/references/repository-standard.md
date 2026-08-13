# Repository standard

## Minimum public contract

A release-ready repository should answer:

1. What is this?
2. Who is it for?
3. What can they do with it?
4. How do they start?
5. What evidence supports its claims?
6. What are the limits and risks?
7. Under what terms can it be reused?
8. How can someone report a problem or contribute?

## Evidence states

- **Verified**: observed in the current environment or supported by saved raw evidence.
- **Partial**: some components were checked, but the full user path was not observed.
- **Unverified**: plausible or documented, but not checked in the current release.

Do not collapse partial and unverified into "supported."

## Repository hygiene

- No secrets, credentials, private state, customer data or unnecessary personal information.
- No generated caches, environment folders, editor metadata or machine-specific paths unless intentionally documented.
- No unresolved TODO placeholders in public-facing material.
- No broken relative links.
- No copied third-party assets without attribution and reuse rights.
- No commands that depend on unstated prerequisites.

## Git hygiene

Inspect status and diff before staging. Preserve unrelated user work. Compare content before synchronizing an existing remote. Never rewrite history, force-push, delete branches or make a repository public without explicit authorization.

## Proportionate community files

Add contribution, security, support or code-of-conduct files when the expected use justifies them. A tiny personal reference repository may need only a README and License; a tool accepting external contributions benefits from more explicit governance.
