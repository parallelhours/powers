---
created: 2026-06-10
updated: 2026-06-10
labels: [howto, releases, github]
description: Step-by-step guide for creating a GitHub release for parallel-powers.
tags: [howto, release, github, versioning]
audience: [developers, agents]
status: active
version: 1.0.0
copyright: "Copyright (c) 2026 Parallel Hours LLC"
license: "PolyForm Noncommercial 1.0.0"
---

# Create a Release

Releases publish a tagged version of the plugin to GitHub so users can install it via `--plugin-url`.

## Prerequisites

- Tag already exists in git (`git tag -l` to verify)
- GitHub CLI authenticated (`gh auth status`)
- On the `main` branch with the tag pushed to origin

## Steps

### 1. Verify the tag exists remotely

```bash
git tag -l | tail -5
git ls-remote --tags origin | tail -5
```

### 2. Review commits since the last release

```bash
git log v1.X.Y..v1.X.Z --oneline
```

Use this to draft the release notes.

### 3. Create the release

```bash
gh release create <tag> \
  --repo parallelhours/powers \
  --title "<tag>" \
  --notes "$(cat <<'EOF'
## What's Changed

* <bullet per change>

**Full Changelog**: https://github.com/parallelhours/powers/compare/<prev-tag>...<tag>
EOF
)"
```

For a patch fix (e.g. `v1.4.1`), one or two bullets is enough. For minor/major versions, include all meaningful changes.

### 4. Attach the zip asset (if needed)

If users install via `--plugin-url`, the zip must be attached.

**Use an explicit include list** — exclude-based approaches inadvertently bundle `engagements/`, `agent-docs/`, `node_modules`, and other non-plugin directories.

```bash
# Build zip from repo root — include only plugin files
zip -r parallel-powers.zip \
  .claude-plugin \
  .codex-plugin \
  skills \
  hooks \
  .opencode/plugins \
  .opencode/skills \
  index.js \
  package.json \
  LICENSE \
  README.md \
  CLAUDE.md \
  AGENTS.md

gh release upload <tag> parallel-powers.zip \
  --repo parallelhours/powers
```

Expected result: ~70 KB, ~48 files. If the zip is larger than 200 KB, something is wrong — stop and audit with `unzip -l parallel-powers.zip`.

### 5. Verify

```bash
gh release view <tag> --repo parallelhours/powers
```

Check that the title, notes, and any assets look correct.

## Notes

- The GitHub remote is `parallelhours/powers` (not `pmonday/parallel-powers`)
- Releases are not drafts by default — they publish immediately
- Use `--prerelease` flag for release candidates
