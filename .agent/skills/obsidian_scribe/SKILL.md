---
name: obsidian_scribe
description: Delegates knowledge management tasks (concept notes, flashcards) to a specialized agent running inside the Obsidian Vault.
---

# Obsidian Scribe Bridge

This tool bridges the current workspace with the Obsidian Vault.

## Function Definition
Use this tool when the user wants to create permanent notes, flashcards, or documentation based on the current conversation.

**Arguments:**
- `payload`: A JSON string containing:
    - `task`: "flashcard" | "concept_note" | "log"
    - `content`: The raw text/code to be processed.
    - `context`: Brief explanation of why this is being saved.

## Execution
```bash
python3 scripts/obsidian_bridge.py "$payload"
```
