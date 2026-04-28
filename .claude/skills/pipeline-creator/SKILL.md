---
name: pipeline-creator
description: Expert assistant for building, running, debugging, and managing ELITEA pipelines and agents. Knows YAML schema, all node types, state management, and can interact with the ELITEA platform via MCP tools. Use this skill whenever the user wants to create a pipeline, debug a pipeline, modify pipeline YAML, build an ELITEA agent, work with pipeline nodes, manage pipeline state, or interact with the ELITEA platform API. Also trigger when user mentions ELITEA, pipeline YAML, node types (LLM, agent, toolkit, MCP, code, router, decision, state_modifier, printer), or pipeline debugging.
---

# ELITEA Pipeline & Agent Builder

You are an expert ELITEA pipeline and agent architect. You help users **design, build, debug, optimize, and deploy** pipelines and agents on the ELITEA platform. You have deep knowledge of the YAML schema, all node types, state management patterns, and the ELITEA MCP API.

## Documentation Reference

On first invocation in a session, fetch the latest pipeline documentation from:
- https://github.com/ProjectAlita/projectalita.github.io/blob/main/docs/features/pipelines/pipeline-agent-framework.md
- https://github.com/ProjectAlita/projectalita.github.io/blob/main/docs/home/key-concepts/what-is-an-agent.md
- https://github.com/ProjectAlita/projectalita.github.io/blob/main/docs/home/key-concepts/what-is-a-pipeline.md
- https://raw.githubusercontent.com/ProjectAlita/projectalita.github.io/main/docs/how-tos/pipelines/overview.md
- https://raw.githubusercontent.com/ProjectAlita/projectalita.github.io/main/docs/how-tos/pipelines/yaml.md
- https://raw.githubusercontent.com/ProjectAlita/projectalita.github.io/main/docs/how-tos/pipelines/states.md
- https://raw.githubusercontent.com/ProjectAlita/projectalita.github.io/main/docs/how-tos/pipelines/nodes-connectors.md
- https://raw.githubusercontent.com/ProjectAlita/projectalita.github.io/main/docs/how-tos/pipelines/nodes/interaction-nodes.md
- https://raw.githubusercontent.com/ProjectAlita/projectalita.github.io/main/docs/how-tos/pipelines/nodes/execution-nodes.md
- https://raw.githubusercontent.com/ProjectAlita/projectalita.github.io/main/docs/how-tos/pipelines/nodes/control-flow-nodes.md
- https://raw.githubusercontent.com/ProjectAlita/projectalita.github.io/main/docs/how-tos/pipelines/nodes/utility-nodes.md
- https://raw.githubusercontent.com/ProjectAlita/projectalita.github.io/main/docs/how-tos/pipelines/pipeline-runs.md
- https://raw.githubusercontent.com/ProjectAlita/projectalita.github.io/main/docs/how-tos/pipelines/ai-assistant-in-nodes.md
- https://raw.githubusercontent.com/ProjectAlita/projectalita.github.io/main/docs/how-tos/pipelines/entry-point.md
- https://raw.githubusercontent.com/ProjectAlita/projectalita.github.io/main/docs/how-tos/pipelines/flow-editor.md
- https://raw.githubusercontent.com/ProjectAlita/projectalita.github.io/main/docs/how-tos/pipelines/appendix-comparison-tables.md

Cache this documentation context for the session to avoid re-fetching.

---

## Core Knowledge: Pipeline YAML Schema

### Top-Level Structure

Every pipeline YAML has three required top-level sections:

```yaml
entry_point: <node_id>        # Required — starting node ID
state: {...}                   # Required — state variable definitions
nodes: [...]                   # Required — node configurations
```

Optional top-level fields:
```yaml
interrupt_before: [NodeA, NodeB]   # Pause BEFORE these nodes (global list)
interrupt_after: [NodeA, NodeB]    # Pause AFTER these nodes (global list)
```

Alternatively, set interrupts **per node** inline:
```yaml
- id: MyNode
  type: llm
  interrupt_before: true    # pause before this specific node
  interrupt_after: true     # pause after this specific node
  ...
```
Both forms are valid. Inline per-node form is convenient during development to inspect state at a single node without editing the top-level lists.

### State Configuration

State is the pipeline's memory system. Every pipeline has two default states:

- **`input`** (str) — most recent user message (short-term memory)
- **`messages`** (list) — complete conversation history (long-term memory)

Custom state syntax:
```yaml
state:
  <variable_name>:
    type: <str|number|list|JSON>
    value: <default_value>  # Optional
```

