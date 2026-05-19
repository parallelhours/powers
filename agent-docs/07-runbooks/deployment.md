---
created: 2026-05-13
updated: 2026-05-13
labels: [runbooks, deployment]
description: Deployment procedures for the parallel-powers documentation and MCP framework.
tags: [deployment, release, runbook]
audience: [operators, agents]
status: draft
version: 0.1.0
---

# Runbook: Deployment

## Pre-deployment Checklist

- [ ] All documentation renders correctly
- [ ] MCP install.json files are valid JSON
- [ ] All links between docs are valid
- [ ] Frontmatter on all new/changed files is valid
- [ ] CHANGELOG updated for the release

## Deployment Steps

### 1. Prepare Release

```bash
git checkout main
git pull origin main
```

### 2. Run Pre-deployment Checks

```bash
# Validate all install.json files
python mcps/installer.py list

# Verify documentation structure
ls agent-docs/*/index.md
```

### 3. Tag Release

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

## Rollback

```bash
git revert HEAD
git push origin main
```
