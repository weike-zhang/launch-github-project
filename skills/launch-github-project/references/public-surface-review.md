# Public-surface review

Run this review after release materials are drafted and again immediately before any public push. A clean secret scan is necessary but not sufficient.

## 1. Inventory exactly what the public will receive

- Inspect the staged diff, archive listing and remote default branch separately.
- Detect nested repositories, duplicated project folders, editor workspaces, caches, `.DS_Store`, build debris and machine-specific paths.
- Keep maintainer planning notes, replacement instructions, launch-copy drafts and private evaluation runs outside the public repository unless they intentionally help contributors.
- Treat author-profile setup drafts, planned username changes and repository-specific onboarding notes as maintainer material, not a reusable public guide.

Run:

```bash
python3 scripts/review_public_surface.py <project-root> --json
```

Resolve every blocker. Review warnings one by one; do not dismiss them in bulk.

## 2. Confirm rights before displaying assets

Inventory images, fonts, icons, screenshots, datasets, copied text and model-edited derivatives. Record one state for each material asset:

- confirmed for the intended public use;
- replace before publication;
- keep local only.

Do not publish an asset while its own notice says permission is pending. A public notice should state the final provenance and reuse terms, not expose rejected generation prompts or unresolved internal discussion.

## 3. Separate product evidence from release plumbing

- A fixture-count or schema check is release integrity, not model or product quality.
- Do not report a percentage when the script only checks that files and fields exist.
- Link every behavior score to the method and complete sanitized raw outputs.
- Label a single run as a pilot, not a benchmark.
- Keep limitations beside the result rather than in an unrelated document.

## 4. Review public copy as an unsigned visitor

The first screen should let a target reader recognize their situation or goal, understand the user-visible outcome, inspect one concrete proof and find the shortest valid start action. A checklist-complete page still fails when these answers require understanding the project's protocol, architecture or maintainer vocabulary first.

Ask five cold-reader questions:

1. Who is this for?
2. What familiar problem, unmet need or intended use should they recognize?
3. What changes for them when they use the project?
4. Which example or evidence supports that change?
5. What should they try first?

Translate internal mechanisms into observable consequences. Inspect comparison images as carefully as prose: both sides should use the same user task and show a difference a reader can interpret without decoding feature labels.

For bilingual material, confirm that the second language was independently written from shared facts rather than mirrored from the first language. In Chinese, read the opening aloud, reject long “不代表……能够……” structures and abstract three-part lists, and verify that public images containing text have a Chinese variant.

Remove:

- `TODO`, `TBD`, placeholder and “replace before launch” instructions;
- internal distribution plans or author-profile drafts;
- AI generation prompts and rejected attempt notes that do not help users verify the shipped artifact;
- openings made only of abstract method claims, badges or install commands;
- feature labels that describe the implementation but not what the reader can do;
- unsupported compatibility, adoption, learning or performance claims.

## 5. Review Git history and identity

- Inspect recent commit messages, authors, contributors, tags and branches.
- Confirm that every public author identity is intended.
- Treat generic commits such as `v1`, accidental nested clones and unrelated repository history as a decision, not harmless background.
- Rewrite published history only with explicit authorization and after preserving a recovery reference.

## 6. Complete the remote surface

Check repository description, Topics, license detection, social preview, default branch, Release, downloadable assets, Issues and security policy. After pushing, open the public URL without relying on an authenticated maintainer view and verify images, links, install commands and the Release asset.

Compare the version on the remote default branch, any open release PR and the latest Release tag. Report drift explicitly: an open PR is uploaded but not published, and a tag does not repair stale version metadata inside the tagged files.

## Gate result

Report four separate outcomes:

1. automated blockers resolved;
2. warnings reviewed;
3. manual rights, evidence and identity decisions confirmed;
4. unsigned remote-page verification observed.

Do not call the project publicly ready when only the push succeeded.