**Data Types:** `str` (string/text), `number`/`int` (int/float), `list` (ordered collections), `JSON`/`dict` (dict/key-value pairs)

**Critical Rule:** If you define a custom `state` section, you **must** include `messages: list` within it. Without it, the agent cannot maintain conversation history. If you don't need custom state variables, omit the `state` section entirely to use the default `messages` state.

**State Name Rules:**
- Letters (a-z, A-Z), numbers (0-9), underscores (_) only
- Must start with a letter
- No spaces, hyphens, or special characters

### Node Types (10 types in 4 categories)

> **IMPORTANT:** There are two generations of pipeline node types. **Always use the current node types below when creating new pipelines.** The legacy system (`tool`, `function`, `loop`, `loop_from_tool` with inline `condition`/`decision`) is documented at the end of this section **for reference only** — do NOT use legacy nodes in new pipelines. Use their modern equivalents instead (see mapping table in the Legacy section).

#### Interaction Nodes

**1. LLM Node** — Direct LLM interaction with full control

`prompt.type` can be `string` (plain text) or `fstring` (formatted with `{state_var}` placeholders). When using `fstring`, all referenced variables must be listed in `input`.

```yaml
- id: <unique_id>
  type: llm
  prompt:
    type: string          # string | fstring
    value: ''
  input: [input, messages]
  output: [messages]
  structured_output: false
  transition: <next_node_id>
  input_mapping:
    system:
      type: fixed          # fixed | variable | fstring
      value: "System prompt here"
    task:
      type: fstring
      value: "Process this: {input}"
    chat_history:
      type: variable
      value: messages
  tool_names:               # Optional — bind toolkits/MCPs
    toolkit_name:
      - tool1
      - tool2
```

**2. Agent Node** — Delegate to pre-configured agents
```yaml
- id: <unique_id>
  type: agent
  input: [input]
  output: [messages]
  transition: <next_node_id>
  input_mapping:
    task:
      type: fstring
      value: "Do this: {input}"
    chat_history:
      type: fixed
      value: []
  tool: <agent_name>        # Must be added to pipeline first
```

#### Execution Nodes

**3. Toolkit Node** — Execute ELITEA toolkit functions (no LLM overhead)
```yaml
- id: <unique_id>
  type: toolkit
  input: [input]
  output: [messages]
  structured_output: false
  transition: <next_node_id>
  toolkit_name: <toolkit_name>
  tool: <tool_name>
  input_mapping:
    param1:
      type: fixed           # fixed | variable | fstring
      value: "static_value"
    param2:
      type: variable
      value: state_var_name
```

**4. MCP Node** — Execute MCP server tools
```yaml
- id: <unique_id>
  type: mcp
  input: [input]
  output: [messages]
  structured_output: false
  transition: <next_node_id>
  toolkit_name: <mcp_server_name>
  tool: <mcp_tool_name>
  input_mapping:
    param1:
      type: fixed
      value: "value"
```

**5. Code Node** — Execute Python in Pyodide sandbox
```yaml
- id: <unique_id>
  type: code
  code:
    type: fixed              # fixed | variable | fstring
    value: |
      # Access state via alita_state
      data = alita_state.get('var_name', default)
      # Return dict for structured output
      {"result_var": processed_data}
  input: [var_name]
  output: [result_var]
  structured_output: true
  transition: <next_node_id>
```

Code Node rules:
- Use `alita_state.get('var', default)` to access state
- Return dict with `structured_output: true` for state updates
- Use `httpx.AsyncClient` for HTTP (not `requests`)
- Use `micropip` for package installation
- `alita_client` is available for artifact/bucket/app operations

**6. Custom Node** — Advanced manual JSON configuration
```yaml
- id: <unique_id>
  type: custom
  input: [input]
  output: [messages]
  config:
    toolkit_type: "advanced_toolkit"
    parameters:
      custom_param1: "value1"
  transition: END
```

#### Control Flow Nodes

**7. Router Node** — Template-based conditional routing (fast, no LLM)
```yaml
- id: <unique_id>
  type: router
  condition: |
    {% if 'approved' in input|lower %}
    ApproveNode
    {% elif 'reject' in input|lower %}
    RejectNode
    {% else %}
    END
    {% endif %}
  input: [input]
  routes:
    - ApproveNode
    - RejectNode
    - END
  default_output: DefaultNode
```

**8. Decision Node** — LLM-powered intelligent routing
```yaml
- id: <unique_id>
  type: decision
  description: |
    Route based on user intent:
    - publish content → ArticlePublisher
    - review content → ContentModerator
    - finish → END
  input: [input, messages]
  nodes:
    - ArticlePublisher
    - ContentModerator
  default_output: END
```

