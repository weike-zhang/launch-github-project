# GitHub Release page

Create a Release page as a decision surface, not a duplicated changelog. A reader should be able to decide whether to install or update without reconstructing the repository history.

## Required content

- Name the observable reason to update in the title and summary.
- List user-visible changes before internal maintenance details.
- Include a copyable install or update command.
- Report verification as exact checks and observed results; do not turn release-integrity checks into product-quality claims.
- State verified compatibility and known limitations separately.
- Name the intended release asset when one exists. Verify GitHub's SHA-256 digest after upload.

Start from `assets/release/release-page.json`, then use the structured spec with `scripts/generate_release_page.py` so required sections and version alignment are deterministic. Keep the generated Markdown in `release/vX.Y.Z.md`; it can be passed to `gh release create --notes-file` only after the remote gate is authorized.

## Remote-state gate

Compare these as separate surfaces before publishing:

1. local `HEAD` and version metadata;
2. remote default branch;
3. any open release PR;
4. latest GitHub Release tag, notes and downloadable asset.

An open PR is uploaded work, not a published version. A tag named `vX.Y.Z` is inconsistent when the tagged manifest still reports another version. Do not create the Release until the intended commit is on the chosen release branch and all named checks have passed there.

After creation, open the Release URL as an unsigned visitor and verify the title, notes, links, asset name, digest and installation command. Keep a missing custom social preview separate from Release readiness; it is repository metadata, not a Release asset.
