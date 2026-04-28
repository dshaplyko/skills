# Per-Agent Scoring Rubric

Use this rubric to assign a single level (L0 / L1 / L2 / L3) per agent. The model is **cumulative** — every level inherits all requirements from the level below it. An agent is scored at the highest level whose criteria it fully meets; if it meets *most* of L2 but misses one or two, mark it `L1+` rather than over-claiming.

## Quick reference

| Level | Label | Headline characteristics |
|---|---|---|
| **L0** 🔴 | Beginner | Single LLM call, no plan, no tool schemas, no retries, manual review only. |
| **L1** 🟡 | Foundational | Explicit plan / CoT, tool schemas with retries, structured outputs, AI-provenance tagging, basic guardrails, tool-call logging, cost limits per call. |
| **L2** 🟢 | Advanced | Adds: RAG with citations, persistent memory, self-consistency / faithfulness checks, HITL gate on irreversible actions, post-write verification, completeness scoring, multi-turn degradation tests. |
| **L3** 🟣 | Autonomous | Adds: reflection / learning loop, ensemble validation on critical decisions, severity-tiered faithfulness floors (e.g. ≥0.95 for medical/legal/financial), red-team / adversarial coverage, named-user attribution + full audit trail. |

## How to read the agent specification

Most agents in this repo are Markdown prompt files (`*.md`) optionally paired with a YAML pipeline (`*.yml`). Look for these signals:

- **Planning** — sections like "## STEPS", "## HOW YOU WORK", explicit Chain-of-Thought instructions, decomposition rules.
- **Tools** — references to tool calls, MCP toolkits, schemas, retry / timeout language ("retry up to 5x", "if X fails, surface STATUS=ERROR…").
- **Memory / RAG** — artifact stores, "load file", similarity checks, vision-ticket lookups, ISO/IEC reference loading, embedding mentions.
- **Guardrails** — "never fabricate", HITL gate phrasing ("ask user before publishing"), AI-Draft / Pending Review tagging, sanitisation.
- **Verification** — post-write reads, completeness scores, self-consistency cross-checks (title ↔ description ↔ AC), citation requirements.
- **Observability** — structured `STATUS` / `ERROR_STEP` / `ERROR_DETAIL` returns, logging instructions.
- **Reflection** — explicit "learn from prior runs", reflection memory, ensemble / panel-of-three voting.

If the spec is silent on a capability, that is a **gap**, not a hidden strength. Don't infer features that aren't written down.

## Strengths and gaps — what to write

For each agent, capture:

- **Strengths**: 3–6 concrete bullets, each tied to a specific instruction / section in the spec. Bad: "good prompts". Good: "Mandatory post-write verification (re-reads created item)".
- **Gaps**: 1–4 bullets that name the *missing* practice, not a vague worry. Bad: "could be more robust". Good: "No prompt-injection sanitisation on ticket text / attachments".

Tie every claim back to evidence you can quote from the spec — that is what makes the report actionable rather than aspirational.

## Coverage column values (39-practice checklist)

When filling the coverage table, use:

- **High** — ≥80% of practices in that category present.
- **Medium** — 40–80% present.
- **Low** — <40% present.
- **N/A** — handled outside the agent layer (platform feature, ops process, off-platform evaluation). When you mark N/A, **say where** in the notes column ("EliteA platform", "client-side sandbox review", etc.). Don't use N/A to hide gaps.

## Suite-level rollup

The suite level is **not the average** — it's the level at which the *anchor* agents (the ones doing the load-bearing work) sit, tempered by how many sibling agents drag below. Rules of thumb:

- All agents at L2+ → suite = L2.
- Anchors at L2, support agents at L1 → suite sits "between L1 and L2"; quote the anchor agents by name.
- Any anchor agent at L0 → suite = L0 regardless of others.

State the rollup logic in the executive summary so a reader can sanity-check it.
