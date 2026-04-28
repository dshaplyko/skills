# Collection structure (quick reference)

The ELITEA REST API Postman collection (v2.1) is large: ~535 requests
across ~141 folders. This file is here so the skill doesn't waste
context reloading structural facts on every run.

## Top-level folders (with approximate request counts)

- `elitea_core`  (189) — the main surface: applications, collections,
  conversations, tools, toolkits, versions, messages, participants,
  predictions, canvases, etc. Most user-facing endpoints live here.
- `configurations` (10) — system configuration.
- `context_manager` (9) — context/state store.
- `auth` (5) — personal access tokens (`/auth/token`), current user,
  permissions. Collection-level bearer auth inheritance applies.
- `artifacts` (13) — including `s3` subfolder.
- `admin` (8) — admin-only endpoints.
- `alita_ui` (2) — UI support endpoints.
- `projects` (6) — project CRUD and groups.
- `deployments` (28) — incl. `admin`, `project`, `load models`,
  `test connections`.
- `Api Mock` (6) — mock server.
- `open_ai_azure_api` (7) — OpenAI/Azure proxy.
- `social` (17) — likes, pins, avatars.
- `secrets` (6)
- `monitoring` (12)
- `notifications` (4)
- `archive` (213) — **deprecated** endpoints: chat, datasources,
  applications, promptlib_shared, prompts prompt_lib (deprecated), flows
  (deprecated). Only surface these if the user explicitly asks, and
  warn them these are deprecated.

## Auth

The collection inherits bearer auth at the root:

```
Authorization: Bearer {{auth_token}}
```

Most individual requests do not redeclare an `auth` block; they rely on
this inheritance. A few override with a static `Authorization` header
instead. If `scripts/show.py` prints no `-- auth --` section, assume the
inherited bearer applies.

## Common {{variables}}

Appear frequently in URLs/headers and come from the user's Postman
environment, not from the collection itself:

- `{{base_url}}` — platform base, e.g. `https://nexus.elitea.ai`
- `{{full_path}}` — often `{{base_url}}{{api_path}}`
- `{{api_path}}` — defined in collection as `/api/v1`
- `{{auth_token}}` — personal access token
- `{{project_id}}`, `{{public_project_id}}` — project identifiers
- `{{project_mode}}` — defined in collection as `default`

The skill never invents values for these. It either leaves them as
`{{...}}` placeholders or substitutes values that the user explicitly
provides in the conversation.

## Postman v2.1 request shape (what show.py parses)

```
{
  "name": "...",
  "request": {
    "method": "POST",
    "url": {"raw": "...", "host": [...], "path": [...], "query": [...], "variable": [...]},
    "header": [{"key": "...", "value": "..."}],
    "auth": {"type": "bearer", "bearer": [{"key": "token", "value": "..."}]},  // optional — else inherits
    "body": {
      "mode": "raw" | "formdata" | "urlencoded" | "graphql" | "file",
      "raw": "...",                    // when mode=raw
      "formdata": [...],               // when mode=formdata
      "urlencoded": [...],
      "options": {"raw": {"language": "json"}}
    },
    "description": "markdown"
  },
  "response": [                         // saved example responses
    {"name": "...", "code": 200, "status": "OK", "body": "..."}
  ]
}
```
