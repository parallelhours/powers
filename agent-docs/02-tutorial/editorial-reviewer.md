---
created: 2026-05-19
updated: 2026-05-19
labels: [tutorial, editorial-review, ai-assisted, content-quality]
description: How and why to use the editorial-reviewer skill — an AI-powered content review that catches inclusive language issues, performs sentiment analysis, and rewrites flagged content to a target tone.
tags: [tutorial, editorial-reviewer, inclusive-language, sentiment, ai-assisted, content-quality]
audience: [users, humans]
status: published
version: 1.0.0
---

# The Editorial Review I Didn't Know I Needed

Many years ago I went on an authoring spree and created 3 technical books and many, many
published articles that went into now-defunct magazines like "Java Report". I still
remember that first editor's review with my co-authors James Carey and Mary Dangler,
it was like getting hit with a bat. Our humor was wiped out — which, as engineers,
we took personally — our grammar was off, and entire paragraphs were wiped out.

I had thought I was a great writer, but I was an engineer who could write — just not
well enough to publish without a lot of help. It takes a team to write books and content.

My career since then is mostly under the cover of large companies with writers that
bring out an engineer's best. But now, as an independent, I can't afford to hire
Kristi — the editor who used to make my work readable — on my own dime.

But I also know most of us have gaps we don't see.
We review for correctness. We spell-check. We run linters.
But most of us have no one in our process whose job is to ask: *who does this accidentally exclude?* Not just the slur you'd catch immediately — but the `simply` that implies the reader is slow if they're struggling, the example that assumes everyone has a credit card, the error message drafted at 11pm that reads like the author is annoyed at you.

---

## Enter Emery

I created an editorial reviewer persona named Emery (they/them, 10+ years experience) whose mandate is to catch what automated checks miss: phrasing that alienates, cultural assumptions that don't travel, examples drawn from too narrow a pool, and language that accidentally excludes. Their goal is communication that works for a broad audience without calling attention to itself — a reader should find the content clear, accurate, and respectful — without it calling attention to itself.

But a persona alone isn't enough. A persona gives you a point of view. What makes review *systematic* and *actionable* is a skill — an encoded process that Emery runs every time, on any content, without drifting.

---

## The Skill

The editorial-reviewer skill wires Emery's judgment into a repeatable six-dimension review: inclusive language, clarity and precision, tone consistency, assumption auditing, example diversity, and omission detection. You invoke it against any target — a file, a directory, a URL, raw text, or a freeform description of what to look for:

```
/parallel-powers:editorial-reviewer agent-docs/
/parallel-powers:editorial-reviewer src/cli/messages.ts
/parallel-powers:editorial-reviewer "error message: 'Invalid input, dummy.'"
/parallel-powers:editorial-reviewer README.md --to empathetic
```

Then two things happen that most people don't expect.

**First: sentiment and emotion analysis.** Emery doesn't just flag language — it reads the emotional profile of your content. Overall sentiment (positive / negative / neutral / mixed, scored −1.0 to +1.0). Primary emotions detected, with quoted evidence. Emotional intensity. And if the content has a narrative arc, how the emotional register shifts across it. Your installation guide might open with confidence, dip into frustration by step 3, and never recover. You won't notice that until someone names it.

**Second: targeted rewrites.** Emery doesn't leave you with a list of problems. For every flagged issue, it generates a structured recommendation:

```
── Inclusive Language — "he can configure the settings"
- Current effect: assumes a male reader; excludes by default
- Target effect: neutral, accurate, broadly applicable
- Suggested rewrite: "they can configure the settings"
- Rationale: singular they is standard; no meaning is lost
```

Recommendations are prioritized by severity:
- 🔴 **HIGH** — language that could genuinely alienate or harm
- 🟡 **MEDIUM** — clarity and accessibility gaps
- 🟢 **LOW** — stylistic polish

You can apply them selectively or ask Emery to rewrite toward a specific tone: `empathetic`, `assertive`, `conversational`, `formal`, or any description you provide.

---

## What It Actually Catches

The things Emery surfaces aren't obvious until they're named:

- An ableist idiom buried in an error message (`"blind spot"`, `"crippled by"`)
- `simply` and `obviously` in documentation — hedge words that quietly tell struggling readers they're the problem
- A tutorial scenario where every example user has a Western name and a credit card
- A docs section written entirely in passive voice that makes it impossible to tell who does what
- A missing caveat: "works on macOS" without mentioning what happens on Linux

None of these would fail a lint check. All of them affect real readers.

---

## Get It

The skill and persona are open and installable as part of the parallel-powers plugin for Claude Code. You'll need [Claude Code](https://claude.ai/code) (Anthropic's CLI) and the parallel-powers plugin loaded with:

```
claude --plugin-dir /path/to/parallel-powers
```

Then grab the files:

- [Editorial Reviewer Skill](https://github.com/parallelhours/powers/blob/main/skills/editorial-reviewer/SKILL.md) — the full encoded process
- [Emery — Editorial Reviewer Persona](https://github.com/parallelhours/powers/blob/main/agent-docs/13-personas/editorial-reviewer.md) — the point of view behind the process

The persona tells Emery *what to care about*. The skill tells Emery *how to work*. You need both.
