---
created: 2026-04-03
updated: 2026-04-03
labels: [metadata, conventions]
description: File structure conventions and frontmatter schema for documentation files.
tags: [frontmatter, yaml, schema]
audience: [agents, humans]
status: active
version: 1.0.0
copyright: "Copyright (c) 2026 Parallel Hours LLC"
license: "PolyForm Noncommercial 1.0.0"

---

# File Structure Conventions

All documentation files in this repository follow a consistent structure.

## Frontmatter Schema

Every `.md` file MUST include YAML frontmatter at the top:

```yaml
---
created: YYYY-MM-DD          # ISO 8601 date when file was created
updated: YYYY-MM-DD          # ISO 8601 date when file was last modified
labels: [label1, label2]     # Categorization tags
description: Brief summary   # One-line description (<100 chars)
tags: [tag1, tag2]           # Searchable tags
audience: [agents, humans]   # Who this doc is for
status: draft|review|active  # Document lifecycle status
version: X.Y.Z               # Semantic version of this doc's content
copyright: "Copyright (c) YYYY Owner Name"  # Legal copyright holder
license: "License Name"      # SPDX name or PolyForm identifier
---
```

## Directory-Specific Frontmatter

Each directory may extend the base schema with additional fields:

### 01-explanation/

```yaml
extends: base
concepts: [concept1, concept2]   # Key concepts covered
prerequisites: [prereq1]         # What reader should know
```

### 02-tutorial/

```yaml
extends: base
duration: 15m                    # Estimated time to complete
prerequisites: [step1, step2]    # Previous steps required
outcomes: [outcome1]             # What reader will achieve
```

### 04-reference/

```yaml
extends: base
applies-to: [component1]         # Components this reference covers
schema-url: https://...          # JSON Schema URL if applicable
```

### 05-plans/

```yaml
extends: base
milestone: v1.0                  # Associated milestone
priority: high|medium|low       # Priority level
owners: [owner1]                 # Responsible individuals
```

## File Naming

- Use kebab-case: `getting-started.md`, `api-reference.md`
- Include step numbers for tutorials: `tutorial-01-setup.md`
- Group related files in subdirectories when > 5 files

## Content Structure

After frontmatter, content should follow:

1. H1 title (matching filename)
2. Brief description paragraph
3. Table of contents (for docs > 200 lines)
4. Body content
5. "See Also" section linking related docs

## Index Files

Each directory MUST have an `index.md` that:

- Lists all files in the directory
- Groups related files logically
- Links to the most important docs first

## Agent Indexing

Agents should extract and use frontmatter for:

- Relevance scoring when searching
- Building knowledge graphs
- Tracking documentation freshness
- Filtering by audience, status, or labels
