# Workflows, Best Practices, Troubleshooting

Operational guidance for building, debugging, and operating ELITEA pipelines.

## When Creating a Pipeline

1. **Clarify requirements**: Understand inputs, outputs, integrations needed
2. **Design state**: Define all state variables with appropriate types and defaults
3. **Plan node flow**: Sketch the node sequence, branching, and loops
4. **Generate YAML**: Produce valid YAML following the schema exactly
5. **Validate**: Check entry_point references exist, all transitions resolve, state vars are defined
6. **Test incrementally**: Add one node at a time, use interrupts to inspect state

## When Debugging a Pipeline

1. **Check YAML syntax**: Indentation (spaces not tabs), quotes around special chars
2. **Verify entry_point**: Must reference an existing node ID
3. **Check transitions**: All must point to existing nodes or END
4. **Validate state**: All variables used in nodes must be defined in `state`
5. **Inspect input/output**: Ensure node I/O arrays match state variables
6. **Use interrupts**: Add `interrupt_before`/`interrupt_after` to inspect state at key points
7. **Check structured_output**: When true, code/LLM must return dict with keys matching output vars
8. **Review input_mapping**: Ensure correct types (fixed/variable/fstring) and values

## Validation Checklist

- [ ] `entry_point` references an existing node ID
- [ ] All node IDs are unique
- [ ] All transitions reference existing nodes or END
- [ ] State variables in nodes are defined in `state`
- [ ] Input/output arrays use valid variable names
- [ ] Node-specific fields complete (LLM has `input_mapping`, Router has `condition` + `routes`, etc.)
- [ ] No YAML syntax errors (proper indentation with spaces)
- [ ] Quotes around special characters (`:`, `{`, `%`)
- [ ] Every execution path reaches END
- [ ] Router has `default_output` set

## Using MCP Tools for Development

- **Inspect existing pipelines**: Use `getEliteaCoreApplication` to review current configurations
- **List available tools**: Use `getEliteaCoreTools` to see what toolkits/MCPs are available in a project
- **Test tool I/O**: Use Artifact and TestRail toolkit tools directly to understand input/output shapes before wiring them into pipeline nodes
- **Deploy changes**: Use `putEliteaCoreVersion` to update pipeline YAML on the platform
- **Test execution**: Use `postEliteaCorePredict` to run an agent/pipeline version with test inputs

## Best Practices

- Use descriptive node IDs (`FetchUserData` not `Node1`)
- Initialize all state variables with sensible defaults
- Keep state minimal — only create variables you need
- Use Code nodes for complex logic, LLM nodes for intelligence
- Use Router for deterministic branching, Decision for semantic routing
- Always provide `default_output` for Router and Decision nodes
- Include `messages` in output when using interrupts with structured output
- Add comments in YAML to explain complex logic
- Test incrementally: build and verify one node at a time
- Use `alita_state.get('var', default)` in Code nodes to handle missing state gracefully
- Never hardcode secrets — use Credentials/`alita_client.unsecret()`
- Clean up unused state with State Modifier and `variables_to_clean`

## Code Node Special Capabilities

The Code Node's `alita_client` provides access to:

**Artifact Operations:**
```python
bucket = alita_client.artifact('bucket-name')
bucket.create('file.txt', 'content')
content = bucket.get('file.txt')
bucket.list()
bucket.append('file.txt', 'more data')
bucket.overwrite('file.txt', 'new content')
bucket.delete('file.txt')
```

**Application & Integration:**
```python
alita_client.get_app_details(application_id=123)
alita_client.get_list_of_apps()
alita_client.unsecret('secret-name')
alita_client.get_mcp_toolkits()
alita_client.mcp_tool_call(params)
```

**Image Generation:**
```python
alita_client.generate_image(prompt, n=1, size='auto', quality='auto')
```

## Response Format

When generating pipeline YAML:
1. Always produce **complete, valid YAML** — never partial snippets
2. Include all required fields for every node type
3. Add inline comments explaining non-obvious logic
4. Follow the validation checklist before presenting
5. Explain the pipeline flow in a brief summary before/after the YAML

When debugging:
1. Identify the specific issue with clear explanation
2. Show the exact fix needed
3. Explain why the fix works

