# Elitea Built-in MCP Tools — Schema Reference

This document defines the input schemas for all 21 built-in Elitea MCP tools so that agents can correctly prepare payloads when calling them.

---

## Table of Contents

| # | Tool Name | Method | Description |
|---|-----------|--------|-------------|
| 1 | [getAuthUser](#1-getauthuser) | GET | Get current authenticated user |
| 2 | [getProjectsProject](#2-getprojectsproject) | GET | List user projects |
| 3 | [getEliteaCoreApplication](#3-geteliteacoreapplication) | GET | Get agent details |
| 4 | [putEliteaCoreApplicationAttachmentStorage](#4-puteliteacoreapplicationattachmentstorage) | PUT | Attach/detach toolkit from agent version |
| 5 | [getEliteaCoreApplications](#5-geteliteacoreapplications) | GET | List agents with filtering & pagination |
| 6 | [postEliteaCoreApplications](#6-posteliteacoreapplications) | POST | Create a new agent |
| 7 | [putEliteaCoreAttachmentStorage](#7-puteliteacoreattachmentstorage) | PUT | Set artifact toolkit on conversation |
| 8 | [postEliteaCoreAttachments](#8-posteliteacoreattachments) | POST | Upload file attachments to conversation |
| 9 | [getEliteaCoreConversation](#9-geteliteacoreconversation) | GET | Get conversation details |
| 10 | [getEliteaCoreConversations](#10-geteliteacoreconversations) | GET | List conversations with filtering |
| 11 | [postEliteaCoreConversations](#11-posteliteacoreconversations) | POST | Create a new conversation |
| 12 | [patchEliteaCoreEntitySettings](#12-patcheliteacoreentitysettings) | PATCH | Configure participant LLM settings |
| 13 | [getEliteaCoreMessages](#13-geteliteacoremessages) | GET | Get messages from conversation |
| 14 | [postEliteaCoreMessages](#14-posteliteacoremessages) | POST | Send message and get AI response |
| 15 | [deleteEliteaCoreParticipant](#15-deleteeliteacoreparticipant) | DELETE | Remove participant from conversation |
| 16 | [postEliteaCoreParticipants](#16-posteliteacoreparticipants) | POST | Add participants to conversation |
| 17 | [postEliteaCorePredict](#17-posteliteacorepredict) | POST | Execute agent and get prediction |
| 18 | [patchEliteaCoreTool](#18-patcheliteacoretool) | PATCH | Link/unlink agent to toolkit |
| 19 | [getEliteaCoreTools](#19-geteliteacoretools) | GET | List project toolkits |
| 20 | [putEliteaCoreVersion](#20-puteliteacoreversion) | PUT | Update agent version configuration |
| 21 | [postEliteaCoreVersions](#21-posteliteacoreversions) | POST | Create new agent version |

---

## Common Path Parameters

Most `elitea_core` tools share these path segments:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `mode` | string | Yes | `"prompt_lib"` | Operating mode |
| `project_id` | integer | Yes | — | Project ID |

---

## 1. getAuthUser

> **Get current authenticated user information.**

### Schema

```json
{
  "name": "getAuthUser",
  "description": "Get current authenticated user profile including personal project ID and avatar.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode (optional)",
        "default": ""
      }
    },
    "required": []
  }
}
```

### Example Call

```json
{
  "tool": "getAuthUser",
  "arguments": {}
}
```

### Response Shape

```json
{
  "id": 42,
  "email": "user@example.com",
  "name": "John Doe",
  "personal_project_id": 7,
  "avatar": "https://provider.com/avatar.png"
}
```

---

## 2. getProjectsProject

> **List user projects**

### Schema

```json
{
  "name": "getProjectsProject",
  "description": "List projects the current user has access to.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "offset": {
        "type": "integer",
        "description": "Pagination offset (number of items to skip)",
        "default": 0
      },
      "limit": {
        "type": "integer",
        "description": "Maximum number of projects to return",
        "default": 10
      },
      "search": {
        "type": "string",
        "description": "Search query to filter projects by name"
      },
      "check_public_role": {
        "type": "boolean",
        "description": "Whether to check public role permissions"
      }
    },
    "required": []
  }
}
```

### Example Call

```json
{
  "tool": "getProjectsProject",
  "arguments": {
    "limit": 20,
    "search": "my-project"
  }
}
```

### Response Shape

```json
[
  {
    "id": 1,
    "name": "My Project",
    "description": "...",
    "created_at": "2025-01-01T00:00:00Z"
  }
]
```

---

## 3. getEliteaCoreApplication

> **Get agent (application) details including version information.**

### Schema

```json
{
  "name": "getEliteaCoreApplication",
  "description": "Get agent (application) details including version information.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "application_id": {
        "type": "integer",
        "description": "Agent (application) ID"
      },
      "version_name": {
        "type": "string",
        "description": "Specific version name to retrieve. If omitted, returns the latest version."
      }
    },
    "required": ["project_id", "application_id"]
  }
}
```

### Example Call

```json
{
  "tool": "getEliteaCoreApplication",
  "arguments": {
    "project_id": 42,
    "application_id": 101
  }
}
```

### Response Shape

```json
{
  "id": 101,
  "name": "My Agent",
  "description": "...",
  "owner_id": 1,
  "created_at": "2025-01-01T00:00:00Z",
  "version_details": {
    "id": 200,
    "name": "latest",
    "status": "published",
    "agent_type": "react",
    "model_settings": {},
    "instructions": "...",
    "variables": [],
    "tags": [],
    "tools": []
  }
}
```

---

## 4. putEliteaCoreApplicationAttachmentStorage

> **Attach or detach a toolkit from an agent version.**

### Schema

```json
{
  "name": "putEliteaCoreApplicationAttachmentStorage",
  "description": "Attach or detach an artifact toolkit from an agent version.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "application_id": {
        "type": "integer",
        "description": "Agent (application) ID"
      },
      "version_id": {
        "type": "integer",
        "description": "Agent version ID"
      },
      "toolkit_id": {
        "type": "integer",
        "description": "Toolkit ID to attach. Pass null to detach."
      }
    },
    "required": ["project_id", "application_id", "version_id", "toolkit_id"]
  }
}
```

### Example Call

```json
{
  "tool": "putEliteaCoreApplicationAttachmentStorage",
  "arguments": {
    "project_id": 42,
    "application_id": 101,
    "version_id": 200,
    "toolkit_id": 55
  }
}
```

### Response Shape

Returns the updated `ApplicationVersionDetail` object.

---

## 5. getEliteaCoreApplications

> **Get agents (applications) with filtering, sorting, and pagination.**

### Schema

```json
{
  "name": "getEliteaCoreApplications",
  "description": "Get agents (applications) with filtering, sorting, and pagination.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "query": {
        "type": "string",
        "description": "Search query to filter agents by name"
      },
      "tags": {
        "type": "string",
        "description": "Comma-separated tag IDs to filter by"
      },
      "author_id": {
        "type": "integer",
        "description": "Filter by author user ID"
      },
      "limit": {
        "type": "integer",
        "description": "Maximum number of results to return",
        "default": 10
      },
      "offset": {
        "type": "integer",
        "description": "Pagination offset",
        "default": 0
      },
      "sort_by": {
        "type": "string",
        "description": "Field to sort by",
        "default": "created_at",
        "enum": ["created_at", "updated_at", "name"]
      },
      "sort_order": {
        "type": "string",
        "description": "Sort direction",
        "default": "desc",
        "enum": ["asc", "desc"]
      },
      "statuses": {
        "type": "string",
        "description": "Comma-separated status filter (e.g. 'published,draft')"
      },
      "my_liked": {
        "type": "boolean",
        "description": "Filter to only agents the current user has liked",
        "default": false
      },
      "agents_type": {
        "type": "string",
        "description": "Filter by agent type"
      },
      "collection_id": {
        "type": "integer",
        "description": "Filter by collection ID"
      },
      "without_tags": {
        "type": "boolean",
        "description": "Filter to agents without any tags",
        "default": false
      },
      "trend_start_period": {
        "type": "string",
        "description": "Start date for trend calculation (ISO format)"
      },
      "trend_end_period": {
        "type": "string",
        "description": "End date for trend calculation (ISO format)"
      }
    },
    "required": ["project_id"]
  }
}
```

### Example Call

```json
{
  "tool": "getEliteaCoreApplications",
  "arguments": {
    "project_id": 42,
    "query": "customer-support",
    "limit": 5,
    "sort_by": "updated_at",
    "sort_order": "desc"
  }
}
```

### Response Shape

```json
{
  "total": 25,
  "rows": [
    {
      "id": 101,
      "name": "Customer Support Agent",
      "description": "...",
      "owner_id": 1,
      "status": "published",
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-06-15T12:00:00Z",
      "tags": [{ "id": 1, "name": "support" }],
      "likes": 5
    }
  ]
}
```

---

## 6. postEliteaCoreApplications

> **Create a new agent (application) with initial version and configuration.**

### Schema

```json
{
  "name": "postEliteaCoreApplications",
  "description": "Create a new agent (application) with initial version and configuration.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "name": {
        "type": "string",
        "description": "Agent name (minimum 1 character)",
        "minLength": 1
      },
      "description": {
        "type": "string",
        "description": "Agent description"
      },
      "versions": {
        "type": "array",
        "description": "Initial version configuration (exactly 1 element required)",
        "items": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "Version name (e.g. 'latest')"
            },
            "agent_type": {
              "type": "string",
              "description": "Agent type",
              "enum": ["openai", "react", "alita", "dial", "codemie", "raw", "autogen", "llama", "pipeline", "xml"]
            },
            "instructions": {
              "type": "string",
              "description": "System instructions for the agent"
            },
            "model_settings": {
              "type": "object",
              "description": "LLM model configuration",
              "properties": {
                "model_name": { "type": "string" },
                "temperature": { "type": "number" },
                "max_tokens": { "type": "integer" }
              }
            },
            "variables": {
              "type": "array",
              "description": "Template variables",
              "items": {
                "type": "object",
                "properties": {
                  "name": { "type": "string" },
                  "value": { "type": "string" }
                }
              }
            },
            "tags": {
              "type": "array",
              "description": "Tag IDs to assign",
              "items": { "type": "integer" }
            }
          }
        },
        "minItems": 1,
        "maxItems": 1
      },
      "webhook_secret": {
        "type": "string",
        "description": "Webhook secret for external integrations"
      },
      "meta": {
        "type": "object",
        "description": "Additional metadata"
      }
    },
    "required": ["project_id", "name", "versions"]
  }
}
```

### Example Call

```json
{
  "tool": "postEliteaCoreApplications",
  "arguments": {
    "project_id": 42,
    "name": "My New Agent",
    "description": "A helpful assistant agent",
    "versions": [
      {
        "name": "latest",
        "agent_type": "react",
        "instructions": "You are a helpful assistant.",
        "model_settings": {
          "model_name": "gpt-4o",
          "temperature": 0.7,
          "max_tokens": 4096
        }
      }
    ]
  }
}
```

### Response Shape

Returns the created `ApplicationDetail` with embedded `version_details` (HTTP 201).

---

## 7. putEliteaCoreAttachmentStorage

> **Set or remove the artifact toolkit on a conversation.**

### Schema

```json
{
  "name": "putEliteaCoreAttachmentStorage",
  "description": "Set or remove the artifact toolkit on a conversation.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "conversation_id": {
        "type": "integer",
        "description": "Conversation ID"
      },
      "toolkit_id": {
        "type": ["integer", "null"],
        "description": "Toolkit ID to set. Pass null to detach the current toolkit."
      }
    },
    "required": ["project_id", "conversation_id", "toolkit_id"]
  }
}
```

### Example Call

```json
{
  "tool": "putEliteaCoreAttachmentStorage",
  "arguments": {
    "project_id": 42,
    "conversation_id": 300,
    "toolkit_id": 55
  }
}
```

### Response Shape

- **200**: Returns `ParticipantDetails` when attaching.
- **204**: Returns `{}` when detaching (`toolkit_id: null`).

---

## 8. postEliteaCoreAttachments

> **Upload file attachments to a conversation.**

### Schema

```json
{
  "name": "postEliteaCoreAttachments",
  "description": "Upload file attachments to a conversation.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "conversation_id": {
        "type": "integer",
        "description": "Conversation ID to attach files to"
      },
      "file": {
        "type": "string",
        "format": "binary",
        "description": "File content to upload (multipart/form-data)"
      },
      "overwrite_attachments": {
        "type": "integer",
        "description": "Set to 1 to overwrite existing attachments with the same name",
        "enum": [0, 1],
        "default": 0
      },
      "file_id": {
        "type": "string",
        "description": "Unique upload session ID (for chunked uploads only)"
      },
      "chunk_index": {
        "type": "integer",
        "description": "0-based chunk index (for chunked uploads only)"
      },
      "total_chunks": {
        "type": "integer",
        "description": "Total number of chunks (for chunked uploads only)"
      },
      "file_name": {
        "type": "string",
        "description": "Original file name (for chunked uploads only)"
      }
    },
    "required": ["project_id", "conversation_id", "file"]
  }
}
```

### Example Call

```json
{
  "tool": "postEliteaCoreAttachments",
  "arguments": {
    "project_id": 42,
    "conversation_id": 300,
    "file": "<binary file data>",
    "overwrite_attachments": 1
  }
}
```

### Response Shape

```json
[
  {
    "filepath": "/bucket-name/uploaded-file.pdf",
    "file_size": 102400
  }
]
```

---

## 9. getEliteaCoreConversation

> **Get detailed information about a specific conversation.**

### Schema

```json
{
  "name": "getEliteaCoreConversation",
  "description": "Get detailed information about a specific conversation.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "conversation_id": {
        "type": "integer",
        "description": "Conversation ID"
      }
    },
    "required": ["project_id", "conversation_id"]
  }
}
```

### Example Call

```json
{
  "tool": "getEliteaCoreConversation",
  "arguments": {
    "project_id": 42,
    "conversation_id": 300
  }
}
```

### Response Shape

```json
{
  "id": 300,
  "name": "Support Chat #1",
  "is_private": true,
  "author_id": 5,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T11:00:00Z",
  "meta": {},
  "source": "alita",
  "attachment_participant_id": null,
  "instructions": "",
  "uuid": "a1b2c3d4-e5f6-...",
  "participants": [
    {
      "id": 1,
      "participant_type": "user",
      "entity_settings": {}
    }
  ],
  "message_groups_count": 12,
  "message_groups": []
}
```

---

## 10. getEliteaCoreConversations

> **Get list of conversations with filtering, sorting, and pagination.**

### Schema

```json
{
  "name": "getEliteaCoreConversations",
  "description": "Get list of conversations with filtering, sorting, and pagination.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "query": {
        "type": "string",
        "description": "Search query to filter conversations by name"
      },
      "source": {
        "type": "string",
        "description": "Comma-separated source filter",
        "default": "alita"
      },
      "limit": {
        "type": "integer",
        "description": "Maximum number of results",
        "default": 10
      },
      "offset": {
        "type": "integer",
        "description": "Pagination offset",
        "default": 0
      },
      "sort_by": {
        "type": "string",
        "description": "Field to sort by",
        "default": "created_at"
      },
      "sort_order": {
        "type": "string",
        "description": "Sort direction",
        "default": "desc",
        "enum": ["asc", "desc"]
      },
      "entity_name": {
        "type": "string",
        "description": "Filter by associated entity name"
      },
      "entity_meta_id": {
        "type": "integer",
        "description": "Filter by associated entity meta ID"
      },
      "entity_meta_project_id": {
        "type": "integer",
        "description": "Filter by entity's source project ID"
      }
    },
    "required": ["project_id"]
  }
}
```

### Example Call

```json
{
  "tool": "getEliteaCoreConversations",
  "arguments": {
    "project_id": 42,
    "query": "support",
    "limit": 20,
    "sort_order": "desc"
  }
}
```

### Response Shape

```json
{
  "total": 50,
  "rows": [
    {
      "id": 300,
      "name": "Support Chat #1",
      "is_private": true,
      "author_id": 5,
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T11:00:00Z",
      "source": "alita",
      "participants_count": 2,
      "message_groups_count": 12,
      "users_count": 1,
      "duration": 1800.5
    }
  ]
}
```

---

## 11. postEliteaCoreConversations

> **Create a new conversation for chat interactions.**

### Schema

```json
{
  "name": "postEliteaCoreConversations",
  "description": "Create a new conversation for chat interactions.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "name": {
        "type": "string",
        "description": "Conversation name (3-character minimum)",
        "minLength": 3
      },
      "is_private": {
        "type": "boolean",
        "description": "Whether the conversation is private",
        "default": true
      },
      "participants": {
        "type": "array",
        "description": "Initial participants to add to the conversation",
        "items": {
          "type": "object",
          "properties": {
            "participant_type": {
              "type": "string",
              "description": "Type of participant (e.g. 'application', 'prompt')"
            },
            "entity_id": {
              "type": "integer",
              "description": "Entity ID for the participant"
            },
            "entity_settings": {
              "type": "object",
              "description": "Settings for this participant"
            }
          }
        },
        "default": []
      },
      "source": {
        "type": "string",
        "description": "Source identifier for the conversation",
        "default": "alita"
      },
      "meta": {
        "type": "object",
        "description": "Additional metadata for the conversation",
        "default": {}
      },
      "instructions": {
        "type": "string",
        "description": "System instructions for the conversation",
        "default": ""
      }
    },
    "required": ["project_id", "name"]
  }
}
```

### Example Call

```json
{
  "tool": "postEliteaCoreConversations",
  "arguments": {
    "project_id": 42,
    "name": "New Support Chat",
    "is_private": true,
    "participants": [
      {
        "participant_type": "application",
        "entity_id": 101,
        "entity_settings": {
          "version_id": 200
        }
      }
    ]
  }
}
```

### Response Shape

Returns the created `ConversationDetails` object (HTTP 201). Same shape as [getEliteaCoreConversation](#9-geteliteacoreconversation) response.

---

## 12. patchEliteaCoreEntitySettings

> **Configure participant settings (LLM settings, etc.) in a conversation.**

### Schema

```json
{
  "name": "patchEliteaCoreEntitySettings",
  "description": "Configure participant settings (LLM settings, etc.) in a conversation.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "conversation_id": {
        "type": "integer",
        "description": "Conversation ID"
      },
      "participant_id": {
        "type": "integer",
        "description": "Participant ID. If omitted, applies to the current user's participant."
      },
      "llm_settings": {
        "type": "object",
        "description": "LLM configuration (for LLM-type participants)",
        "properties": {
          "model_name": {
            "type": "string",
            "description": "Model identifier (e.g. 'gpt-4o', 'claude-sonnet-4-20250514')"
          },
          "model_project_id": {
            "type": "integer",
            "description": "Project ID where the model is configured"
          },
          "temperature": {
            "type": "number",
            "description": "Sampling temperature (0.0 - 2.0)"
          },
          "max_tokens": {
            "type": "integer",
            "description": "Maximum tokens in response"
          },
          "reasoning_effort": {
            "type": "string",
            "description": "Reasoning effort level",
            "enum": ["low", "medium", "high"]
          },
          "chat_history_template": {
            "description": "Chat history strategy: 'all' (full history), 'context_managed' (auto-managed), or integer (last N messages)",
            "oneOf": [
              { "type": "string", "enum": ["all", "context_managed"] },
              { "type": "integer" }
            ],
            "default": "all"
          }
        }
      },
      "version_id": {
        "type": "integer",
        "description": "Agent version ID (for application-type participants, aliased as 'id')"
      },
      "variables": {
        "type": "array",
        "description": "Override variables for the agent version",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "value": { "type": "string" }
          }
        },
        "default": []
      },
      "icon_meta": {
        "type": "object",
        "description": "Icon metadata for application participant",
        "default": {}
      }
    },
    "required": ["project_id", "conversation_id"]
  }
}
```

### Example Call — Configure LLM

```json
{
  "tool": "patchEliteaCoreEntitySettings",
  "arguments": {
    "project_id": 42,
    "conversation_id": 300,
    "llm_settings": {
      "model_name": "gpt-4o",
      "temperature": 0.5,
      "max_tokens": 8192
    }
  }
}
```

### Example Call — Configure Agent Participant

```json
{
  "tool": "patchEliteaCoreEntitySettings",
  "arguments": {
    "project_id": 42,
    "conversation_id": 300,
    "participant_id": 15,
    "version_id": 200,
    "variables": [
      { "name": "tone", "value": "formal" }
    ],
    "chat_history_template": "context_managed"
  }
}
```

### Response Shape

Returns the updated participant object with `entity_settings` (HTTP 200).

---

## 13. getEliteaCoreMessages

> **Get messages from a conversation with filtering and pagination.**

### Schema

```json
{
  "name": "getEliteaCoreMessages",
  "description": "Get messages from a conversation with filtering and pagination.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "conversation_id": {
        "type": "integer",
        "description": "Conversation ID"
      },
      "query": {
        "type": "string",
        "description": "Search query to filter messages by text content"
      },
      "limit": {
        "type": "integer",
        "description": "Maximum number of message groups to return",
        "default": 10
      },
      "offset": {
        "type": "integer",
        "description": "Pagination offset",
        "default": 0
      },
      "sort_by": {
        "type": "string",
        "description": "Field to sort by",
        "default": "created_at"
      },
      "sort_order": {
        "type": "string",
        "description": "Sort direction",
        "default": "desc",
        "enum": ["asc", "desc"]
      }
    },
    "required": ["project_id", "conversation_id"]
  }
}
```

### Example Call

```json
{
  "tool": "getEliteaCoreMessages",
  "arguments": {
    "project_id": 42,
    "conversation_id": 300,
    "limit": 20,
    "sort_order": "asc"
  }
}
```

### Response Shape

```json
{
  "total": 24,
  "rows": [
    {
      "id": 500,
      "uuid": "msg-uuid-...",
      "author_participant_id": 1,
      "meta": {},
      "created_at": "2025-01-15T10:31:00Z",
      "sent_to": { "id": 2, "participant_type": "application" },
      "is_streaming": false,
      "task_id": null,
      "message_items": [
        {
          "id": 600,
          "uuid": "item-uuid-...",
          "order_index": 0,
          "item_type": "text_message",
          "item_details": {
            "content": "Hello, how can I help you?"
          },
          "meta": {}
        }
      ]
    }
  ]
}
```

### Message Item Types

| `item_type` | `item_details` shape |
|-------------|---------------------|
| `text_message` | `{ "content": "..." }` |
| `canvas_message` | `{ "content": "...", "language": "python", "title": "..." }` |
| `attachment_message` | `{ "filepath": "/bucket/file.pdf", "file_size": 1024 }` |

---

## 14. postEliteaCoreMessages

> **Send a message to a conversation and get AI response.**

### Schema

```json
{
  "name": "postEliteaCoreMessages",
  "description": "Send a message to a conversation and get AI response.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "conversation_uuid": {
        "type": "string",
        "format": "uuid",
        "description": "Conversation UUID (NOTE: this is the UUID, not the integer ID)"
      },
      "user_input": {
        "type": "string",
        "description": "The user's message text. Required if tool_call_input is not provided."
      },
      "participant_id": {
        "type": "integer",
        "description": "Target participant ID to send the message to. If omitted with llm_settings, performs a direct LLM predict."
      },
      "tool_call_input": {
        "type": "object",
        "description": "Tool call payload (alternative to user_input for tool invocations)",
        "properties": {
          "tool_name": { "type": "string" },
          "tool_args": { "type": "object" }
        }
      },
      "await_task_timeout": {
        "type": "integer",
        "description": "Seconds to wait for AI response before returning async. Range: -1 (no wait) to 300. Default: 30.",
        "default": 30,
        "minimum": -1,
        "maximum": 300
      },
      "attachments_info": {
        "type": "array",
        "description": "File attachments to include with the message",
        "items": {
          "type": "object",
          "properties": {
            "filepath": {
              "type": "string",
              "description": "File path in format /{bucket}/{filename}"
            },
            "file_size": {
              "type": "integer",
              "description": "File size in bytes",
              "default": 0
            }
          },
          "required": ["filepath"]
        }
      },
      "llm_settings": {
        "type": "object",
        "description": "LLM settings (required when participant_id is null for direct LLM predict)",
        "properties": {
          "model_name": { "type": "string" },
          "temperature": { "type": "number" },
          "max_tokens": { "type": "integer" }
        }
      },
      "return_task_id": {
        "type": "boolean",
        "description": "If true, returns a task_id immediately instead of waiting for the response",
        "default": false
      }
    },
    "required": ["project_id", "conversation_uuid"]
  }
}
```

### Example Call — Send to Agent

```json
{
  "tool": "postEliteaCoreMessages",
  "arguments": {
    "project_id": 42,
    "conversation_uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "participant_id": 15,
    "user_input": "Summarize the latest sales report",
    "await_task_timeout": 60
  }
}
```

### Example Call — Direct LLM Predict

```json
{
  "tool": "postEliteaCoreMessages",
  "arguments": {
    "project_id": 42,
    "conversation_uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "user_input": "Translate this to French: Hello world",
    "llm_settings": {
      "model_name": "gpt-4o",
      "temperature": 0.3,
      "max_tokens": 1024
    }
  }
}
```

### Example Call — With Attachments

```json
{
  "tool": "postEliteaCoreMessages",
  "arguments": {
    "project_id": 42,
    "conversation_uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "participant_id": 15,
    "user_input": "Analyze the attached document",
    "attachments_info": [
      {
        "filepath": "/my-bucket/report.pdf",
        "file_size": 204800
      }
    ]
  }
}
```

### Response Shape

**HTTP 201** — Synchronous response (completed within timeout):
```json
{
  "message_groups": [
    {
      "id": 501,
      "uuid": "user-msg-uuid",
      "author_participant_id": 1,
      "message_items": [{ "item_type": "text_message", "item_details": { "content": "Summarize..." } }]
    },
    {
      "id": 502,
      "uuid": "ai-msg-uuid",
      "author_participant_id": 15,
      "message_items": [{ "item_type": "text_message", "item_details": { "content": "Here is the summary..." } }]
    }
  ]
}
```

**HTTP 202** — Still processing (response not ready within timeout):
```json
{
  "message_groups": [
    { "id": 501, "message_items": [{ "...": "user message" }] },
    { "id": 502, "is_streaming": true, "message_items": [] }
  ]
}
```

**HTTP 200** — When `return_task_id: true`:
```json
{
  "task_id": "celery-task-id-string"
}
```

---

## 15. deleteEliteaCoreParticipant

> **Remove a participant from a conversation.**

### Schema

```json
{
  "name": "deleteEliteaCoreParticipant",
  "description": "Remove a participant from a conversation.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "conversation_id": {
        "type": "integer",
        "description": "Conversation ID"
      },
      "participant_id": {
        "type": "integer",
        "description": "Participant ID to remove from the conversation"
      }
    },
    "required": ["project_id", "conversation_id", "participant_id"]
  }
}
```

### Example Call

```json
{
  "tool": "deleteEliteaCoreParticipant",
  "arguments": {
    "project_id": 42,
    "conversation_id": 300,
    "participant_id": 15
  }
}
```

### Response Shape

- **200/204**: Confirmation of deletion.
- **400**: `{"error": "..."}` if participant not found or cannot be removed.

---

## 16. postEliteaCoreParticipants

> **Add participants (users, agents, toolkits) to a conversation.**

### Schema

```json
{
  "name": "postEliteaCoreParticipants",
  "description": "Add participants (users, agents, toolkits) to a conversation.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "conversation_id": {
        "type": "integer",
        "description": "Conversation ID to add participants to"
      },
      "participants": {
        "type": "array",
        "description": "List of participants to add (or a single participant object)",
        "items": {
          "type": "object",
          "properties": {
            "entity_name": {
              "type": "string",
              "description": "Participant type",
              "enum": ["user", "llm", "datasource", "application", "toolkit", "dummy"]
            },
            "entity_meta": {
              "type": "object",
              "description": "Type-specific metadata (see entity_meta table below)"
            },
            "entity_settings": {
              "type": "object",
              "description": "Optional extra settings for the participant",
              "default": {}
            }
          },
          "required": ["entity_name", "entity_meta"]
        }
      }
    },
    "required": ["project_id", "conversation_id", "participants"]
  }
}
```

### entity_meta by participant type

| `entity_name` | `entity_meta` fields |
|---------------|---------------------|
| `user` | `{ "id": <user_id> }` |
| `llm` | `{ "model_name": "<model>" }` |
| `datasource` | `{ "id": <datasource_id>, "project_id": <project_id> }` |
| `application` | `{ "id": <application_id>, "project_id": <project_id> }` |
| `toolkit` | `{ "id": <toolkit_id>, "project_id": <project_id> }` |
| `dummy` | `{}` |

### Example Call — Add an Agent

```json
{
  "tool": "postEliteaCoreParticipants",
  "arguments": {
    "project_id": 42,
    "conversation_id": 300,
    "participants": [
      {
        "entity_name": "application",
        "entity_meta": {
          "id": 101,
          "project_id": 42
        },
        "entity_settings": {
          "version_id": 200
        }
      }
    ]
  }
}
```

### Example Call — Add an LLM

```json
{
  "tool": "postEliteaCoreParticipants",
  "arguments": {
    "project_id": 42,
    "conversation_id": 300,
    "participants": [
      {
        "entity_name": "llm",
        "entity_meta": {
          "model_name": "gpt-4o"
        }
      }
    ]
  }
}
```

### Response Shape

**HTTP 200**: List of created participant detail objects:
```json
[
  {
    "id": 12,
    "entity_name": "application",
    "entity_meta": { "id": 101, "project_id": 42 },
    "meta": {},
    "entity_settings": {}
  }
]
```

---

## 17. postEliteaCorePredict

> **Execute an agent (application version) with provided inputs and get predictions.**

### Schema

```json
{
  "name": "postEliteaCorePredict",
  "description": "Execute an agent (application version) with provided inputs and get predictions.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "version_id": {
        "type": "integer",
        "description": "Application version ID to execute"
      },
      "user_input": {
        "type": ["string", "array"],
        "description": "User message or prompt input"
      },
      "chat_history": {
        "type": "array",
        "description": "Prior conversation history",
        "items": {
          "type": "object",
          "properties": {
            "role": {
              "type": "string",
              "description": "Message role",
              "enum": ["user", "assistant"]
            },
            "content": {
              "type": ["string", "array"],
              "description": "Message content"
            }
          },
          "required": ["role", "content"]
        },
        "default": []
      },
      "instructions": {
        "type": "string",
        "description": "Override agent system instructions"
      },
      "variables": {
        "type": "array",
        "description": "Template variables to substitute",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "value": { "type": "string" }
          }
        }
      },
      "llm_settings": {
        "type": "object",
        "description": "Override LLM parameters",
        "properties": {
          "model_name": { "type": "string" },
          "temperature": { "type": "number", "description": "0.0 - 1.0" },
          "max_tokens": { "type": "integer" },
          "reasoning_effort": { "type": "string", "enum": ["low", "medium", "high"] },
          "model_project_id": { "type": "integer" }
        }
      },
      "tools": {
        "type": "array",
        "description": "Override tools for this execution",
        "items": { "type": "object" },
        "default": []
      },
      "thread_id": {
        "type": "string",
        "description": "Thread ID for multi-turn conversations"
      },
      "checkpoint_id": {
        "type": "string",
        "description": "Checkpoint ID to resume from"
      },
      "conversation_id": {
        "type": "string",
        "description": "Conversation UUID for context"
      },
      "should_continue": {
        "type": "boolean",
        "description": "Whether to continue a previous execution",
        "default": false
      },
      "meta": {
        "type": "object",
        "description": "Additional metadata",
        "default": {}
      },
      "callback_url": {
        "type": "string",
        "description": "Webhook URL for async result delivery"
      },
      "callback_headers": {
        "type": "object",
        "description": "Headers to include in callback webhook request"
      },
      "async": {
        "type": "string",
        "description": "Set to 'yes' or 'true' for async execution (query parameter)",
        "default": "no"
      }
    },
    "required": ["project_id", "version_id"]
  }
}
```

### Example Call — Simple Predict

```json
{
  "tool": "postEliteaCorePredict",
  "arguments": {
    "project_id": 42,
    "version_id": 200,
    "user_input": "What is the weather in Paris?"
  }
}
```

### Example Call — With History & Overrides

```json
{
  "tool": "postEliteaCorePredict",
  "arguments": {
    "project_id": 42,
    "version_id": 200,
    "user_input": "Now tell me about London",
    "chat_history": [
      { "role": "user", "content": "What is the weather in Paris?" },
      { "role": "assistant", "content": "Paris is currently 18C and sunny." }
    ],
    "llm_settings": {
      "temperature": 0.3,
      "max_tokens": 2048
    },
    "variables": [
      { "name": "language", "value": "English" }
    ]
  }
}
```

### Example Call — Async with Callback

```json
{
  "tool": "postEliteaCorePredict",
  "arguments": {
    "project_id": 42,
    "version_id": 200,
    "user_input": "Generate a full report",
    "async": "yes",
    "callback_url": "https://my-service.com/webhook/result",
    "callback_headers": { "Authorization": "Bearer token123" }
  }
}
```

### Response Shape

**Synchronous (HTTP 200)**:
```json
{
  "result": "Agent response text...",
  "task_id": "abc123",
  "error": null
}
```

**Async (HTTP 200)**:
```json
{
  "task_id": "abc123",
  "result": null
}
```

---

## 18. patchEliteaCoreTool

> **Link an agent (application) to a toolkit.**

### Schema

```json
{
  "name": "patchEliteaCoreTool",
  "description": "Link or unlink an agent (application version) to/from a toolkit.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "tool_id": {
        "type": "integer",
        "description": "Toolkit ID to link/unlink"
      },
      "entity_id": {
        "type": "integer",
        "description": "Application (agent) ID to link to the toolkit"
      },
      "entity_version_id": {
        "type": "integer",
        "description": "Application version ID to link"
      },
      "entity_type": {
        "type": "string",
        "description": "Entity type",
        "enum": ["agent", "datasource"]
      },
      "has_relation": {
        "type": "boolean",
        "description": "true to add the link, false to remove it",
        "default": false
      },
      "selected_tools": {
        "type": "array",
        "description": "List of specific tool names to allow from this toolkit. If null, all tools are available.",
        "items": { "type": "string" }
      }
    },
    "required": ["project_id", "tool_id", "entity_id", "entity_version_id", "entity_type"]
  }
}
```

### Example Call — Link Toolkit to Agent

```json
{
  "tool": "patchEliteaCoreTool",
  "arguments": {
    "project_id": 42,
    "tool_id": 55,
    "entity_id": 101,
    "entity_version_id": 200,
    "entity_type": "agent",
    "has_relation": true,
    "selected_tools": ["create_issue", "list_issues"]
  }
}
```

### Example Call — Unlink Toolkit

```json
{
  "tool": "patchEliteaCoreTool",
  "arguments": {
    "project_id": 42,
    "tool_id": 55,
    "entity_id": 101,
    "entity_version_id": 200,
    "entity_type": "agent",
    "has_relation": false
  }
}
```

### Response Shape

**HTTP 201**: Updated toolkit relation data.

---

## 19. getEliteaCoreTools

> **Get project toolkits with tools, supporting filtering and pagination.**

### Schema

```json
{
  "name": "getEliteaCoreTools",
  "description": "Get project toolkits with tools, supporting filtering and pagination.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "query": {
        "type": "string",
        "description": "Text search filter for toolkit names"
      },
      "limit": {
        "type": "integer",
        "description": "Maximum number of results",
        "default": 10
      },
      "offset": {
        "type": "integer",
        "description": "Pagination offset",
        "default": 0
      },
      "sort_by": {
        "type": "string",
        "description": "Field to sort by",
        "default": "created_at"
      },
      "sort_order": {
        "type": "string",
        "description": "Sort direction",
        "default": "desc",
        "enum": ["asc", "desc"]
      },
      "toolkit_type": {
        "type": "string",
        "description": "Filter by toolkit type(s) — can be repeated for multiple types"
      },
      "mcp": {
        "type": "boolean",
        "description": "Filter to MCP toolkits only",
        "default": false
      },
      "application": {
        "type": "boolean",
        "description": "Filter to application-type toolkits only",
        "default": false
      },
      "author_id": {
        "type": "integer",
        "description": "Filter by author user ID"
      },
      "search_artifact": {
        "type": "string",
        "description": "Search within artifact content"
      }
    },
    "required": ["project_id"]
  }
}
```

### Example Call

```json
{
  "tool": "getEliteaCoreTools",
  "arguments": {
    "project_id": 42,
    "query": "github",
    "limit": 10
  }
}
```

### Response Shape

```json
{
  "total": 15,
  "rows": [
    {
      "id": 55,
      "type": "github",
      "name": "My GitHub Toolkit",
      "description": "GitHub integration toolkit",
      "author_id": 42,
      "settings": {},
      "meta": {},
      "toolkit_name": "MyGitHubToolkit",
      "author": { "id": 42, "name": "John Doe", "email": "john@example.com" },
      "created_at": "2025-01-01T00:00:00",
      "online": true,
      "icon_meta": null,
      "variables": [],
      "is_pinned": false
    }
  ]
}
```

---

## 20. putEliteaCoreVersion

> **Update an existing agent version configuration.**

### Schema

```json
{
  "name": "putEliteaCoreVersion",
  "description": "Update an existing agent version configuration.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "application_id": {
        "type": "integer",
        "description": "Agent (application) ID"
      },
      "version_id": {
        "type": "integer",
        "description": "Version ID to update"
      },
      "name": {
        "type": "string",
        "description": "Version name (minimum 1 character)",
        "minLength": 1
      },
      "agent_type": {
        "type": "string",
        "description": "Agent type",
        "enum": ["openai", "react", "alita", "dial", "codemie", "raw", "autogen", "llama", "pipeline", "xml"],
        "default": "openai"
      },
      "instructions": {
        "type": "string",
        "description": "Agent system prompt. Must be valid YAML if agent_type is 'pipeline'."
      },
      "llm_settings": {
        "type": "object",
        "description": "LLM model configuration",
        "properties": {
          "model_name": { "type": "string" },
          "temperature": { "type": "number" },
          "max_tokens": { "type": "integer" },
          "reasoning_effort": { "type": "string", "enum": ["low", "medium", "high"] },
          "model_project_id": { "type": "integer" }
        }
      },
      "variables": {
        "type": "array",
        "description": "Template variables",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "value": { "type": "string" }
          }
        }
      },
      "tools": {
        "type": "array",
        "description": "Tools attached to this version",
        "items": { "type": "object" }
      },
      "tags": {
        "type": "array",
        "description": "Tags for this version",
        "items": {
          "type": "object",
          "properties": {
            "id": { "type": "integer" },
            "name": { "type": "string" }
          }
        }
      },
      "welcome_message": {
        "type": "string",
        "description": "Welcome message shown when conversation starts"
      },
      "conversation_starters": {
        "type": "array",
        "description": "Suggested conversation starters",
        "items": { "type": "string" }
      },
      "pipeline_settings": {
        "type": "object",
        "description": "Pipeline-specific settings (for pipeline agent_type)",
        "default": {}
      },
      "meta": {
        "type": "object",
        "description": "Version metadata. Supports 'step_limit' (default 25), 'attachment_toolkit_id', 'icon_meta'.",
        "default": {}
      }
    },
    "required": ["project_id", "application_id", "version_id", "name"]
  }
}
```

### Example Call

```json
{
  "tool": "putEliteaCoreVersion",
  "arguments": {
    "project_id": 42,
    "application_id": 101,
    "version_id": 200,
    "name": "v2",
    "instructions": "You are an updated helpful assistant with code review capabilities.",
    "llm_settings": {
      "model_name": "gpt-4o",
      "temperature": 0.5,
      "max_tokens": 8192
    },
    "variables": [
      { "name": "language", "value": "English" }
    ],
    "meta": {
      "step_limit": 30
    }
  }
}
```

### Response Shape

**HTTP 201**: Updated version detail object:
```json
{
  "id": 200,
  "name": "v2",
  "status": "draft",
  "created_at": "2025-01-01T00:00:00",
  "author_id": 42,
  "author": { "id": 42, "name": "John Doe", "email": "john@example.com" },
  "instructions": "You are an updated helpful assistant...",
  "llm_settings": { "model_name": "gpt-4o", "temperature": 0.5, "max_tokens": 8192 },
  "tools": [],
  "variables": [{ "name": "language", "value": "English" }],
  "tags": [],
  "meta": { "step_limit": 30 },
  "agent_type": "openai",
  "welcome_message": null,
  "conversation_starters": null,
  "pipeline_settings": {},
  "is_forked": false,
  "icon_meta": {}
}
```

---

## 21. postEliteaCoreVersions

> **Create a new version for an existing agent (application).**

### Schema

```json
{
  "name": "postEliteaCoreVersions",
  "description": "Create a new version for an existing agent (application).",
  "inputSchema": {
    "type": "object",
    "properties": {
      "mode": {
        "type": "string",
        "description": "Operating mode",
        "default": "prompt_lib"
      },
      "project_id": {
        "type": "integer",
        "description": "Project ID"
      },
      "application_id": {
        "type": "integer",
        "description": "Agent (application) ID to create a version for"
      },
      "name": {
        "type": "string",
        "description": "Version name (minimum 1 character, cannot be 'base')",
        "minLength": 1
      },
      "agent_type": {
        "type": "string",
        "description": "Agent type",
        "enum": ["openai", "react", "alita", "dial", "codemie", "raw", "autogen", "llama", "pipeline", "xml"],
        "default": "openai"
      },
      "instructions": {
        "type": "string",
        "description": "Agent system prompt. Must be valid YAML if agent_type is 'pipeline'."
      },
      "llm_settings": {
        "type": "object",
        "description": "LLM model configuration",
        "properties": {
          "model_name": { "type": "string" },
          "temperature": { "type": "number" },
          "max_tokens": { "type": "integer" },
          "reasoning_effort": { "type": "string", "enum": ["low", "medium", "high"] },
          "model_project_id": { "type": "integer" }
        }
      },
      "variables": {
        "type": "array",
        "description": "Template variables",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "value": { "type": "string" }
          }
        }
      },
      "tools": {
        "type": "array",
        "description": "Tools to attach to this version",
        "items": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "Tool name (minimum 1 character)"
            },
            "type": {
              "type": "string",
              "description": "Toolkit type (e.g. 'github', 'jira', 'openapi')"
            },
            "description": {
              "type": "string",
              "description": "Tool description"
            },
            "settings": {
              "type": "object",
              "description": "Type-specific tool settings",
              "default": {}
            },
            "meta": {
              "type": "object",
              "description": "Tool metadata",
              "default": {}
            }
          },
          "required": ["name", "type"]
        }
      },
      "tags": {
        "type": "array",
        "description": "Tags for this version",
        "items": {
          "type": "object",
          "properties": {
            "id": { "type": "integer" },
            "name": { "type": "string" }
          }
        }
      },
      "welcome_message": {
        "type": "string",
        "description": "Welcome message shown when conversation starts"
      },
      "conversation_starters": {
        "type": "array",
        "description": "Suggested conversation starters",
        "items": { "type": "string" }
      },
      "pipeline_settings": {
        "type": "object",
        "description": "Pipeline-specific settings (for pipeline agent_type)",
        "default": {}
      },
      "meta": {
        "type": "object",
        "description": "Version metadata. 'step_limit' defaults to 25.",
        "default": {}
      }
    },
    "required": ["project_id", "application_id", "name"]
  }
}
```

### Example Call

```json
{
  "tool": "postEliteaCoreVersions",
  "arguments": {
    "project_id": 42,
    "application_id": 101,
    "name": "v2-experimental",
    "agent_type": "react",
    "instructions": "You are a code review assistant.",
    "llm_settings": {
      "model_name": "gpt-4o",
      "temperature": 0.3,
      "max_tokens": 4096
    },
    "tools": [
      {
        "name": "GitHub",
        "type": "github",
        "settings": { "repository": "my-org/my-repo" }
      }
    ],
    "meta": {
      "step_limit": 25
    }
  }
}
```

### Response Shape

**HTTP 201**: Created version detail object:
```json
{
  "id": 201,
  "name": "v2-experimental",
  "status": "draft",
  "created_at": "2025-02-26T10:00:00",
  "author_id": 42,
  "author": { "id": 42, "name": "John Doe", "email": "john@example.com" },
  "instructions": "You are a code review assistant.",
  "llm_settings": { "model_name": "gpt-4o", "temperature": 0.3, "max_tokens": 4096 },
  "tools": [{ "id": 56, "name": "GitHub", "type": "github" }],
  "variables": [],
  "tags": [],
  "meta": { "step_limit": 25 },
  "agent_type": "react",
  "welcome_message": null,
  "conversation_starters": null,
  "pipeline_settings": {},
  "application_id": 101,
  "is_forked": false,
  "icon_meta": {}
}
```
