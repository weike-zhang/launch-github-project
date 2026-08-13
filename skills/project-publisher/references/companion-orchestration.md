# Companion orchestration

Project Publisher owns the release workflow, but some stages should use a more specialized Skill or host capability. Resolve those companions from the current session before editing. Do not infer activation from a directory, `skills-lock.json` or plugin manifest alone.

## Resolution protocol

1. Read the host-provided Skills and tools list.
2. Select only companions whose scope matches a real stage in the current task.
3. Add them to the working plan, tell the user why they apply and read their full instructions before use.
4. Run the companion at the stage below and preserve its validation boundary.
5. If it is unavailable, use the documented fallback and report the missing proof before that stage starts. Do not silently install or enable anything during the launch task.

## Installation and runtime state

The repository root contains `runtime/dependencies.json` and `scripts/install.py`. The installer places Project Publisher and its bundled Humanizer companion in the same Skill scope, checks required command-line tools, installs the dependency-guard Hook when accepted, and writes the result to `$HOME/.codex/project-publisher/install-state.json`.

Treat that file as evidence of the last install attempt, not as permanent truth. Recheck the host-provided Skills and tools before use. Interpret component states as follows:

- `installed`, `already_copied`, `already_linked` or `available`: the installer found the component, but the host must still expose it;
- `installed_pending_trust`: the Hook files and configuration exist, but Codex will skip the Hook until the user reviews and trusts it;
- `declined`: the user chose not to install that optional component;
- `failed` or `missing`: do not enter the affected stage without reporting the gap and fallback.

Installation consent does not authorize repository publication, package-manager changes or remote GitHub mutations. Conditional host capabilities such as image generation, browser inspection, a security reviewer and a GitHub connector cannot be made callable by copying Skill files. Resolve them from the active host when their stage is reached.

| Stage | Preferred companion | Required behavior | Fallback |
| --- | --- | --- | --- |
| Public prose and text inside images | `$humanizer` | Use file mode for one file or embedded mode inside the larger launch task, after facts and evidence are fixed | Run the manual AI-pattern, name-swap and desire-to-try checks in `readme-patterns.md`; report that Humanizer did not run |
| Raster artwork or image editing | Host image-generation Skill | Use it only after the visual-necessity gate; preserve source and rights evidence | Keep the existing asset, use a reproducible local renderer or omit the visual |
| Rendered README, UI or unsigned page | Host browser Skill | Inspect the visible normal and narrow states; after publication inspect the unsigned remote page | Mark source-only or authenticated checks as partial and leave unsigned rendering open |
| Security-focused review | Host security Skill or tool | Keep findings separate from the redacted secret scan and obtain authorization for deeper scans | Run the bundled secret and public-surface scripts; do not call them a security audit |
| Authorized GitHub mutation | Dedicated GitHub publishing Skill or connector | Confirm exact repository, branch, visibility, Release and external destinations immediately before mutation | Hand off exact commands or UI steps without performing the remote action |

## Humanizer contract

The plugin distributes Humanizer as a companion Skill, and the recommended Skills CLI command installs both Skills. This makes the companion available to hosts that load installed Skills; it does not force a host to invoke it.

When Humanizer is available:

- use the version bundled with the same Project Publisher package unless the user selects another installation;
- preserve commands, URLs, filenames, numbers, version strings, citations and explicit evidence limits;
- run its draft, audit and final loop internally;
- write only the final prose back in file or embedded mode;
- rerun the release-specific comprehension and desire-to-try gates afterward.

Do not send scripts, JSON, YAML or quoted evidence through a prose rewrite. Do not treat a natural voice as proof that the positioning, product behavior or claims are correct.

## Hook boundary

Hooks run because Codex loaded and trusted lifecycle configuration from the user, repository, administrator or an enabled plugin. A Skill cannot call a hook like a function.

- Inspect active hook configuration only when the task depends on it.
- Do not create, enable, trust or modify Hooks as an incidental part of a release audit. The explicit repository installer is the supported setup path.
- Treat hook output as one input to the workflow, not proof that every release gate passed.
- Run required deterministic checks directly even when a hook normally runs them.
- If a hook is missing, skipped, disabled or untrusted, report that state instead of fabricating a successful result.
- The bundled `UserPromptSubmit` dependency guard is a redundant alert path. The main Skill must still perform its own stage check when the Hook was declined, failed or skipped.

## Degraded-mode report

At handoff, name only material companion gaps. Use evidence states such as:

- `Humanizer: completed in embedded mode`;
- `Humanizer: unavailable; manual copy pass completed`;
- `Rendered README: source checked; browser proof unavailable`;
- `Unsigned remote page: pending publication`;
- `Hook-assisted gate: not loaded; direct script passed`.

Do not describe a missing optional companion as a release blocker when its documented fallback completed the same necessary check.
