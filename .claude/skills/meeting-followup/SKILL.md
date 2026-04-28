---
name: meeting-followup
description: Generate a structured meeting follow-up document from a raw text transcript. Produces a .md file with a quick recap, key discussion points, and action items with owners and due dates. Use when the user provides a meeting transcript, meeting notes, or asks to summarize a meeting.
---

# Meeting Follow-Up Generator

## Workflow

1. Read the pasted transcript carefully
2. Identify the meeting topic, date (if mentioned), and participants
3. Generate the follow-up using the template below
4. Save the output as a `.md` file (default name: `meeting-followup-YYYY-MM-DD.md`)

## Output Template

```markdown
# Meeting Follow-Up: [Topic / Meeting Title]

**Date:** [Date if mentioned, otherwise omit]
**Attendees:** [Names or roles if identifiable]

---

## Quick Recap

[2–4 sentence summary of the meeting's purpose and overall outcome.]

---

## Key Discussion Points

- [Topic 1]: [What was discussed and any conclusion reached]
- [Topic 2]: [What was discussed and any conclusion reached]
- [Add more as needed]

---

## Action Items

| # | Action | Owner | Due Date |
|---|--------|-------|----------|
| 1 | [Clear, specific task] | @[Name/Role] | [Date or "TBD"] |
| 2 | [Clear, specific task] | @[Name/Role] | [Date or "TBD"] |

---

*Generated from meeting transcript.*
```

## Rules

- **Recap**: Neutral summary — no opinions or filler. Max 4 sentences.
- **Key points**: Group related topics. Omit small talk and tangents.
- **Action items**: Extract only commitments, decisions, or tasks with a clear next step. Each must be actionable (starts with a verb: *Review*, *Send*, *Schedule*, *Complete*, etc.).
  - If an owner is clearly named in the transcript → include them as `@Name`
  - If no owner is mentioned → use `@TBD`
  - If a due date is mentioned → use it; otherwise use `TBD`
- Do not invent information not present in the transcript.
- If the transcript is ambiguous, flag it with a `> ⚠️ Note:` blockquote below the relevant section.