#### Utility Nodes

**9. State Modifier Node** — Transform state with Jinja2 templates
```yaml
- id: <unique_id>
  type: state_modifier
  template: '{{ counter + 1 }}'
  variables_to_clean: []
  input: [counter]
  output: [counter]
  transition: <next_node_id>
```

Available custom Jinja2 filters:
- `|from_json` — parse a JSON string into an object (e.g. `{{ api_response|from_json }}`)
- `|base64_to_string` — decode base64-encoded data
- `|split_by_words(n)` — split text into chunks of `n` words
- `|split_by_regex('pattern')` — split text using a regex pattern

Standard filters also work: `|upper`, `|lower`, `|length`, `|default('fallback')`

**10. Printer Node** — Display output to the user and pause for acknowledgement

The Printer Node shows a message to the user and **automatically pauses** the pipeline until the user types anything to continue. Use it for progress updates, review checkpoints, and final output display.

`input_mapping.printer` is the **required field name** — the value can be `fixed`, `variable`, or `fstring`.

```yaml
- id: <unique_id>
  type: printer
  input_mapping:
    printer:
      type: fstring          # fixed | variable | fstring
      value: 'Found {count} results in {project_name}'
  transition: <next_node_id>  # or END
```

> **Note:** If `transition: END`, the pipeline does not fully complete until the user provides input to acknowledge the message.

### Connection Rules

- **`transition`**: Simple single-target connection (most nodes)
- **`routes`** + **`condition`**: Multi-path routing (Router)
- **`nodes`** + **`description`**: LLM-powered routing (Decision)
- **`END`**: Terminate pipeline execution
- Every path must eventually reach END
- The `entry_point` can be **any node type** except `router` and `decision`
- Router nodes cannot be entry points
- Decision nodes cannot be entry points
- Decision nodes cannot chain directly to other Decision nodes

### Input Mapping Types

| Type | Purpose | Example |
|------|---------|---------|
| `fixed` | Static, unchanging value | `value: "Hello"` |
| `variable` | Reference to state variable | `value: user_input` |
| `fstring` | Template with `{var}` interpolation | `value: "Process {data}"` |

### Legacy Node Types (Pipeline Agent Framework) — REFERENCE ONLY

> **DO NOT USE legacy node types when building new pipelines.** They are documented here solely so you can understand and debug existing pipelines that use them. For new pipelines, always use the modern equivalents.

**Legacy → Modern Mapping:**

| Legacy Node | Modern Equivalent | Notes |
|-------------|-------------------|-------|
| `tool` | `agent` or `toolkit` | Use `agent` for delegating to agents/prompts; `toolkit` for direct tool calls |
| `function` | `agent` or `toolkit` with `input_mapping` | `agent`/`toolkit` nodes provide the same explicit input mapping |
| `loop` | `code` node with loop logic | Implement iteration in a Code node with Router for control flow |
| `loop_from_tool` | `toolkit` + `code` + `router` | Chain a toolkit call → code processing → router loop |
| Inline `condition` | `router` node | Use a separate Router node for Jinja2-based branching |
| Inline `decision` | `decision` node | Use a separate Decision node for LLM-powered routing |

The original Pipeline Agent Framework uses a different set of node types. They may be encountered in existing pipelines.

#### `tool` Node — Simple entity delegation (uses LLM internally for input prep)
```yaml
- id: <unique_id>
  type: tool
  tool: <entity_name>          # Name of ELITEA prompt, agent, or datasource
  input: [input]               # Optional
  output: [result]             # Optional
  structured_output: false
  transition: <next_node_id>
```
**Note:** `tool` nodes use LLM overhead internally to prepare inputs. Use `function` nodes for more token-efficient execution.

#### `function` Node — Direct ELITEA entity call with explicit input mapping
```yaml
- id: <unique_id>
  type: function
  input: [state_var]           # Mandatory
  output: [result_var]         # Mandatory
  input_mapping:
    task:                      # For agents
      type: fstring            # variable | fstring | fixed
      value: "Process: {state_var}"
    chat_history:              # For agents
      type: fixed
      value: []
    input:                     # For prompts (without variables)
      type: variable
      value: state_var
    query:                     # For datasources
      type: fstring
      value: "Search for {topic}"
  transition: <next_node_id>
```

#### `loop` Node — Repeat a task for each item
```yaml
- id: <unique_id>
  type: loop
  task: "Formulate ALL file paths from chat_history as a list of inputs."
  tool: <agent_or_prompt_name>
  input: [file_listing]        # Optional but more token-efficient
  output: [results]            # Optional
  transition: <next_node_id>
```

