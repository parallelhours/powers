# User Personas

This document describes the target users of this project.

## Personas at a Glance

| Persona | Role | Experience |
|---------|------|------------|
| Wei | Full-stack Developer | 5+ years |
| Jordan | DevOps Engineer | 3+ years |
| Sam | Tech Lead / Evaluator | 10+ years |
| Morgan | Project Manager | 7+ years |
| Yuki | Technical Writer | 4+ years |
| Taylor | Product Marketing Manager | 8+ years |
| Amara | Solutions Architect | 12+ years |
| Emery | Editorial Reviewer | 10+ years |
| Hikaru | Junior Developer | 1-2 years |

---

## Detailed Personas

### Persona: The Developer

**Name**: Wei  
**Role**: Full-stack developer  
**Experience**: 5+ years  
**Pronouns**: they/them

### Goals
- Build and ship features quickly
- Understand codebase structure
- Debug issues efficiently

### Pain Points
- Poor documentation
- Unclear error messages
- Missing examples

### How We Help
- Clear [tutorials](../02-tutorial/) and [how-to guides](../03-howto/)
- Comprehensive [reference docs](../04-reference/)
- Detailed [troubleshooting](../08-troubleshooting/)

---

### Persona: The Operator

**Name**: Jordan  
**Role**: DevOps engineer  
**Experience**: 3+ years  
**Pronouns**: they/them

### Goals
- Deploy reliably
- Monitor system health
- Respond to incidents

### Pain Points
- Missing deployment docs
- Unclear rollback procedures
- No runbooks

### How We Help
- Detailed [runbooks](../07-runbooks/)
- Clear [environment setup](../06-environment/)
- Incident response procedures

---

### Persona: The Evaluator

**Name**: Sam  
**Role**: Tech lead  
**Experience**: 10+ years  
**Pronouns**: they/them

### Goals
- Evaluate fit for team
- Estimate integration effort
- Assess quality

### Pain Points
- No high-level overview
- Missing architecture docs
- No changelog

### How We Help
- Clear [README](../00-readme/)
- [Architecture documentation](../01-explanation/)
- [Changelog](../09-changelog/) for history

---

### Persona: The Project Manager

**Name**: Morgan  
**Role**: Project manager  
**Experience**: 7+ years  
**Pronouns**: they/them

### Goals
- Track project progress and milestones
- Coordinate sprints and releases
- Identify blockers early
- Communicate status to stakeholders

### Pain Points
- Outdated roadmaps
- No clear sprint tracking
- Missing release timelines
- Hard to find decision history

### How We Help
- Clear [roadmap](../05-plans/roadmap.md) with milestones
- [Sprint backlog](../05-plans/sprint-backlog.md) for current work
- [Design decisions](../01-explanation/decisions.md) for rationale
- [Changelog](../09-changelog/) for release history

---

### Persona: The Docs Author

**Name**: Yuki  
**Role**: Technical writer / documentation lead  
**Experience**: 4+ years  
**Pronouns**: they/them

### Goals
- Create clear, consistent documentation
- Produce customer-facing materials
- Maintain glossary and terminology
- Enable self-service for users

### Pain Points
- No established conventions
- Inconsistent formatting across docs
- Hard to find source of truth
- Diagrams not rendering properly

### How We Help
- [File structure conventions](../12-metadata/file-structure.md) for consistency
- [Diagram guidelines](../12-metadata/diagrams.md) for visuals
- [Glossary](../10-glossary/) for terminology
- [How-to guides](../03-howto/) template and structure

---

### Persona: The Product Marketing Manager

**Name**: Taylor  
**Role**: Product marketing manager  
**Experience**: 8+ years  
**Pronouns**: they/them

### Goals
- Define and communicate product vision and strategy
- Author clear, actionable product requirements documents (PRDs)
- Prioritize features based on customer impact and business value
- Maintain a continuous feedback loop with all customer segments
- Ensure shipped features solve the original problem

### Pain Points
- Requirements lack context — "what" without "why"
- No standard PRD template or acceptance framework
- Hard to trace shipped features back to original customer needs
- Feature prioritization feels arbitrary
- No mechanism to validate post-ship whether requirements were met
- Customer feedback (including churn signals) has no structured home

### How We Help
- [Plans and roadmaps](../05-plans/) for product definition and strategy
- [Architecture decisions](../01-explanation/decisions.md) that capture rationale
- [Changelog](../09-changelog/) to close the loop between definition and delivery
- [Glossary](../10-glossary/) for consistent terminology across PRDs
- [Personas](../13-personas/) that model customer needs and feed requirements
- [Issue labels](../04-reference/issue-labels.md) for structured prioritization metadata

---

### Persona: The Architect

**Name**: Amara  
**Role**: Solutions architect / technical architect  
**Experience**: 12+ years  
**Pronouns**: they/them

### Goals
- Define system architecture
- Make high-level design decisions
- Ensure technical coherence
- Evaluate technology choices

### Pain Points
- Low-level implementation details cluttering architecture docs
- No clear separation between high-level and detailed design
- Missing rationale for decisions
- Hard to visualize component relationships

### How We Help
- High-level [architecture overview](../01-explanation/architecture.md)
- [Design decision records](../01-explanation/decisions.md) with rationale
- [Diagram guidelines](../12-metadata/diagrams.md) for component/runtime diagrams
- Reference docs kept separate from explanation docs

---

### Persona: The Editorial Reviewer

**Name**: Emery  
**Role**: Editorial reviewer  
**Experience**: 10+ years  
**Pronouns**: they/them

### Goals
- Catch language that assumes a single cultural, gender, or socioeconomic perspective
- Replace stereotyped or outdated framing with precise, neutral alternatives
- Ensure examples, names, and scenarios reflect a range of backgrounds
- Apply the same standard to technical content (CLI, error messages, docs) as to marketing copy

### Pain Points
- Good editorial work is invisible — when it succeeds, no one notices
- Hard to maintain consistent standards across different content types
- Small mistakes on names, pronouns, or cultural references carry outsized impact
- Balancing broad accessibility against concise technical communication

### How We Help
- Every piece of content benefits from an editorial review pass — ask Emery
- The [Glossary](../10-glossary/) maintains terminology choices that serve diverse audiences

---

### Persona: The Junior Developer

**Name**: Hikaru  
**Role**: Junior developer / career switcher  
**Experience**: 1-2 years  
**Pronouns**: they/them

### Goals
- Get a development environment running without getting stuck on tooling setup
- Understand the project structure and conventions
- Complete tasks with clear instructions and examples
- Build confidence through small, achievable wins
- Learn best practices while contributing real value

### Pain Points
- Documentation that assumes prior knowledge of tools or conventions
- Tasks that require hidden context (e.g., "run the tests" when they don't know the framework)
- Imposter syndrome — afraid to ask what seems like a "dumb" question
- No clear path from "I don't know this" to "I can do this"

### How We Help
- Step-by-step [tutorials](../02-tutorial/) for setup and first contributions
- [Troubleshooting guide](../08-troubleshooting/) for common issues
- [Glossary](../10-glossary/) defining every technical term
- Concrete examples in [how-to guides](../03-howto/)
