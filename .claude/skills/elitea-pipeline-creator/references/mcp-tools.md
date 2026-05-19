# ELITEA MCP Tools Catalog

Catalog of ELITEA MCP tools available for platform interactions. Use these to inspect, create, modify, and test pipelines and agents.

For detailed input schemas, example calls, and response shapes, read `mcp-tools-schema.md`.

## Platform Management Tools

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

## Conversation Tools

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

## Artifact Toolkit (file/data operations)

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

## TestRail Toolkit (test case management)

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
