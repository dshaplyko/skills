# Pipeline YAML Schema

Complete reference for the ELITEA pipeline YAML format: top-level structure, state, all 10 modern node types, and legacy node types (reference only).

## Top-Level Structure

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

## State Configuration

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

## Node Types (10 types in 4 categories)

> **IMPORTANT:** There are two generations of pipeline node types. **Always use the current node types below when creating new pipelines.** The legacy system (`tool`, `function`, `loop`, `loop_from_tool` with inline `condition`/`decision`) is documented at the end of this file **for reference only** — do NOT use legacy nodes in new pipelines. Use their modern equivalents instead (see mapping table in the Legacy section).

### Interaction Nodes

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

### Execution Nodes

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

### Control Flow Nodes

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

### Utility Nodes

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

## Connection Rules

- **`transition`**: Simple single-target connection (most nodes)
- **`routes`** + **`condition`**: Multi-path routing (Router)
- **`nodes`** + **`description`**: LLM-powered routing (Decision)
- **`END`**: Terminate pipeline execution
- Every path must eventually reach END
- The `entry_point` can be **any node type** except `router` and `decision`
- Router nodes cannot be entry points
- Decision nodes cannot be entry points
- Decision nodes cannot chain directly to other Decision nodes

## Input Mapping Types

| Type | Purpose | Example |
|------|---------|---------|
| `fixed` | Static, unchanging value | `value: "Hello"` |
| `variable` | Reference to state variable | `value: user_input` |
| `fstring` | Template with `{var}` interpolation | `value: "Process {data}"` |

## Legacy Node Types (Pipeline Agent Framework) — REFERENCE ONLY

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

### `tool` Node — Simple entity delegation (uses LLM internally for input prep)
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

### `function` Node — Direct ELITEA entity call with explicit input mapping
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

### `loop` Node — Repeat a task for each item
```yaml
- id: <unique_id>
  type: loop
  task: "Formulate ALL file paths from chat_history as a list of inputs."
  tool: <agent_or_prompt_name>
  input: [file_listing]        # Optional but more token-efficient
  output: [results]            # Optional
  transition: <next_node_id>
```

### `loop_from_tool` Node — Iterate over dynamically generated items
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

## Legacy Inline Conditions & Decisions — REFERENCE ONLY

In the legacy framework, `condition` and `decision` are **attributes within nodes** (typically `llm` nodes), not separate node types. **For new pipelines, use `router` and `decision` nodes instead.**

### Inline Condition (within an `llm` or `function` node)
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

### Inline Decision (within an `llm` node)
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
