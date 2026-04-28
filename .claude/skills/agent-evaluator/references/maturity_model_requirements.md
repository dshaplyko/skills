Created by Ihar Bylitski, last updated on Feb 17, 2026  1 minute read
📊 Chapter 1: Agent Maturity Model
About This Model

A cumulative maturity model where each level includes all capabilities from previous levels. Progress from basic LLM integration to autonomous agentic networks.

The Four Levels at a Glance
🔴 Level 0 — BEGINNER
Basic LLM Integration

5 PRACTICES
Simple prompt-response patterns with minimal safeguards. Suitable for internal tools and prototypes.

Single LLM, single task pattern
No explicit planning
Manual review of outputs
Direct API calls
🟡 Level 1 — FOUNDATIONAL
Production-Ready Single Agent

19 PRACTICES
Structured agent with planning, tools, and evaluation. Ready for production deployment.

Explicit planning with CoT
Tool usage with schemas
Automated evaluation
Cost tracking & alerts
🟢 Level 2 — ADVANCED
Sophisticated Production Agent

35 PRACTICES
Full-featured agent with RAG, persistent memory, and hallucination prevention.

Hybrid RAG with reranking
Persistent memory
Hallucination detection
Human-in-the-loop
🟣 Level 3 — AUTONOMOUS
Agentic Network

39 PRACTICES
Self-improving multi-agent system with minimal human oversight.

Multi-agent orchestration
Self-reflection & learning
Full regulatory compliance
Predictive monitoring
🔍 Level Details (Cumulative)
🔴 Level 0: BEGINNER — Basic LLM Integration (5 Practices)
🟡 Level 1: FOUNDATIONAL — Production-Ready Single Agent (19 Practices = 5 + 14 new)
🟢 Level 2: ADVANCED — Sophisticated Production Agent (35 Practices = 19 + 16 new)
🟣 Level 3: AUTONOMOUS — Agentic Network (39 Practices = 35 + 4 new)
📋 Chapter 2: Best Practices Checklist
39 practices across 9 categories. Each practice shows its minimum maturity level requirement.

1. TOKEN ECONOMICS & EFFICIENCY




L0
Manage output length for quality and cost

LLMs struggle with text >4,000 words (HelloBench 2024). Output tokens cost 3–5× more than input. Chunking reduces hallucination by 40–60%.

All API calls have explicit limits; bulk outputs use iteration

L1
Implement context budget allocation

Lost-in-the-middle shows >30% degradation when critical info is mid-context (Liu et al., TACL 2024).

Critical information at start/end of context

L1
Cache reusable artifacts between agent runs

Cached tokens cost 10% of base price — 90% savings. LLMLingua compresses prompts by up to 20×.

>70% cache hit rate; measurable cost reduction

L2
Avoid model calls when scripts or tool calls suffice

RouteLLM: 40% cheaper with same performance. Hybrid-LLM: 22% queries to smaller model with <1% quality drop.

≥50% simple tasks use efficient models

L1
Optimize data flow to minimize token transmission

32K to 128K context triples GPU memory. Hidden costs add 15–30%.

No unnecessary context re-transmission

L1
Track costs with real-time monitoring

Tier-1 financials spend up to $20M daily. Batch APIs offer 50% discount.

Cost per task documented; ≥30% batch processing

2. PLANNING & REASONING




L1
Guide planning with CoT, but leave room for reasoning

ReAct (Yao 2023): Reasoning traces allow model to induce, track, update action plans.

All complex tasks have plan; CoT enabled

L2
Ensure sufficient data and pre-requisites before any generation

ADaPT (NAACL 2024): 28.3% higher success via recursive decomposition.

Tasks decomposed into ≤5 subtasks

L2
Build new plans from outputs; avoid rigid pipeline architectures

Closed-loop systems adapt plans based on feedback (ACL 2025).

Plans persist >10 turns; revision capability

L1
Estimate and confirm expensive operations

Output tokens cost 2–5× input. $9K–$109K per million requests depending on model.

Operations >$1 estimated; confirm >$10

3. EVALUATION FRAMEWORK




L1
Maintain statistically valid test datasets

~246 samples required for 95% confidence, 5% margin. Misjudging shifts metrics by 10%.

≥30 cases minimum; ~246 for validity

L2
Create expert-validated golden datasets

Target Cohen's kappa >0.7. Anthropic found only 63% crowdsource agreement.

Kappa >0.7; all entries expert-validated

L1
Version control datasets and prompts together

Results must link to specific versions for reproducibility (Microsoft 2024).

Every run linked to dataset/prompt version

L2
Balance synthetic, real-world, and adversarial data

Production-derived cases improved performance by 34% vs synthetic-only.

≥30% real-world; ≥10% adversarial

L1
Run evaluations with statistical rigor

10% accuracy fluctuation across identical runs. GPT-4 has self-preference bias.

≥3 runs; variance <10%; separate judge model

L2
Track multi-dimensional metrics by impact

KDD Survey: Evaluate behavior, capabilities, reliability, safety.

