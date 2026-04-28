# Clarifying Questions — Pre-Report Checklist

The maturity model includes practices that **cannot be judged from the agent specification alone** — they live on the agentic platform, in ops processes, or in evidence the user holds outside the repo. Before generating the final HTML report, ask the user about each one. Skipping this step produces a report full of false gaps.

Use the `AskUserQuestion` tool. Group related items into one prompt rather than firing them one by one. For each topic, **prefill the most likely default** based on what you saw in the spec, so the user can confirm with a single click.

## What to ask, and why each matters

### 1. Token economics & cost monitoring (Category 1)
Most agentic platforms (EliteA, LangSmith, custom dashboards) provide token-per-run metrics, batch discounts, and cost alerts at the platform layer — the agent spec rarely mentions them. Without confirmation you will mis-mark this category as a gap.

Ask:
- Is token usage / cost-per-run tracked by the agentic platform (e.g. EliteA, LangSmith, Helicone, in-house)? If yes, name it.
- Are there cost alerts or budget caps configured outside the agent spec?
- Is prompt / KV caching enabled at the platform level?

If the user confirms platform-side handling, mark Category 1 as **N/A (platform)** with a note naming the platform — not as a gap.

### 2. Evaluation framework (Category 3)
Test datasets, golden sets, statistical evaluation rigor are usually run *off-platform* (sandbox tickets, client review sessions, eval harnesses). The agent spec almost never mentions them.

Ask:
- Is there an evaluation suite for these agents? If yes: how many cases, who validates them, how often is it run?
- Are runs versioned against specific prompt / dataset versions?
- Is there a separate judge model or human reviewer?

Mark **N/A** if handled outside the agent layer; mark a real gap only if the user says no eval exists at all.

### 3. Observability & monitoring (Category 8)
Tracing, TTFT/ITL latency, OTEL spans, release gates — these are platform features. The agent spec usually only contributes structured `STATUS / ERROR_STEP / ERROR_DETAIL` returns.

Ask:
- Does the platform emit traces / latency metrics / token telemetry per run?
- Are releases gated on automated evaluation, or promoted manually?

### 4. Safety, guardrails & compliance (Category 9, partial)
Some Category 9 practices are agent-spec material (HITL gates, AI-Draft tagging, no-fabrication rules — visible in the prompt). Others are platform / ops:

Ask:
- Are agents run under named user identity (per-user attribution, audit logs retrievable <24h)?
- Is there a red-team / adversarial test cadence?
- Is there a default-deny posture on tool permissions?

### 5. RAG freshness & embedding refresh (Category 7)
The spec may mention RAG / similarity / reference-doc loading, but rarely names a refresh SLA. Confirm before scoring.

Ask:
- Is there a refresh SLA on any embedded knowledge base or reference document used by the agents?

### 6. Memory persistence (Category 6)
If the spec references an "artifact store" or "session memory" without details, confirm whether facts truly persist across sessions or only within one.

Ask:
- Does memory / artifact storage persist across sessions, or is it scoped per session?

### 7. Scope ambiguities

Ask up front, before reading the agents in depth:

- **Suite name** — what should the report be titled? (e.g. "<Client> BA Agents", "<Client> QA Suite")
- **Target path** — confirm the folder / files being assessed.
- **Author** — whose name goes on the report?
- **Anchor agents** — if the suite has many agents, which one or two are doing the load-bearing work? (Used in the executive-summary rollup.)
- **Out-of-scope categories** — anything the user explicitly does *not* want scored (e.g. "Category 3 is handled by client review, mark N/A").

## Question style

- Be direct: "Does the platform track per-run token cost?" not "I was wondering if perhaps…".
- Offer the most-likely answer as the first option (recommended).
- One topic per question, max 4 options.
- If the user has already volunteered an answer in earlier turns, **skip that question** — don't re-ask.

## Recording answers

Note every confirmed answer in the report's **Scoring caveat** callout near the top, e.g.:

> Token-cost monitoring and statistical evaluation are platform-side concerns (EliteA + ongoing client review on a sandbox with limited tickets). Those practices are scored as not applicable at the agent layer rather than as gaps.

This makes the report defensible — a reader can see exactly which N/A calls came from user confirmation versus assumption.
