# {{SUITE_NAME}} — Maturity Assessment

> **Subject:** `{{TARGET_PATH}}` — {{N_AGENTS}} agents
> **Framework:** Agent Maturity Model ({{FRAMEWORK_AUTHOR}}, {{FRAMEWORK_DATE}})
> **Assessment date:** {{REPORT_DATE}}
> **Author:** {{REPORT_AUTHOR}}

---

## Executive Summary

{{ONE_PARAGRAPH_VERDICT — where the suite sits overall (L0/L1/L2/L3), which agents anchor that score, and the headline next step.}}

| Metric | Value |
|---|---|
| Suite-level maturity | **{{SUITE_LEVEL}}** |
| Agents at L2+ | {{N_L2}} / {{N_TOTAL}} |
| Agents at L1 | {{N_L1}} / {{N_TOTAL}} |
| Agents at L0 | {{N_L0}} / {{N_TOTAL}} |
| L2 practice coverage | ~{{COVERAGE_PCT}}% |

> **Scoring caveat:** {{SCOPE_NOTES — e.g. which checklist categories are platform-side and scored as N/A rather than gaps.}}

---

## Per-Agent Scorecard

| Agent | Level | Strengths | Gaps |
|---|---|---|---|
| `{{AGENT_1_NAME}}` | **{{LEVEL}}** | {{strength bullets, semicolon-separated}} | {{gap bullets, semicolon-separated}} |
| `{{AGENT_2_NAME}}` | **{{LEVEL}}** | … | … |
| `{{AGENT_N_NAME}}` | **{{LEVEL}}** | … | … |

**Legend:** 🔴 L0 Beginner · 🟡 L1 Foundational · 🟢 L2 Advanced · 🟣 L3 Autonomous

---

## Coverage Against the 39-Practice Checklist

| # | Category | Coverage | Notes |
|---|---|---|---|
| 1 | Token economics & efficiency | {{High / Medium / Low / N/A}} | {{evidence or platform note}} |
| 2 | Planning & reasoning | {{…}} | {{…}} |
| 3 | Evaluation framework | {{…}} | {{…}} |
| 4 | Hallucination prevention | {{…}} | {{…}} |
| 5 | Tool usage & function calling | {{…}} | {{…}} |
| 6 | Conversation & memory | {{…}} | {{…}} |
| 7 | RAG & retrieval | {{…}} | {{…}} |
| 8 | Observability & monitoring | {{…}} | {{…}} |
| 9 | Safety, guardrails & compliance | {{…}} | {{…}} |

---

## Recommendations

### To reach a clean Level 2 across the suite
1. {{Highest-leverage L1→L2 action — name the agent, the missing practice, and what "done" looks like.}}
2. {{Second action.}}
3. {{Third action.}}

### To reach Level 3 (autonomous)
1. {{Reflection / self-improvement loop — what to capture, where to feed it back.}}
2. {{Domain-aware severity thresholds — which characteristics, which floor.}}
3. {{Ensemble / cross-validation for critical decisions.}}
4. {{Red-team / adversarial coverage — ingestion sanitisation, exfil tests.}}

---

## Housekeeping / Changes Made

- {{Files removed, renamed, or created during the assessment, if any.}}

---

*Generated {{REPORT_DATE}} · Source: `{{TARGET_PATH}}` · Framework: Agent Maturity Model v1 ({{FRAMEWORK_DATE}})*

---

## How to use this template

1. **Copy** this file to the target client folder (e.g. `<client>/agents/maturity_assessment.md`).
2. **Fill placeholders** — every `{{LIKE_THIS}}` token is a slot; remove sections that don't apply.
3. **Score per agent** using the rubric below before filling the scorecard:
   - **L0** — single LLM call, no planning, no tool schemas, no retries.
   - **L1** — explicit plan/CoT, tool schemas with retries, structured outputs, AI-provenance tagging, basic guardrails.
   - **L2** — adds: RAG/citations, persistent memory, self-consistency checks, HITL gates, post-write verification, completeness scoring.
   - **L3** — adds: reflection/learning loop, ensemble validation, severity-tiered faithfulness thresholds, red-team coverage.
4. **Coverage column values:** `High` (≥80% of practices in that category present), `Medium` (40–80%), `Low` (<40%), `N/A` (handled outside the agent layer — note where).
5. **Recommendations:** order by leverage, not by category. Each item should name the agent, the missing practice, and the observable "done" state.
6. **Optional:** generate the HTML version of the same content for stakeholders who prefer a styled deliverable — keep both in sync.
