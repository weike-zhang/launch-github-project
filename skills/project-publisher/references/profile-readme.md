# GitHub profile README

Build or refresh the account-level README that GitHub renders at the top of a
user's profile page, then shape the repository list it sits above.

## When to use

A profile README earns its place when the account has enough real material to
point at, not as an empty placeholder. Create or update it when:

- the account has two or more original repositories worth showing;
- a user wants recruiters, collaborators or visitors to understand who they are
  and what they ship in one screen;
- the account is used for open-source contributions and the contribution trail
  should reflect the original projects, not a wall of forks.

Do not create one for an account with nothing concrete to show, and do not pad
it with invented metrics, links or claims.

## Repository mechanics

A profile README must live in a public repository named exactly
`<username>/<username>` (for `weike-zhang` that is `weike-zhang/weike-zhang`),
and the file must be named `README.md` on the default branch. GitHub renders it
automatically; there is no setting to toggle.

Check first:

```sh
gh api "repos/<owner>/<owner>" --jq '.name'   # 404 = does not exist yet
gh repo create <owner>/<owner> --public --description "Profile README"
```

If the repo already exists, read its current `README.md` before editing and
preserve anything the user wants kept.

## Content that comes from the account, not from a template

Pull every fact from the user's actual account and projects. Do not invent a
job title, employer, location, contact method, follower count, star count, or
"open to work" status that the user did not provide.

- Name and one line about what they build or study.
- Two to four original repositories, each with one line about what it does and
  why it exists. Link each one.
- A short "open-source contributions" section listing merged or submitted PRs,
  with repository names. Mark merged and in-progress separately and do not claim
  a PR merged before it is.
- Technologies actually used.
- A real contact channel the user controls. GitHub issues/PRs is the safest
  default; never fabricate an email or social handle.

## Decide language and structure

The profile page is public and global, and GitHub renders only the single
`README.md` from the `<username>/<username>` repository. That constraint shapes
how bilingual copy works here: you cannot ship a second rendered file like a
project README can (`README.zh-CN.md`). Apply the bilingual rules from
[chinese-public-copy.md](chinese-public-copy.md) inside one file.

Rules:

- English is the safe default for the main narrative when the audience is mixed
  or unknown.
- When the user's community is predominantly Chinese-speaking, write a
  self-contained Chinese section, not a translated echo. Do not start it with a
  label such as "中文:" or "简体中文". A label header reads like a machine
  translation note, not like a person introducing themselves.
- Each language block must read as an independent narrative with its own hook,
  its own facts and its own reading order, exactly as a bilingual project README
  does across its two files. The Chinese block is not a footnote to the English
  one; it stands alone for a Chinese-speaking visitor.
- Keep the facts identical across languages: same projects, same PR states,
  same contact. Only the wording, order and emphasis differ per language.
- Run the native-speaker checks from `chinese-public-copy.md` on the Chinese
  block: would a Chinese developer say this to a colleague? Is the verb early
  enough? Is there a sentence a reader can repeat back?

A workable single-file bilingual structure is two clearly separated sections
with plain headings in each language's own words (for example an English
introductory section followed by a Chinese section that restates who this is and
what they build for a Chinese reader, with no cross-language label prefix on
either).

## Order the page around a visitor's decision

The reader is usually a recruiter, a collaborator, or another developer deciding
whether to look closer. Lead with who you are and what you build, then show the
strongest original projects, then the contribution trail, then how to reach you.
Do not bury the projects below a long self-description.

Give every section one job:

- introduction: who this is and what they build;
- projects: what each shipped thing does and why it exists;
- contributions: evidence of working with other communities;
- contact: the one channel a visitor can actually use.

## Handle the repository list under the profile

The profile README renders above the pinned repositories and the full repository
list. The list can undercut the README if it is dominated by forks.

Before asking a user to delete anything, separate the forks that are load-bearing
for open-source work from forks that are just noise:

- Keep forks that back an open PR or an active contribution effort.
- A fork created only to try a repo, or a stale fork whose PR already merged,
  can be deleted once the user confirms no work depends on it.

Suggest a deletion window only when the user wants one (for example, "wait N days
for the PR to merge, then delete the fork"). Deleting a fork is permanent and
removes it from the profile, so it needs explicit user authorization per repo.

Pinned repositories are not settable through the GitHub API. When the user wants
pins, give the exact web steps instead:

1. Open `https://github.com/<owner>?tab=repositories`.
2. Click "Customize your pins" on the pinned section.
3. Select the original repositories to show.

## Validators

- The repository name matches the account name and the default branch holds a
  `README.md`.
- The page renders as an unsigned visitor (200 on `https://github.com/<owner>`).
- No invented facts: every project, link, metric and contact channel traces back
  to the user's real account or an explicit user statement.
- Every repository link resolves.
- Merged and in-progress PR claims are separated and accurate.
