---
title: Tutorial — Good Prompting
summary: Learn what goes into a good prompt, and how this project's docs already cover most of it.
date: 2026-05-12
created: 2026-05-12
updated: 2026-05-12
labels: [tutorial, prompting, ai]
description: Learn what goes into a good prompt, and how this project's docs already cover most of it.
tags: [tutorial, prompting, costar, prompt-framework, diataxis]
audience: [users, agents]
status: published
version: 0.1.0
extends: base
duration: 15m
prerequisites: []
outcomes: [understand-costar, use-prompt-framework, leverage-docs-for-prompting]
copyright: "Copyright (c) 2026 Parallel Hours LLC"
license: "PolyForm Noncommercial 1.0.0"

---

# Tutorial: Good Prompting

The single highest-leverage thing you can do when working with AI agents is
write a good prompt. This tutorial covers what goes into one, a simple
framework to remember the parts, and — most importantly — how this project's
documentation already gives you most of those parts for free.

## What Makes a Good Prompt?

Vague prompts produce vague results. A well-structured prompt gives the AI
clear instructions about what to do, how to do it, who it's for, and how to
verify success.

The industry-standard framework for this is **CO-STAR**, developed by data
scientist Sheila Teo (winner of Singapore's GPT-4 Prompt Engineering
competition). It has six components:

| Letter | Component | What It Defines |
|--------|-----------|-----------------|
| **C** | **Context** | Background, situation, constraints |
| **O** | **Objective** | The specific task or goal |
| **S** | **Style** | Structural approach (technical, conversational, academic) |
| **T** | **Tone** | Emotional quality (formal, urgent, encouraging) |
| **A** | **Audience** | Who will read or use the output |
| **R** | **Response** | Exact format, structure, length of the output |

A variant called **CO-STAR+** adds a seventh component:

| + | **E** | **Examples** | Few-shot samples showing what you want |

### Grounding

**Grounding** anchors LLM outputs to verifiable, external data — documents,
codebases, examples, or specific context — rather than relying solely on
training data. It prevents hallucinations, improves accuracy, and ensures
responses are relevant and actionable.

In CO-STAR+, the **E** (Examples) component is the primary grounding technique:
few-shot samples show the model the exact format, style, and reasoning you
want. But **C** (Context) and **O** (Objective) also ground the response by
narrowing scope to a specific situation and goal.

In the PROMPT framework, grounding lives in **M** (Material) — providing
trusted source material (documents, API specs, constraints) — and **T** (Test)
— concrete verification criteria to validate the output against reality. A
well-grounded prompt combines context, examples, and testable expectations so
the model acts as a precise, data-driven assistant rather than a creative
storyteller.

## A Catchier Framework: P.R.O.M.P.T.

CO-STAR is thorough, but six letters are hard to remember in the heat of the
moment. Here's a self-referential mnemonic:

| Letter | Stands For | Question to Ask Yourself |
|--------|------------|--------------------------|
| **P** | **Persona** | Who is the AI acting as? (senior engineer, tutor, editor) |
| **R** | **Request** | What exactly do you want done? (the objective) |
| **O** | **Outline** | How should the output look? (format, structure, length) |
| **M** | **Material** | What context does the AI need? (background, constraints, references) |
| **P** | **Preference** | What's the style, tone, and audience level? |
| **T** | **Test** | How will you (or the AI) verify success? (examples, checks, tests) |

**P.R.O.M.P.T.** covers the same ground as CO-STAR+ but uses a single word
you're already thinking about when you sit down to write one.

## How This Project's Docs Already Fill In Most of P.R.O.M.P.T.

Here's the key insight: good prompting is mostly about transferring context
from your head to the AI. In this project, that context already lives in
structured documentation. Your prompt can be much shorter because the
scaffolding is already baked in.

