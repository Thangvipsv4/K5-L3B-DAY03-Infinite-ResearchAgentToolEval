
---
name: research_notes
track: bonus
kind: action
requires_env: []
inputs: [title, content, source, confirmed]
outputs: [tool, status, note, total_notes, error, message]
side_effect: local_file_write
requires_confirmation: true
---

# research_notes

Saves research notes into a local JSON file.

Use this tool when the user explicitly wants to save a research note
for later reference.

Inputs:
- title: non-empty note title.
- content: non-empty note content.
- source: optional source URL or reference.
- confirmed: must be true before writing to the file.

Do not use this tool when the user only wants to summarize or format
information without saving it.

The tool returns the saved note and total note count on success.
It returns an error dictionary if input or file operations fail.