#### `loop_from_tool` Node — Iterate over dynamically generated items
```yaml
- id: <unique_id>
  type: loop_from_tool
  tool: <tool_that_generates_list>
  loop_tool: <tool_for_each_item>
  structured_output: true
  variables_mapping:
    id: task                   # Map output var → loop_tool input param
    messages: chat_history
  transition: <next_node_id>
```

### Legacy Inline Conditions & Decisions — REFERENCE ONLY

In the legacy framework, `condition` and `decision` are **attributes within nodes** (typically `llm` nodes), not separate node types. **For new pipelines, use `router` and `decision` nodes instead.**

#### Inline Condition (within an `llm` or `function` node)
```yaml
- id: UserApproval
  type: llm
  input: [input]
  prompt:
    type: string
    value: "Provide details and type 'approved' when ready."
  output: [data_field]
  structured_output: true
  condition:
    condition_input: [data_field, input]
    condition_definition: |
      {% if 'approved' in input|lower and data_field %}
      NextStep
      {% else %}
      UserApproval
      {% endif %}
```

#### Inline Decision (within an `llm` node)
```yaml
- id: UserFeedback
  type: llm
  input: [enhanced_us, input]
  prompt:
    type: fstring
    value: "Review this: {enhanced_us}. Type Publish, Edit, or Finish."
  output: [user_feedback]
  decision:
    nodes: ["PublishStory", "RequestEdit", "END", "UserFeedback"]
    description: "Route based on user feedback keywords."
    decisional_inputs: ["input"]
    default_output: "UserFeedback"
```

---

## Common Pipeline Patterns

### Linear Flow
```yaml
entry_point: Step1
nodes:
  - id: Step1
    type: llm
    transition: Step2
  - id: Step2
    type: code
    transition: END
```

### Loop with Router
```yaml
- id: ProcessItem
  type: code
  transition: CheckComplete
- id: CheckComplete
  type: router
  condition: |
    {% if current_index < total_count %}
    ProcessItem
    {% else %}
    END
    {% endif %}
  routes: [ProcessItem, END]
  default_output: END
```

### Converging Paths
```yaml
- id: RouteInput
  type: decision
  nodes: [PathA, PathB]
  default_output: END
- id: PathA
  type: toolkit
  transition: FinalReport
- id: PathB
  type: toolkit
  transition: FinalReport
- id: FinalReport
  type: llm
  transition: END
```

---

## ELITEA MCP Tools Available

You have access to the ELITEA MCP which enables you to interact with the platform directly. Use these tools to inspect, create, modify, and test pipelines and agents.

### Platform Management Tools

| Tool | Purpose |
|------|---------|
| `getAuthUser` | Get current authenticated user info |
| `getProjectsProject` | List projects for the user |
| `getEliteaCoreApplications` | List all agents/pipelines in a project |
| `getEliteaCoreApplication` | Get agent/pipeline details + version info |
| `postEliteaCoreApplications` | Create a new agent/pipeline |
| `postEliteaCoreVersions` | Create a new version for an agent/pipeline |
| `putEliteaCoreVersion` | Update an existing version configuration |
| `getEliteaCoreTools` | List project toolkits and available tools |
| `patchEliteaCoreTool` | Link an agent to a toolkit |
| `postEliteaCorePredict` | Execute an agent version and get predictions |

### Conversation Tools

| Tool | Purpose |
|------|---------|
| `postEliteaCoreConversations` | Create a new conversation |
| `getEliteaCoreConversations` | List conversations |
| `getEliteaCoreConversation` | Get conversation details |
| `postEliteaCoreMessages` | Send message and get AI response |
| `getEliteaCoreMessages` | Get messages from a conversation |
| `postEliteaCoreParticipants` | Add participants to conversation |
| `deleteEliteaCoreParticipant` | Remove participant from conversation |
| `patchEliteaCoreEntitySettings` | Configure LLM settings in conversation |
| `postEliteaCoreAttachments` | Upload file attachments |
| `putEliteaCoreAttachmentStorage` | Configure attachment storage |
| `putEliteaCoreApplicationAttachmentStorage` | Attach storage to agent version |

### Artifact Toolkit (file/data operations)

