<p align="center">
  <img src="assets/hero.png" alt="Project Publisher helps people understand a project and keeps its public materials up to date" width="100%">
</p>

<p align="center">
  <strong>Your project changed. Its README, Release and launch posts did not. Project Publisher shows you what is out of date, fixes only the files you approve, and asks before it does anything on GitHub.</strong>
</p>

<p align="center">
  <a href="#find-what-stops-new-users-from-trying-it">Find what stops new users from trying it</a> ·
  <a href="examples/self-audit-bundle-safety.md">See the release leak it caught</a> ·
  <a href="README.zh-CN.md">简体中文</a>
</p>

A project can work well and still be hard for new users to understand. Its name may fit only the first demo. The README may start with details for maintainers. The install command may be buried, and the Release may list changes without saying why they matter.

Project Publisher reviews your project, fixes the public files you approve, and updates them when the project changes. It can also turn a real result or a caught failure into material you can share. The first review does not change files.

Install Project Publisher and its bundled Humanizer from the public repository:

```bash
git clone https://github.com/weike-zhang/project-publisher.git
python3 project-publisher/scripts/install.py
```

Then ask: `Use $project-publisher to review this project before I publish or update it. Do not change anything yet. Tell me what is most likely to stop a new visitor from trying it.` The first response shows what it found before any file changes. The v0.3.0 public clone, installer and Skills CLI setup were [tested from clean temporary folders](evals/results/public-install-v0.3.0.md). [An earlier Codex test covers the published v0.2.0 Skills-only install under the former name](evals/results/codex-first-audit-v0.2.0.md).

## Keep files from outside the project out of the release ZIP

While checking its own repository, the Skill found a symbolic link, which is a file that points to another file. That link pointed outside the project, and the old ZIP builder copied the outside file into the release.

```text
project/
├── README.md
└── outside.txt -> /etc/hosts

Release stopped: outside.txt is a symbolic link
ZIP not created; target file not read
```

The ZIP builder now stops before reading the outside file. The same release review checks both the README and the ZIP contents. Automated tests keep this bug from coming back.

[Read how the bug was found, fixed, and tested](examples/self-audit-bundle-safety.md) · [See the v0.1.2 Release for the fix](https://github.com/weike-zhang/launch-github-project/releases/tag/v0.1.2)

This example proves only that the ZIP check caught this known problem. It does not prove that a project is safe, useful, or popular.

## Find what stops new users from trying it

The installer adds Project Publisher and Humanizer, then checks that Python and Git are available. It also adds an optional Hook that warns when a needed tool or Skill is missing. You must review and trust that Hook with `/hooks` before it can run. If any part is missing, refused, or unavailable, Project Publisher tells you what it cannot check and what it can still do. [See every install option and limit](docs/INSTALL.md).

From the project you want to publish:

```text
Use $project-publisher to review this project before I publish or update it.
Do not change anything yet. Tell me what is most likely to stop a new visitor
from understanding or trying it. Show me what you found and suggest the smallest
useful fix. Ask before doing anything on GitHub.
```

The first response shows the project type, what was checked, the main problem, and what still needs your choice:

```text
Project type       Agent Skill
What I checked     SKILL.md, install path, scripts, release history
Biggest problem    no direct input/output example on the first screen
Blocks release     version in the files and latest Release do not match
Needs your choice  asset rights, visibility, exact GitHub repository
Changed            nothing
```

The answer changes with the project. The Skill checks first, marks what it had to assume, and explains why each file is needed. It waits for your approval before any GitHub change. See [installation and update options](docs/INSTALL.md).

## What it helps you fix

| Need | Result |
| --- | --- |
| The name fits only one demo or platform | A short name for what the project will keep doing, with details in the description |
| The README lists features but gives no reason to care | A clear reader problem, a useful result, proof, and a first step |
| The project changed but the README still teaches old commands | A full reread and an update where the old claim already lives |
| You do not know what is safe to publish | A secret check that hides matched values, plus clear questions about private data and rights |
| The README, tag, ZIP, and Release disagree | Matching version details and a ZIP whose contents were listed and extracted |
| A post only says that the repository exists | Shareable material built around a real result, a caught failure, or a test someone can repeat |

The exact files depend on the project. The Skill will not add a website, community, benchmark, or roadmap unless the project needs one.

## Automatic checks and human decisions

| Automated | Still requires judgment |
| --- | --- |
| Local links, unfinished text, and paths from your computer | Whether a new reader understands the first screen |
| Possible secrets, with matched values hidden | Whether a secret or personal detail is truly safe to share |
| Extra repositories, editor files, and private drafts | Whether you have the right to publish each image, file, and dataset |
| Whether the README, plugin version, tag, and Release agree | Whether the proof supports what the page promises |
| What is inside the ZIP and whether it can be extracted | Whether the project should be public and where it should live |

Passing these checks does not prove that the project is safe, useful, or wanted.

## How it works

1. Read the files, Git history, risks, and missing details without changing anything.
2. Work out the project type and whether the name matches what the project is becoming.
3. Put the reader's problem, a useful example, and the first step in a clear order.
4. Check links, possible secrets, images, versions, and the real ZIP file.
5. Prepare the Release and material you can share. Ask before any GitHub action.
6. Open the public page as a visitor. Read the full page again when the project changes.

## Evidence and compatibility

| What was tested | Status | Proof |
| --- | --- | --- |
| Public v0.2.0: full install, first run, and first review | Checked with Codex CLI 0.147.0-alpha.6.5 | [Install steps, clean test project, and result](evals/results/codex-first-audit-v0.2.0.md#post-publication-check) |
| Local v0.2.0 before release: project install, first run, and first review | Checked on the same computer | [Test project, command, and result with private values removed](evals/results/codex-first-audit-v0.2.0.md#release-candidate-check) |
| Public v0.3.0: clone, install, and find both Skills | Checked after the repository rename | [Test from a new empty folder](evals/results/public-install-v0.3.0.md) |
| Release scripts | Checked with Python 3.12 for public v0.2.0 | [Tests that keep fixed bugs from returning](tests/test_release_tools.py) and [the older GitHub Actions run](https://github.com/weike-zhang/launch-github-project/actions/workflows/validate.yml) |
| Project type examples and test files | Required files checked | [File checker](evals/validate_fixtures.py); this does not measure answer quality |
| Plan for sharing a project | One early comparison | [Exact prompt, answer without the Skill, answer with the Skill, and limits](evals/results/model-comparison.md) |
| Other tools that support Agent Skills | Not tested | Reports with the tool name and version are welcome |

## Permissions and limits

- Installing the Skill does not give it permission to create a repository, push code, change who can see it, publish a Release, or post anywhere. It asks before each GitHub action.
- The secret check looks for known patterns and can miss things. Review the result yourself.
- The ZIP builder rejects symbolic links and unusual file types. It cannot protect against every harmful file change while it runs.
- Automated checks cannot prove that you own every asset, that every detail is safe to share, that users want the project, or that GitHub looks right to a signed-out visitor.
- Working notes belong in `.project-publisher/`; the directory is ignored and excluded from release bundles.

Read [PRIVACY.md](PRIVACY.md), [SECURITY.md](SECURITY.md), the [visual asset notice](assets/ASSET-NOTICE.md) and [third-party notices](THIRD-PARTY-NOTICES.md) for the full details and limits.

## Contributing

The most useful contribution is a release problem someone else can repeat, a project type the Skill handles badly, a broken first-use path, or a public claim with no checkable proof. See [CONTRIBUTING.md](CONTRIBUTING.md).

MIT licensed. Built by [Weike Zhang](https://github.com/weike-zhang).
