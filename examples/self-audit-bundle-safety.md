# Real self-audit: release bundle path escape

Date: 2026-08-13. Repository: `project-publisher`. Scope: local, read-only reproduction followed by a code and test repair.

## Failure

The release bundle builder walked project files and called `read_bytes()` without rejecting symbolic links. A project could therefore contain a file link whose visible path was inside the project while its target was outside it. The generated ZIP contained the target file's bytes.

Minimal reproduction:

```bash
probe="$(mktemp -d)"
mkdir "$probe/project"
printf 'safe\n' > "$probe/project/README.md"
ln -s /etc/hosts "$probe/project/outside.txt"
python skills/project-publisher/scripts/build_release_bundle.py \
  "$probe/project" --output "$probe/release.zip"
```

Before 0.1.2, `outside.txt` was archived. Passing the public-surface gate did not catch the link.

## Repair

- Reject file and directory symlinks before reading them.
- Reject other non-regular filesystem entries.
- Treat Git-candidate symlinks as public-surface blockers.
- Do not follow Markdown or secret-scan symlinks.
- Add regression tests for file and directory links, deterministic archives and excluded local state.

## Verification

```bash
python -m unittest discover -s tests -v
python skills/project-publisher/scripts/review_public_surface.py --self-test
python skills/project-publisher/scripts/check_links.py .
python skills/project-publisher/scripts/check_secrets.py .
```

The repaired builder exits before creating a bundle and identifies the symbolic link without printing the target file contents. This case proves a narrow safety property; it does not prove every project is safe to publish.
