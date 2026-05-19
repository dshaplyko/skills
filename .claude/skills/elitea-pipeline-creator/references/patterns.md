# Pipeline Patterns

Reusable building blocks and end-to-end pipeline shapes expressed with modern node types.

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

## Common Use Case Patterns

> These patterns are derived from legacy Pipeline Agent Framework use cases, **re-expressed using modern node types**.

1. **User Story Creation Workflow**: `llm` (gather info) → `agent` (aggregate content) → `agent` (draft) → `agent` (enhance) → `llm` (feedback) → `router` (approve/edit/finish) → `agent` (publish to Jira) → END
2. **Code Documentation**: `toolkit` (get file list) → `code` (iterate files) → `agent` (doc per file) → `router` (loop check) → END
3. **Master Orchestration**: `agent` (trigger Agent A) → `agent` (trigger Agent B) → END
4. **Bulk Processing with Publishing Decision**: `llm` (input) → `toolkit` (extract) → `agent` (bulk create) → `llm` (prepare) → `decision` (Jira vs Confluence) → `toolkit` (publish) → END
5. **Data Extraction Pipeline**: `toolkit` (list items) → `code` (process each) → `router` (loop) → END
