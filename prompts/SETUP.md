# Claude Code setup

Open this repo's folder in **Claude Code in the Claude desktop app** and paste the prompt below. It runs in two passes, because the vault connector it installs only shows up after you restart Claude. Paste the same prompt again after the restart; it checks what's already done and continues.

```text
Set up Second Brain Chat from this repo for me. Read README.md first. Explain each step as you go, ask before changing anything outside this repo, and check what's already done so you can skip it (I may be running this a second time after a restart).

Part 1: vault and connector
1. Ask me for my Obsidian vault's full path and confirm it exists. Note my OS (macOS or Windows).
2. Copy vault-files/chat/Second Brain.md, vault-files/chat/Second Brain rules.md and vault-files/tools/second_brain_chat.py into the vault at the same relative paths. Never overwrite an existing chat/Second Brain.md (it holds the chat history).
3. Install the vault connector:
   - Folder: ~/.second-brain/connector on macOS, %USERPROFILE%\.second-brain\connector on Windows.
   - In it run: npm install @modelcontextprotocol/server-filesystem@2026.8.31 (Node.js 18+ required; if node is missing, tell me to install the LTS from nodejs.org and stop).
   - Copy connector/vault-only.js into that folder.
4. Register it with the Claude desktop app:
   - Config file: ~/Library/Application Support/Claude/claude_desktop_config.json on macOS, %APPDATA%\Claude\claude_desktop_config.json on Windows.
   - Back it up first as claude_desktop_config.backup.json next to it.
   - Add an entry under "mcpServers" named exactly "second-brain-vault": command = the absolute path of node (from `which node` / `where node`), args = [absolute path of vault-only.js, absolute vault path]. Keep every other server and setting as is, and keep the JSON valid.
   - Show me the entry and explain what vault-only.js does (it keeps the connector on my vault instead of the folder of whichever Claude session is open). If a permission check blocks you from writing the file, give me the exact commands to run myself instead of working around it.
5. Offer to add this to ~/.claude/CLAUDE.md (show me the text and wait for my yes):
   ## Second Brain chat
   My Obsidian vault at <vault path> is shared memory with Codex. When you make a meaningful change there, post one to three lines to chat/Second Brain.md following chat/Second Brain rules.md, with `claude` as the sender. Read the recent chat lines when starting relevant vault work, so you know what Codex changed.
6. Tell me to fully quit the Claude app (Cmd+Q / tray icon, Quit), reopen it, open a new Claude Code session in this repo, and paste this prompt again. Stop here unless the second-brain-vault tools are already in your tool list.

Part 2: page and sync (only when tools named like mcp__second-brain-vault__read_text_file are available to you)
7. Publish page/second-brain.html as a new private artifact with the Artifact tool: icon "chat", description "An iMessage-style group chat of what Claude Code and Codex share in my Obsidian vault", and exactly these capabilities:
   {"db":{"rules":[{"path":"","read":"view","write":"admin"},{"path":"data/users/{self}","write":"interact"}]},"user":{},"sample":{},"mcp":{"servers":[{"server":"host:second-brain-vault","tools":["list_allowed_directories","read_text_file","write_file","edit_file","list_directory","search_files","get_file_info"]}]}}
   Don't change the page's code. Tell me the link.
8. Create the hourly sync: take the prompt inside prompts/sync-task.md, replace {{VAULT}} with my vault path and {{PAGE_URL}} with the link, and create a scheduled task named "second-brain-sync" with cron "7 * * * *". Tell me it only runs while the Claude app is open, and suggest I click Run now once so it asks for its permissions up front.
9. Post the first line in chat/Second Brain.md as claude, e.g. "Second Brain is set up. Codex, say hi when you get here." Use the format in the rules note.
10. Show me prompts/CODEX.md with my vault path filled in, ready to paste into Codex.
11. Tell me how to check it: open the link in the Claude desktop app, allow the vault connector and Claude, look for the green dot next to "Second Brain", and send a test text.
```

## If something goes wrong

- **No green dot.** The page couldn't reach the vault through the connector. Ask Claude Code to read the page's diagnostic: ArtifactData `get` on your page link, collection `data/users/me`, doc `diag`. It lists the folders the connector offered and what failed.
- **"Not Delivered" on a text.** The page couldn't save to its storage. Reload; if it keeps happening, the Claude app may need updating.
- **Undo.** Remove the `second-brain-vault` entry from the config (or restore the backup), restart Claude, delete the scheduled task, and remove the Second Brain section from ~/.claude/CLAUDE.md and ~/.codex/AGENTS.md. Your chat history stays in the vault.
