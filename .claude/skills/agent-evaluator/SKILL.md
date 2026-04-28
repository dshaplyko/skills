---
name: agent-evaluator
description: Evaluate one or more AI agent specifications against the Agent Maturity Model (L0–L3, 39 practices across 9 categories) and produce a styled HTML maturity assessment report. Use this skill whenever the user asks to assess, score, grade, audit, review the maturity of, or generate a maturity report for an AI agent, agent suite, prompt, ELITEA pipeline, sub-agent folder, or any agentic system — even if they don't say the word "maturity". Trigger on phrases like "evaluate this agent", "score these agents", "how mature is X", "audit the agent suite in folder Y", "rate this prompt against best practices", "is this L1 or L2", or when the user points at a folder of `*_agent.md` / `*.yml` files and asks for an assessment. Always ask the user clarifying questions about platform-side concerns (token tracking, eval suite, observability, audit logs) before generating the final report — those concerns must be confirmed, not assumed.
---

# Agent Evaluator

Score AI agent specifications against the **Agent Maturity Model** (Ihar Bylitski, Feb 2026) and emit a styled HTML report following the project's house template.

The model has four cumulative levels — **L0 Beginner**, **L1 Foundational**, **L2 Advanced**, **L3 Autonomous** — and 39 practices spread across 9 categories. The full requirements live in `references/maturity_model_requirements.md`; the rubric for assigning a level lives in `references/scoring_rubric.md`; the report skeleton lives in `references/report_template.md` and a worked example in `references/example_report.html`.

## Why this skill exists

Without a structured rubric, agent reviews drift into vibes ("looks pretty good"). This skill enforces three things every review needs to be useful:

1. **A consistent scale** — every agent gets one of L0/L1/L2/L3, anchored to the same 39 practices, so reports across clients are comparable.
2. **Evidence per claim** — each strength and gap must point to a specific instruction in the agent's spec. Aspirational scoring is worse than no scoring.
3. **Honest N/A handling** — many practices live on the agentic platform (token cost, telemetry, eval harness), not in the agent prompt. The skill explicitly asks the user about those before scoring, so platform-side concerns aren't mis-marked as gaps.

## Workflow

Follow these phases in order. Don't skip the clarifying-questions phase — it is the difference between a defensible report and a wrong one.

### Phase 1 — Locate the inputs

Detect how the user supplied the agents:

- **Path mode** (most common in this repo) — the user names a folder (e.g. `SLB/agents/`, `philips/ba_agent/`) or a list of files. Use Glob / Read / Bash `ls` to enumerate. Look for `*.md` (prompt bodies), `*_agent.yml` / `master.yml` (pipelines), and any `agents/` subfolder. Read every file fully — partial reads cause missed gaps.
- **Pasted mode** — the user pastes the agent definition inline. Treat the pasted blocks as the spec and skip filesystem walking.
- **Mixed** — a mix of paths and pasted snippets. Read paths, then append pasted content as additional agents.

Present the list of agents you found back to the user in one short message ("Found 6 agents in `SLB/agents/`: orchestrator, req_creator, req_publisher, req_validator, us_stories_creator, artifact_cleaner — proceeding."). This catches scope mistakes before the slow steps.

### Phase 2 — Read the rubric and requirements

Before scoring, load:

- `references/maturity_model_requirements.md` — the 39 practices, organised by category, each tagged with the minimum level it requires.
- `references/scoring_rubric.md` — how to translate spec content into a level, what counts as a strength vs a gap, how to roll up a suite-level score.

Read both fully on each invocation. They are short and the cost of skipping them is mis-scoring.

### Phase 3 — Ask clarifying questions

This phase is non-negotiable. Many practices in the maturity model live on the agentic platform (EliteA, LangSmith, in-house) or in ops processes the user runs off-platform. If you score those from the agent spec alone, you will mark real strengths as gaps.

Read `references/clarifying_questions.md` for the full list, but at minimum confirm these before generating the report:

- **Suite name, target path, author, report date** — needed for the header.
- **Token economics & cost monitoring** (Cat. 1) — is per-run cost tracked by the platform? Caching enabled? Budget alerts?
- **Evaluation framework** (Cat. 3) — is there an eval suite? Where? How rigorous?
- **Observability** (Cat. 8) — does the platform emit traces, latency, token telemetry?
- **Compliance bits of safety** (Cat. 9) — named-user runs, audit retention, red-team cadence.
- **Anchor agents** — if the suite is large, which agents are load-bearing? (Drives the executive-summary rollup.)
- **Out-of-scope categories** — anything the user explicitly wants marked N/A.

Use the `AskUserQuestion` tool. Group related items into one prompt. Prefill the most likely answer as the first option. Do not ask questions whose answers the user already volunteered earlier in the conversation.

### Phase 4 — Score each agent