When explaining concepts:
1. Be concise but thorough
2. Use examples from the schema reference
3. Link back to relevant patterns

## Troubleshooting Quick Reference

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Agent won't start | `entry_point` doesn't match any node `id` | Verify exact spelling and case |
| YAML syntax errors | Tabs instead of spaces, or bad indentation | Use spaces only; use YAML Indentation Corrector prompt |
| Unexpected transitions | Wrong `transition`/`condition`/`decision` target | Check all node ID references for typos |
| Node not found | Node ID mismatch (case-sensitive) | Ensure IDs match exactly across transitions, conditions, decisions |
| Wrong state data | State variables not updated correctly | Use `interrupt_before`/`interrupt_after` to inspect state at key points |
| Condition logic errors | Bad Jinja2 syntax in `condition_definition` | Verify `{% if %}` / `{% elif %}` / `{% else %}` / `{% endif %}` blocks |
| Function node fails | Incorrect `input_mapping` types/values | Verify `type` (variable/fstring/fixed) and `value` for each mapped param |
| Toolkit not working | Toolkit not added/configured in agent settings | Add all required toolkits in Configuration tab with correct versions |
| `messages` lost | `messages: list` missing from custom `state` | Always include `messages: list` when defining custom state |

**Debugging Strategy:** Isolate → add interrupts → inspect state → trace transitions → review error messages in Chat window.

## Quick Reference: Common MCP Workflows

### Workflow 1: Create conversation and send a message

```
1. getAuthUser                      → get user info & personal_project_id
2. postEliteaCoreConversations      → create conversation, get conversation_id and uuid
3. postEliteaCoreParticipants       → add agent participant to conversation
4. patchEliteaCoreEntitySettings    → configure LLM settings
5. postEliteaCoreMessages           → send user_input using conversation_uuid
```

### Workflow 2: List agents and get details

```
1. getProjectsProject               → list available projects
2. getEliteaCoreApplications        → list agents in a project
3. getEliteaCoreApplication         → get full details for a specific agent
```

### Workflow 3: Create agent with toolkit

```
1. postEliteaCoreApplications       → create agent with initial version
2. getEliteaCoreTools               → list available toolkits
3. patchEliteaCoreTool              → link toolkit to agent version
```

### Workflow 4: Upload file and reference in message

```
1. postEliteaCoreAttachments        → upload file, get filepath
2. postEliteaCoreMessages           → send message with attachments_info containing the filepath
```

### Workflow 5: Direct agent execution (without conversation)

```
1. getEliteaCoreApplication         → get agent details with version_id
2. postEliteaCorePredict            → execute agent directly with version_id
```

### Workflow 6: Manage agent versions

```
1. getEliteaCoreApplication         → get current agent with version details
2. postEliteaCoreVersions           → create a new version
3. putEliteaCoreVersion             → update version configuration
4. patchEliteaCoreTool              → link/unlink toolkits to version
```

### Workflow 7: Browse conversation history

```
1. getEliteaCoreConversations       → find conversation by name/query
2. getEliteaCoreConversation        → get conversation details with participants
3. getEliteaCoreMessages            → paginate through messages
```

## Key Gotchas

| Gotcha | Details |
|--------|---------|
| `postEliteaCoreMessages` uses UUID | The `conversation_uuid` parameter is a UUID string, **not** the integer `conversation_id`. Get it from the conversation's `uuid` field. |
| `postEliteaCorePredict` uses `version_id` | Execute against a specific version, not the application ID. Get it from `version_details.id`. |
| `mode` defaults to `prompt_lib` | Almost all tools default to `"prompt_lib"` mode. You rarely need to change this. |
| Pipeline instructions must be YAML | When `agent_type` is `"pipeline"`, the `instructions` field must contain valid YAML. |
| Version name cannot be `"base"` | When creating versions with `postEliteaCoreVersions`, the name `"base"` is reserved. |
| `meta.step_limit` defaults to 25 | Agent versions default to 25 execution steps. Override via `meta.step_limit`. |
| `author_id` is auto-set | Fields like `author_id` and `owner_id` are automatically set from the authenticated user — do not pass them manually. |
