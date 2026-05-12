---
name: elitea-agent-update
description: Update an ELITEA agent's instruction (and optionally name/description/welcome_message) from a local .md instruction file via the ELITEA REST API. Use this skill whenever the user wants to push a Markdown prompt/instruction file to an existing ELITEA agent — phrases like "update the agent instruction", "sync this .md to the agent", "push my_instr/foo.md to ELITEA", "update agent 79 with this file", or hands you a .md file whose header lists `Agent ID:`, `Version ID:`, `Project ID:`, and `URL:`. Reads ELITEA_API_TOKEN from the project .env, does a GET first to preserve llm_settings/tools/tags, then a dry-run diff and only PUTs when --apply is passed.
---

# ELITEA agent instruction update skill

This skill pushes a local Markdown instruction file to an existing
ELITEA agent via the REST API. It targets this endpoint (the only
documented agent-update path in the ELITEA Postman collection — note
it lives under `archive/` upstream but is still the live update path):

```
PUT  {{base_url}}/api/v1/applications/application/prompt_lib/{{project_id}}/{{agent_id}}
```

The body shape is `{name?, description?, version: {...}}`, where the
`version` object contains `instructions`, `llm_settings`, `tools`,
`tags`, `welcome_message`, `conversation_starters`, etc. To avoid
clobbering those unrelated fields, the script ALWAYS does a GET first
and only overrides the fields the user explicitly asked to change.

## Expected .md file shape

The first lines are a `Key: Value` header block, then a blank line,
then the instruction body:

```
Agent ID: 79
Version ID: 79
Project ID: 29
URL: https://next.elitea.ai/

# Role & Persona
You are the ...
```

Recognised header keys (case-insensitive): `Agent ID`, `Version ID`,
`Project ID`, `URL`. Everything from the first blank line / first
Markdown heading onward is the new `instructions` value.

If any header field is missing AND not passed via CLI flag, the
script exits with a clear error — ask the user to fill it in.

## Auth

`ELITEA_API_TOKEN` is read from the environment, or from the nearest
`.env` walking up from the current working directory (stopping at the
nearest `.git` boundary). Never paste the token elsewhere.

## Workflow

1. **Confirm the file path with the user** if not already explicit.
2. **Dry-run** (this is the default — no `--apply`):
   ```bash
   python3 .claude/skills/elitea-agent-update/scripts/update_agent.py path/to/file.md
   ```
   This prints the parsed target (agent / version / project / base URL),
   fetches the current version, and shows a diff-style summary
   (instructions changed/unchanged, char counts, first 80 chars of old
   vs new).
3. **Show the user the summary** and ask for confirmation.
4. **Apply** only after the user confirms:
   ```bash
   python3 .claude/skills/elitea-agent-update/scripts/update_agent.py path/to/file.md --apply
   ```

## Updating other fields

Pass `--set FIELD=VALUE` (repeatable):

- `--set name="New agent name"` — top-level application name
- `--set description="..."` — top-level application description
- `--set welcome_message="..."` — version-level welcome message

Example:
```bash
python3 .claude/skills/elitea-agent-update/scripts/update_agent.py \
    my_instr/postman_researcher.md \
    --set description="Postman researcher with structured output" \
    --apply
```

## Overriding header values

If the .md header is missing or wrong, override per-invocation:
`--agent-id`, `--version-id`, `--project-id`, `--base-url`.

## Do not

- Do not invent or guess `ELITEA_API_TOKEN`, IDs, or base URLs.
- Do not skip the dry-run unless the user has just reviewed it and
  asked you to apply.
- Do not edit `update_agent.py` to hardcode credentials or IDs.