For each agent file, work through the rubric:

1. **Read the spec end to end.** Note every section header, every numbered capability, every rule.
2. **Tag strengths** — concrete instructions that satisfy a specific practice. Example: "Mandatory post-write verification (re-reads created item)" → Cat. 4 hallucination prevention + Cat. 9 safety.
3. **Tag gaps** — practices the rubric calls for at the level you're considering, that are *absent* from the spec. Don't infer presence.
4. **Pick a level** — the highest level whose criteria the agent fully meets. If it sits between (most of L2 satisfied, one or two L2 items missing), record `L1+` rather than over-claim L2. The honesty makes the recommendations land.
5. **Quote evidence in your notes** — when you write a strength bullet, you should be able to point to the exact line in the spec. Keep these notes alongside the scoring; they are the raw material for the report.

### Phase 5 — Roll up to a suite-level score

The suite level is **not the average** — it follows the anchor-agent rule (see `scoring_rubric.md`). State the rollup logic explicitly in the executive summary: "anchor agents X, Y at L2; supporting agents at L1; suite sits between L1 and L2".

### Phase 6 — Generate the HTML report

Output a single self-contained HTML file. **Always** use the styling from `references/example_report.html` — same `<style>` block, same level badges (`b-l0`/`b-l1`/`b-l2`/`b-l3`/`b-na`), same structural sections in the same order:

1. `<header>` — title, subject, framework, date.
2. **Executive Summary** — one-paragraph verdict + 4-card metric grid + scoring caveat callout.
3. **Per-Agent Scorecard** — one row per agent, level badge, 3–6 strength bullets, 1–4 gap bullets.
4. **Coverage Against the 39-Practice Checklist** — 9 rows, one per category, with `High`/`Medium`/`Low`/`N/A` badge and an evidence note.
5. **Recommendations** — two ordered lists: "To reach a clean Level 2" and "To reach Level 3". Order by leverage, not by category. Each item names the agent, the missing practice, and the observable "done" state.
6. **Housekeeping** callout — only if you actually changed files during the assessment.
7. `<footer>` — generation date, source path, framework reference.

The structural skeleton (with placeholders) is in `references/report_template.md`; the worked example is in `references/example_report.html`. Use the example as your CSS / markup reference and the template as your section checklist.

**Output path**: write the report to the **repo root** as `<suite_slug>_maturity_assessment.html` (e.g. `slb_ba_agents_maturity_assessment.html`). Tell the user the absolute path when you're done.

### Phase 7 — Hand off

After writing the file:

- State the suite-level verdict in one sentence.
- Mention any practice categories marked N/A and *why* (so the user can verify the platform-side claim).
- Point at the top 1–3 leverage recommendations.

Don't dump the whole report into the chat — the user has the file.

## Writing the report — voice and content

The example report (`references/example_report.html`) is the gold standard for tone. Match it:

- **Executive summary**: one paragraph, names the anchor agents, gives the headline level, ends with the headline next step. No filler.
- **Strengths bullets**: concrete and specific. "Hard human-in-the-loop gate before publish" beats "Has guardrails".
- **Gaps bullets**: name the missing practice, not a vibe. "No prompt-injection sanitisation on ticket text / attachments" beats "Could be more secure".
- **Coverage notes**: short, evidence-bearing, end with a period. When marking N/A, name the platform / process that handles it.
- **Recommendations**: each item must be doable. Bad: "Improve hallucination prevention". Good: "Anchor `req_validator` output — every gap claim should cite the exact AC sentence it flags, and the agent should raise an uncertainty signal when input content is sparse".

## Common pitfalls

- **Inferring features not in the spec.** If the prompt doesn't mention citations, the agent doesn't have citations — even if it would be sensible to add them. Score what's written.
- **Marking platform features as gaps.** Token cost, telemetry, eval harness usually live on the platform. Confirm in Phase 3 before scoring.
- **Over-scoring for ambition.** An agent that *talks about* doing CoT but doesn't actually structure a plan is L0/L1, not L2.
- **Averaging the suite level.** Use the anchor rule. Three L2 agents and three L1 agents do not equal "L1.5" — they equal "between L1 and L2, anchored at L2 by X and Y".
- **Skipping clarifying questions.** Always ask. The user has context you don't, and the report's defensibility depends on those answers being recorded in the scoring caveat.

## References (in this skill folder)

- `references/maturity_model_requirements.md` — the full 39-practice checklist with level tags and rationales.
- `references/scoring_rubric.md` — how to translate spec content into a level.
- `references/clarifying_questions.md` — what to ask the user, why each question matters, and how to record answers.
- `references/report_template.md` — section-by-section skeleton with placeholders.
- `references/example_report.html` — worked HTML example (SLB BA agents). Reuse the `<style>` block verbatim.
