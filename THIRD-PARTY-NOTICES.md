# Third-party notices

## Humanizer

- Source: [blader/humanizer](https://github.com/blader/humanizer)
- Version: 2.9.1
- Source commit reviewed: `523374dee72d67c7b2b5f858ea0094ffda49c3ac`
- Project lock hash: `7f032c368d4355fb237e1980d73d7febe5bc1a03bad3de74a3d4a918e8940cd1`
- License: MIT; the upstream license is preserved in both the project-level development copy and `skills/humanizer/LICENSE`.

Humanizer is distributed as a companion Skill used to review public prose and image text after factual claims are fixed. Its runtime instructions are Markdown. The project-level source copy also contains a local metadata validator; manual review found no network calls, environment-variable reads, shell execution or file-writing behavior in that script.

The Skills CLI installation report showed mixed automated results: Gen marked the package safe, Socket reported zero alerts and Snyk reported high risk without a public finding that could be independently verified. This repository records that unresolved scanner disagreement instead of treating popularity or one scanner as proof of safety.

The release bundler excludes `.agents/`, `.claude/` and `.codex/` development directories. The reviewed runtime subset in `skills/humanizer/` is included in the plugin and Release ZIP, while `skills-lock.json` records its upstream source and hash. The integrated installer installs this pinned bundled copy; it does not fetch unreviewed Humanizer code at install time.