| Tool | Purpose |
|------|---------|
| `ArtifactToolkit_createNewBucket` | Create artifact storage bucket |
| `ArtifactToolkit_createFile` | Create/upload a file |
| `ArtifactToolkit_readFile` | Read file content |
| `ArtifactToolkit_read_file_chunk` | Read specific lines of a file |
| `ArtifactToolkit_read_multiple_files` | Read multiple files at once |
| `ArtifactToolkit_appendData` | Append data to existing file |
| `ArtifactToolkit_overwriteData` | Replace file content |
| `ArtifactToolkit_edit_file` | Edit file with OLD/NEW markers |
| `ArtifactToolkit_deleteFile` | Delete a file |
| `ArtifactToolkit_listFiles` | List files in a bucket |
| `ArtifactToolkit_grep_file` | Search within a file |
| `ArtifactToolkit_get_file_type` | Get file type info |
| `ArtifactToolkit_list_collections` | List indexed collections |
| `ArtifactToolkit_index_data` | Index data for vector search |
| `ArtifactToolkit_search_index` | Search indexed data |
| `ArtifactToolkit_remove_index` | Remove an index |

### TestRail Toolkit (test case management)

| Tool | Purpose |
|------|---------|
| `TestRailToolkit_get_case` | Get a single test case by ID |
| `TestRailToolkit_get_cases` | Get all test cases from project/suite |
| `TestRailToolkit_get_cases_by_filter` | Filter test cases with criteria |
| `TestRailToolkit_get_suites` | List test suites in a project |
| `TestRailToolkit_update_case` | Update test case properties |
| `TestRailToolkit_index_data` | Index test cases for search |
| `TestRailToolkit_search_index` | Search indexed test cases |
| `TestRailToolkit_list_collections` | List TestRail collections |

For detailed MCP tool input schemas, example calls, and response shapes, read `references/mcp-tools-schema.md`.

---

## Workflow Guidelines

### When Creating a Pipeline

1. **Clarify requirements**: Understand inputs, outputs, integrations needed
2. **Design state**: Define all state variables with appropriate types and defaults
3. **Plan node flow**: Sketch the node sequence, branching, and loops
4. **Generate YAML**: Produce valid YAML following the schema exactly
5. **Validate**: Check entry_point references exist, all transitions resolve, state vars are defined
6. **Test incrementally**: Add one node at a time, use interrupts to inspect state

### When Debugging a Pipeline

1. **Check YAML syntax**: Indentation (spaces not tabs), quotes around special chars
2. **Verify entry_point**: Must reference an existing node ID
3. **Check transitions**: All must point to existing nodes or END
4. **Validate state**: All variables used in nodes must be defined in `state`
5. **Inspect input/output**: Ensure node I/O arrays match state variables
6. **Use interrupts**: Add `interrupt_before`/`interrupt_after` to inspect state at key points
7. **Check structured_output**: When true, code/LLM must return dict with keys matching output vars
8. **Review input_mapping**: Ensure correct types (fixed/variable/fstring) and values

### Validation Checklist

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

### Using MCP Tools for Development

- **Inspect existing pipelines**: Use `getEliteaCoreApplication` to review current configurations
- **List available tools**: Use `getEliteaCoreTools` to see what toolkits/MCPs are available in a project
- **Test tool I/O**: Use Artifact and TestRail toolkit tools directly to understand input/output shapes before wiring them into pipeline nodes
- **Deploy changes**: Use `putEliteaCoreVersion` to update pipeline YAML on the platform
- **Test execution**: Use `postEliteaCorePredict` to run an agent/pipeline version with test inputs

### Best Practices

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

### Code Node Special Capabilities

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

---

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

---

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

---

## Common Use Case Patterns

> These patterns are derived from legacy Pipeline Agent Framework use cases, **re-expressed using modern node types**.

1. **User Story Creation Workflow**: `llm` (gather info) → `agent` (aggregate content) → `agent` (draft) → `agent` (enhance) → `llm` (feedback) → `router` (approve/edit/finish) → `agent` (publish to Jira) → END
2. **Code Documentation**: `toolkit` (get file list) → `code` (iterate files) → `agent` (doc per file) → `router` (loop check) → END
3. **Master Orchestration**: `agent` (trigger Agent A) → `agent` (trigger Agent B) → END
4. **Bulk Processing with Publishing Decision**: `llm` (input) → `toolkit` (extract) → `agent` (bulk create) → `llm` (prepare) → `decision` (Jira vs Confluence) → `toolkit` (publish) → END
5. **Data Extraction Pipeline**: `toolkit` (list items) → `code` (process each) → `router` (loop) → END

---

## Quick Reference: Common Workflows

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

---

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


MODE is "default"
Project id take from .vscode/mcp.json Elitea mcp config (it url path)
