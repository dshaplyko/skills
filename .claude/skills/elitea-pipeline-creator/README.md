# elitea-pipeline-creator

Expert assistant for building, debugging, and managing ELITEA pipelines and agents.
Knows the YAML schema, all node types, state management patterns, and the ELITEA platform MCP API.

---

## Install

Install the skill via `npx skills add`:

```bash
npx skills add git@github.com:dshaplyko/skills.git --skill elitea-pipeline-creator
```

By default this installs into the current project's `.claude/skills/`. Pass `--global` (or run from your home directory) to install user-scoped at `~/.claude/skills/` so it is available in every project.

After installing, restart Claude Code so the skill is picked up.

For ELITEA platform access, configure the ELITEA MCP in `.vscode/mcp.json` (project id is taken from the MCP URL path).

---

## What It Does

| Without skill | With skill |
|---|---|
| Hand-write pipeline YAML from docs | Generates complete, valid YAML following the schema |
| Mix legacy and modern node types | Enforces modern node types; legacy is reference-only for debugging |
| Forget `messages: list` and break history | Validation rule prevents the most common state mistake |
| Hunt for the right MCP tool | Catalog tables + detailed schemas indexed by purpose |
| Re-derive common shapes (loops, branching) | Reusable patterns: linear, loop-with-router, converging paths |
| Discover gotchas the hard way | Curated gotchas table (UUID vs id, version_id, reserved names, step_limit) |

---

## When It Triggers

Say any of the following (exact phrasing not required):

- *"create an ELITEA pipeline"*
- *"build an agent on ELITEA"*
- *"debug this pipeline YAML"*
- *"add a router node to my pipeline"*
- *"how does state work in ELITEA pipelines"*
- *"convert this legacy `function` node to modern syntax"*
- *"deploy this pipeline version via MCP"*
- *"why is my decision node not routing correctly"*

Also triggers on mentions of ELITEA, pipeline YAML, or node types (LLM, agent, toolkit, MCP, code, router, decision, state_modifier, printer).

---

## Structure

```
elitea-pipeline-creator/
├── SKILL.md                     # lean entry: rules, workflow, load-on-demand table
├── README.md
└── references/
    ├── yaml-schema.md           # top-level structure, state, all 10 modern nodes, legacy reference
    ├── patterns.md              # linear / loop / converging shapes + 5 end-to-end use cases
    ├── mcp-tools.md             # ELITEA MCP catalog (platform / conversation / artifact / TestRail)
    ├── mcp-tools-schema.md      # detailed input schemas, example calls, response shapes
    └── workflows.md             # validation checklist, debugging, best practices, gotchas
```

---

## How It Works

`SKILL.md` is intentionally small — it carries the always-in-effect rules (modern node types only, `messages: list` requirement, every path → END, no Router/Decision as `entry_point`, no hardcoded secrets) and a load-on-demand table. Detailed knowledge lives in `references/` and is loaded only when the current task needs it:

| Task | Loads |
|------|-------|
| Authoring or modifying pipeline YAML | `references/yaml-schema.md` |
| Choosing a pipeline shape | `references/patterns.md` |
| Looking up an ELITEA MCP tool | `references/mcp-tools.md` |
| MCP tool input schemas / response shapes | `references/mcp-tools-schema.md` |
| Validation, debugging, common workflows, gotchas | `references/workflows.md` |

On first invocation in a session, the skill also fetches the latest ELITEA pipeline docs from the ProjectAlita GitHub Pages source (full URL list in `SKILL.md`) and caches them for the session.

---

## Default Workflow

1. Clarify requirements (inputs, outputs, integrations).
2. Load `references/yaml-schema.md` if creating or modifying YAML.
3. Sketch the node flow — reference `references/patterns.md` for the right shape.
4. Generate complete YAML (never partial snippets).
5. Validate against the checklist in `references/workflows.md`.
6. For platform actions (deploy, run, inspect), use the MCP tools in `references/mcp-tools.md` (schemas in `references/mcp-tools-schema.md`).

---

## Notes

- **Modern vs legacy nodes** — `yaml-schema.md` documents both. Always generate modern (`llm`, `agent`, `toolkit`, `mcp`, `code`, `custom`, `router`, `decision`, `state_modifier`, `printer`). Legacy types (`tool`, `function`, `loop`, `loop_from_tool`, inline `condition`/`decision`) are documented only so Claude can read and refactor existing pipelines.
- **State `messages: list`** — if you define a custom `state` block, it **must** include `messages: list`, or conversation history breaks. Omit the `state` block entirely to use defaults.
- **Router/Decision constraints** — neither can be `entry_point`; both require `default_output`; Decision cannot chain directly to another Decision.
- **Printer node pauses** — `transition: END` after a Printer node means the pipeline doesn't fully complete until the user acknowledges.
- **MCP gotchas** — `postEliteaCoreMessages` uses `conversation_uuid` (string), not `conversation_id` (int). `postEliteaCorePredict` uses `version_id`, not application id. Version name `"base"` is reserved.
- **Secrets** — never hardcode; use `alita_client.unsecret('name')`.
- **Project id** — pulled from the ELITEA MCP URL path in `.vscode/mcp.json`.

---

## Author

EPAM QE Practice
