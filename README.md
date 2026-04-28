# Skills

A personal collection of [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills) I've built and use.

## Skills

- **agent-evaluator** — Score AI agents against the Agent Maturity Model (L0–L3) and generate an HTML report.
- **docx-to-markdown** — Convert `.docx` / `.doc` files to clean Markdown via Pandoc, preserving images.
- **elitea-api** — Answer questions about the ELITEA REST API using the live Postman collection.
- **meeting-followup** — Turn a raw meeting transcript into a structured follow-up doc with action items.
- **pipeline-creator** — Build, run, and debug ELITEA pipelines and agents (YAML, nodes, MCP).
- **skill-creator** — Create, edit, evaluate, and benchmark Claude Code skills.

## Layout

```
.claude/skills/<skill-name>/SKILL.md
```

Each skill lives in its own folder under `.claude/skills/` with a `SKILL.md` describing when and how it triggers.

## Usage

Open this directory in Claude Code — the skills are auto-discovered and invocable by name (e.g. `/skill-creator`).