This project uses the [Diátaxis framework](https://diataxis.fr/) — four
documentation modes (tutorial, how-to, explanation, reference), plus
supplementary directories for agents, personas, and metadata. Each one maps
directly to a P.R.O.M.P.T. component:

| PROMPT | Filled by these docs | What it gives the AI |
|--------|---------------------|---------------------|
| **P**ersona | `CLAUDE.md`, `docs/11-agents/`, `docs/13-personas/` | Role, conventions, coding style, user archetypes |
| **M**aterial | `docs/01-explanation/`, `docs/04-reference/`, `docs/12-metadata/` | Architecture, API specs, project metadata |
| **P**reference (Audience) | `docs/13-personas/` | Who the output is for — developer, PM, operator, evaluator |

**That means your prompt shrinks from six items to three:**

| Remaining | Why you still need to provide it |
|-----------|----------------------------------|
| **R**equest | The AI can't read your mind — tell it what to do |
| **O**utline | Every task has a different desired output format |
| **T**est | This is the single highest-leverage thing you can provide |

<div style="margin: 2rem 0; overflow-x: auto;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 610" role="img" aria-label="Diagram showing the six PROMPT framework components (Persona, Request, Outline, Material, Preference, Test) split between those covered by project documentation and those the user writes in their prompt" style="max-width: 100%; height: auto; display: block; margin: 0 auto; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="115%" height="115%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.06"/>
    </filter>
  </defs>
  <text x="420" y="36" text-anchor="middle" font-size="23" font-weight="700" fill="#0f172a" letter-spacing="-0.3">The PROMPT Framework &mdash; Lightened by Documentation</text>
  <text x="420" y="60" text-anchor="middle" font-size="14" fill="#64748b">Your project&rsquo;s Di&aacute;taxis documentation covers the heavy context. You only write the task-specific details.</text>
  <g transform="translate(250, 78)">
    <rect x="0" y="0" width="340" height="28" rx="14" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
    <circle cx="16" cy="14" r="5" fill="#4f46e5"/>
    <text x="26" y="18" font-size="12" fill="#334155" font-weight="500">Covered by docs</text>
    <circle cx="175" cy="14" r="5" fill="#f59e0b"/>
    <text x="185" y="18" font-size="12" fill="#334155" font-weight="500">You provide in your prompt</text>
  </g>
  <g transform="translate(35, 125)">
    <rect width="240" height="210" rx="14" fill="#fff" filter="url(#shadow)"/>
    <circle cx="120" cy="72" r="40" fill="none" stroke="#f1f5f9" stroke-width="12"/>
    <circle cx="120" cy="72" r="40" fill="none" stroke="#4f46e5" stroke-width="12" stroke-dasharray="251.327" stroke-dashoffset="37.699" transform="rotate(-90 120 72)"/>
    <text x="120" y="80" text-anchor="middle" font-size="28" font-weight="700" fill="#0f172a">P</text>
    <text x="120" y="140" text-anchor="middle" font-size="14" font-weight="600" fill="#374151">Persona</text>
    <rect x="65" y="158" width="110" height="26" rx="13" fill="#eef2ff"/>
    <text x="120" y="175" text-anchor="middle" font-size="11" font-weight="600" fill="#4f46e5">Covered by docs</text>
  </g>
  <g transform="translate(300, 125)">
    <rect width="240" height="210" rx="14" fill="#fff" filter="url(#shadow)"/>
    <circle cx="120" cy="72" r="40" fill="none" stroke="#f1f5f9" stroke-width="12"/>
    <text x="120" y="80" text-anchor="middle" font-size="28" font-weight="700" fill="#0f172a">R</text>
    <text x="120" y="140" text-anchor="middle" font-size="14" font-weight="600" fill="#374151">Request</text>
    <rect x="55" y="158" width="130" height="26" rx="13" fill="#fffbeb"/>
    <text x="120" y="175" text-anchor="middle" font-size="11" font-weight="600" fill="#d97706">You write this</text>
  </g>
  <g transform="translate(565, 125)">
    <rect width="240" height="210" rx="14" fill="#fff" filter="url(#shadow)"/>
    <circle cx="120" cy="72" r="40" fill="none" stroke="#f1f5f9" stroke-width="12"/>
    <text x="120" y="80" text-anchor="middle" font-size="28" font-weight="700" fill="#0f172a">O</text>
    <text x="120" y="140" text-anchor="middle" font-size="14" font-weight="600" fill="#374151">Outline</text>
    <rect x="55" y="158" width="130" height="26" rx="13" fill="#fffbeb"/>
    <text x="120" y="175" text-anchor="middle" font-size="11" font-weight="600" fill="#d97706">You write this</text>
  </g>
  <g transform="translate(35, 365)">
    <rect width="240" height="210" rx="14" fill="#fff" filter="url(#shadow)"/>
    <circle cx="120" cy="72" r="40" fill="none" stroke="#f1f5f9" stroke-width="12"/>
    <circle cx="120" cy="72" r="40" fill="none" stroke="#4f46e5" stroke-width="12" stroke-dasharray="251.327" stroke-dashoffset="50.265" transform="rotate(-90 120 72)"/>
    <text x="120" y="80" text-anchor="middle" font-size="28" font-weight="700" fill="#0f172a">M</text>
    <text x="120" y="140" text-anchor="middle" font-size="14" font-weight="600" fill="#374151">Material</text>
    <rect x="65" y="158" width="110" height="26" rx="13" fill="#eef2ff"/>
    <text x="120" y="175" text-anchor="middle" font-size="11" font-weight="600" fill="#4f46e5">Covered by docs</text>
  </g>
  <g transform="translate(300, 365)">
    <rect width="240" height="210" rx="14" fill="#fff" filter="url(#shadow)"/>
    <circle cx="120" cy="72" r="40" fill="none" stroke="#f1f5f9" stroke-width="12"/>
    <circle cx="120" cy="72" r="40" fill="none" stroke="#4f46e5" stroke-width="12" stroke-dasharray="251.327" stroke-dashoffset="62.832" transform="rotate(-90 120 72)"/>
    <text x="120" y="80" text-anchor="middle" font-size="28" font-weight="700" fill="#0f172a">P</text>
    <text x="120" y="140" text-anchor="middle" font-size="14" font-weight="600" fill="#374151">Preference</text>
    <rect x="65" y="158" width="110" height="26" rx="13" fill="#eef2ff"/>
    <text x="120" y="175" text-anchor="middle" font-size="11" font-weight="600" fill="#4f46e5">Covered by docs</text>
  </g>
  <g transform="translate(565, 365)">
    <rect width="240" height="210" rx="14" fill="#fff" filter="url(#shadow)"/>
    <circle cx="120" cy="72" r="40" fill="none" stroke="#f1f5f9" stroke-width="12"/>
    <circle cx="120" cy="72" r="40" fill="none" stroke="#4f46e5" stroke-width="12" stroke-dasharray="251.327" stroke-dashoffset="201.062" transform="rotate(-90 120 72)"/>
    <text x="120" y="80" text-anchor="middle" font-size="28" font-weight="700" fill="#0f172a">T</text>
    <text x="120" y="140" text-anchor="middle" font-size="14" font-weight="600" fill="#374151">Test</text>
    <rect x="55" y="158" width="130" height="26" rx="13" fill="#fffbeb"/>
    <text x="120" y="175" text-anchor="middle" font-size="11" font-weight="600" fill="#d97706">You write this</text>
  </g>
  <text x="420" y="600" text-anchor="middle" font-size="13" fill="#94a3b8">Persona + Material + Preference are covered by your project docs &rarr; your prompt is just Request + Outline + Test</text>
</svg>
</div>

Let's see this in action.

## Before and After

### Before (no docs, vague prompt):

> "Add a timer endpoint to the API."

### After (leveraging docs, using P.R.O.M.P.T.):

> **R**equest: Add a `POST /api/timers/start` endpoint.
>
> **O**utline: DRF viewset + serializer + test. Follow existing patterns.
>
> **T**est: `pytest` — write a test that starts a timer and asserts the response.
> Run `pytest -k test_start_timer` to verify.
>
> *(The AI already knows from CLAUDE.md + docs: Django, DRF serializers,
> rich models/thin views, `services.py` pattern, auth required, pytest
> fixtures. Your prompt doesn't need to repeat any of that.)*

### Even shorter — after you've built trust:

Once you and the AI have a shared understanding of the conventions, you can
drop the Outline too:

> "Add a `POST /api/timers/start` endpoint. Write a test and verify it passes."

The AI pulls Persona from `CLAUDE.md`, Material from the codebase and docs,
and Preference from the project's existing patterns. You only supply the
Request and a Test to verify.

## Putting It All Together

### When writing a prompt for this project:

1. **Check what the docs already cover.** Read `CLAUDE.md`, skim the relevant
   `docs/` section — you'll often find you can skip half the prompt.
2. **State the Request clearly.** This is the one thing the AI cannot guess.
3. **Specify the Outline** if the output format isn't obvious from context.
4. **Always include a Test.** A command to run, an assertion to check, a
   screenshot to compare. This is the single highest-leverage practice
   across all AI coding tools.

### When writing a prompt for any project:

Run through P.R.O.M.P.T.:

1. **P**ersona — role for the AI
2. **R**equest — what to do
3. **O**utline — output format
4. **M**aterial — context and constraints
5. **P**reference — style, tone, audience
6. **T**est — verification criteria

Skip any component the project's docs already provide. Over time, you'll
develop intuition for what each project needs.

## References

- Teo, S. (2023). *How I Won Singapore's GPT-4 Prompt Engineering Competition*. Towards Data Science.
  [https://towardsdatascience.com/how-i-won-singapores-gpt-4-prompt-engineering-competition-34c195a93d41](https://towardsdatascience.com/how-i-won-singapores-gpt-4-prompt-engineering-competition-34c195a93d41/)
  — Original article introducing the CO-STAR framework, developed by GovTech Singapore's Data Science & AI team.
- *Diátaxis: A systematic approach to technical documentation authoring*.
  [https://diataxis.fr/](https://diataxis.fr/)

## Next Steps

- [How-to: Write Effective Prompts](../03-howto/effective-prompts.md)
- Read `CLAUDE.md` to see what conventions are already set for this project
- Browse `docs/13-personas/` to understand your audience archetypes
- Browse `docs/12-metadata/` for project-level context you can reference
- [Anthropic's Prompting Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- **Create a Prompt Notebook** — Generate a printable Kindle Scribe notebook template for CO-STAR or PROMPT using the open-source [Kindle Scribe Notebook Generator](https://github.com/parallelhours/kindle-scribe-generator).

---

*Written by **Paul B. Monday** ([pmonday@parallelhours.io](mailto:pmonday@parallelhours.io)) — published at [parallelhours.io](https://parallelhours.io). Created with [OpenCode Zen](https://opencode.ai) (Big Pickle model).*  
© 2026 Paul B. Monday
