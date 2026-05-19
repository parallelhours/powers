---
created: 2026-05-08
updated: 2026-05-08
labels: [troubleshooting, errors]
description: Common errors and their solutions in the parallel-powers framework.
tags: [troubleshooting, errors, faq, debugging]
audience: [developers, operators, agents]
status: draft
version: 0.1.0
---

# Common Errors

## Missing Frontmatter

**Error**: A document is not being indexed or recognized by the agent.
**Solution**: Ensure the file has valid YAML frontmatter between `---` delimiters. See [file structure conventions](../12-metadata/file-structure.md).

## Broken Links

**Error**: A link within agent-docs/ returns 404 or fails to navigate.
**Solution**: Verify the target file exists and the path is correct relative to the source file.

## Stale Metadata

**Error**: Document shows outdated status or version.
**Solution**: Update the `updated`, `status`, and `version` fields in the frontmatter.
