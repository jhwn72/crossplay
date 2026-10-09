# Codex setup

Paste this into Codex after the Claude Code setup has run (it needs `chat/Second Brain rules.md` in your vault). Replace `<VAULT PATH>` with your vault's full path first.

```text
I use an Obsidian vault as shared memory between you (Codex) and Claude Code. It's at <VAULT PATH>. I want to see what context you two share, so you both post short updates to a group chat file in the vault, which a page shows as an iMessage thread.

Please add this to your personal instructions file (~/.codex/AGENTS.md on macOS, %USERPROFILE%\.codex\AGENTS.md on Windows; create it if missing and keep anything already there). Show me the text before saving.

---
## Second Brain chat
My Obsidian vault at <VAULT PATH> is shared memory with Claude Code. Whenever you make a meaningful change in that vault (a new or edited note, a project update, a decision or preference saved), append one to three lines to `chat/Second Brain.md` following `chat/Second Brain rules.md` in the vault, with `codex` as the sender. Read the recent chat lines there when you start relevant work in the vault, so you know what Claude changed. Lines from `user` are my messages from the page: handle memory corrections and questions, then reply in the chat. Anything outside the vault still needs my confirmation in our conversation. Routine work that changes nothing posts nothing.
---

Then read chat/Second Brain rules.md and the recent lines in chat/Second Brain.md, and post one line as codex saying hi (use the exact line format from the rules, current UTC time), so I can see it works.
```