≥5 metrics; business weights documented

L2
Test end-to-end including multi-turn

39% lower performance in multi-turn vs single-turn (OpenReview 2025).

E2E tests cover all workflows

L2
Cross-validate critical decisions with ensemble

Panel of three reduces variance by at least 50% (Scale AI 2025).

Critical decisions use ≥3 calls

4. HALLUCINATION PREVENTION




L2
Include citations in responses to verify relevance

50–90% of responses not fully supported by sources. AGREE achieves 30%+ improvement.

Faithfulness >0.85; >90% claims cited

L2
Monitor uncertainty signals

SelfCheckGPT: Hallucinated facts show divergent responses across samples.

Entropy alerts set; <15% variance on ≥5 samples

L3
Apply domain-appropriate severity thresholds

Hallucinations >1/3 of deployed incidents. Medical: 1.47% rate with high stakes.

Medical/legal/financial ≥0.95 faithfulness

5. TOOL USAGE & FUNCTION CALLING




L1
Design tools with clear names and schemas

BFCL: Top AIs stumble on context retention and when not to act.

100% naming standard; >95% selection accuracy

L2
Filter tools contextually per task

Too many tools degrades quality and increases latency (Anthropic 2024).

≤10 tools per turn; <5% false positives

L1
Handle tool failures with retry

5–15% production failure rate. Sandboxed execution prevents cascading failures.

All tools have timeout/retry; no silent failures

L1
Log all tool calls for observability

Complete audit trails essential for debugging and compliance.

100% tool calls logged with full context

6. CONVERSATION & MEMORY




L1
Manage context with summarization

MemGPT: Virtual context management enables unbounded conversation.

Summarization before 80% context fill

L2
Implement persistent memory for critical facts

Key facts must persist across sessions. External memory beyond context limits.

Facts persist; >95% retrieval accuracy

L2
Test and monitor multi-turn degradation

39% performance drop multi-turn vs single-turn (OpenReview 2025).

Weekly tests; <20% drop at turn 10

7. RAG & RETRIEVAL




L2
Chunk documents with semantic boundaries

Naive chunking breaks semantic units. 10–20% overlap prevents info loss.

Semantic boundaries; 10–20% overlap

L2
Use hybrid retrieval with reranking

Combining dense + sparse yields 10–15% improvement.

Both retrieval types; MRR >0.7

L2
Evaluate retrieval quality independently

Poor retrieval with good generation masks underlying issues.

Recall@5 >0.8; tracked separately

L2
Maintain embedding freshness

Stale embeddings cause retrieval failures for updated content.

Refresh SLA defined; freshness monitored

8. OBSERVABILITY & MONITORING




L1
Implement comprehensive instrumentation

Hallucinations cost $67.4B in 2024. Track TTFT, ITL, loops, token usage.

TTFT p95 <2s; ITL p95 <100ms; OTEL traces

L2
Gate releases on automated evaluation

Evaluation-first achieves 30%+ accuracy improvements (Braintrust).

100% releases gated; no undocumented overrides

L3
Establish continuous feedback loops

Reflexion: Agents generate reflections stored as episodic memory.

Weekly production review; monthly improvements

9. SAFETY, GUARDRAILS & COMPLIANCE




L2
Implement human oversight for high-risk

EU AI Act Article 14: High-risk AI must be overseen by natural persons.

All high-risk have HITL; <85% confidence triggers review

L1
Implement layered guardrails

OWASP: Prompt injection is #1 risk. 39% had agents access unintended systems.

Bypass rate <0.1%; 100% irreversible confirmed

L3
Run agents under named users; log all actions

97% AI breaches had inadequate access controls. 90% agents over-permissioned.

Logs retrievable <24h; default-deny configured

L3
Ensure agent prevents harmful actions even when users attempt them

MITRE ATLAS: Playbooks for prompt injection, exfiltration, collusion.

≥10% safety tests; quarterly red-teaming

📚 Chapter 3: References
Academic Research
ReAct (Yao et al., 2023): Synergizing Reasoning and Acting
Chain-of-Thought (Wei et al., 2022): Emergent abilities
ADaPT (Prasad et al., NAACL 2024): Recursive decomposition
Lost in the Middle (Liu et al., TACL 2024): Context position
Hybrid-LLM (ICLR 2024): Cost-efficient routing
FrugalGPT (TMLR 2024): Adaptive LLM selection
RouteLLM (LMSYS, 2024): Preference-based routing
SelfCheckGPT (Manakul, 2023): Consistency detection
Reflexion (Shinn, 2023): Verbal reinforcement learning
ACM Hallucination Survey (2024): Taxonomy
MemGPT (2024): Virtual context management
Regulatory & Security Frameworks
EU AI Act (2024/1689): High-risk oversight
NIST AI RMF (2024): GenAI risk management
ISO 42001: AI management systems
OWASP Top 10 LLM (2025): Security threats
MITRE ATLAS (2024): AI red-teaming playbooks
IBM Data Breach (2025): AI access findings
Obsidian Security (2025): Over-permissioning study