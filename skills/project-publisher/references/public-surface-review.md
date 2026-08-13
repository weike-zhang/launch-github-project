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

The automated review warns when a root README references a hero, banner, cover or masthead only after a long introduction or code block. Review that warning in the rendered page: move the visual into the initial viewport when it carries the identity or promise, or rename and keep it later when it is genuinely section evidence rather than a hero.

It also warns when a centered tagline contains several method words such as audit, check, validate, 检查 or 核对 but no visible user result. This is a narrow signal, not a positioning score. A tagline that passes still needs the name-swap and desire-to-try cold reads below.

Ask five cold-reader questions:

1. Who is this for?
2. What familiar problem, unmet need or intended use should they recognize?
3. What changes for them when they use the project?
4. Which example or evidence supports that change?
5. What should they try first?

Then ask two positioning questions separately from prose quality:

1. What project-specific result appears in the first use rather than only a list of internal steps?
2. Would the main outcome line still fit an unrelated tool after swapping the name? If so, it is too generic.

Translate internal mechanisms into observable consequences. Inspect comparison images as carefully as prose: both sides should use the same user task and show a difference a reader can interpret without decoding feature labels.

Audit every heading, navigation label, CTA, caption and visible image string for purpose. It must surface a reader pain or goal, a result or advantage, evidence, a boundary, or a next step with an already-clear payoff. Reject labels that only narrate motion, such as “try,” “see,” “ask,” “试一下,” “看案例” or “问一次.” A concrete noun does not rescue an empty instruction: “问一次登录流程” still leaves the reader asking why.

After the factual draft and Humanizer pass, cold-read the full page as a new target reader. Mark the job of every public line and revise every line that lacks a job or uses author-only language. Read the complete revised page a second time. Do not treat generated copy, a Humanizer result, a diff review or the first cold read as finished work. For English, ask whether the intended reader would say the example prompt and could repeat each outcome in their own words. Prefer common words, and explain an exact technical term the first time it is needed.

Challenge every image after the hero. If a code block, Markdown table or short paragraph carries the same evidence, remove the image. For quantitative claims, prefer a reproducible chart built from checked-in data over a decorative dashboard. Verify fonts, glyphs, line breaks, axes and units at the rendered README width; source-code review does not catch broken Chinese raster text.

For bilingual material, confirm that the second language was independently written from shared facts rather than mirrored from the first language. In Chinese, read the opening aloud, reject long “不代表……能够……” structures and abstract three-part lists, and verify that public images containing text have a Chinese variant.

Remove:

- `TODO`, `TBD`, placeholder and “replace before launch” instructions;
- internal distribution plans or author-profile drafts;
- AI generation prompts and rejected attempt notes that do not help users verify the shipped artifact;
- openings made only of abstract method claims, badges or install commands;
- natural-sounding but product-blind taglines that name no pain, first result or reason to try;
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
