# Claude Code setup

Open this repo's folder in **Claude Code in the Claude desktop app** and paste the prompt below.

It runs in two passes. The vault connector it installs only appears after you restart the Claude app, and the page can only be published once the connector is there. So: paste, let it finish part 1, restart Claude, open a new Claude Code session in this folder, and paste the same prompt again. It checks what's already done and picks up where it left off.

```text
Set up Second Brain Chat from this repo for me: an iMessage-style group chat where Claude Code and Codex post what they save to my Obsidian vault, and I can text back.

Ground rules for you:
- Read README.md, connector/vault-only.js, vault-files/chat/Second Brain rules.md and prompts/sync-task.md before doing anything.
- Explain each step in plain language as you go. Ask before changing anything outside this repo folder, and wait for my yes.
- Check what's already done before each step and skip it if so. I may be running this a second time after a restart.
- Never delete or overwrite my existing notes or settings. Back up any config file before editing it.
- If a permission check blocks one of your actions, don't look for a way around it. Give me the exact command or click path to do it myself, then continue.
- Quote every path, since vault paths often contain spaces.

Start by telling me in a few lines what you're about to do (copy two notes and a small script into my vault, install a local vault connector for the Claude app, add a short instruction for Claude, then after a restart publish my private page and an hourly sync) and ask me to confirm.

PART 1: vault and connector

1. Ask for my Obsidian vault's full path. Check it exists and looks like a vault (it usually has a .obsidian folder; ask me if it doesn't). Note my OS (macOS or Windows) and which Python command works (python3, or python / py on Windows).

2. Copy into the vault, keeping the same relative paths:
   - vault-files/chat/Second Brain.md -> chat/Second Brain.md (skip if it already exists: it holds the chat history)
   - vault-files/chat/Second Brain rules.md -> chat/Second Brain rules.md (if one exists and differs, show me the difference and ask)
   - vault-files/tools/second_brain_chat.py -> tools/second_brain_chat.py
   Then run the script with to-json into a temp file to confirm it parses (0 messages is expected on a fresh chat).

3. Install the vault connector:
   - Folder: ~/.second-brain/connector on macOS, %USERPROFILE%\.second-brain\connector on Windows. Create it if needed.
   - Check Node.js 18 or newer (node --version). If it's missing or older, tell me to install the LTS from nodejs.org, then stop until I say it's done.
   - In that folder run: npm install @modelcontextprotocol/server-filesystem@2026.8.31
   - Copy connector/vault-only.js into that folder.
   - Smoke test: confirm node_modules/@modelcontextprotocol/server-filesystem/dist/index.js exists. Don't start the server.

4. Register the connector with the Claude desktop app:
   - Config file: ~/Library/Application Support/Claude/claude_desktop_config.json on macOS, %APPDATA%\Claude\claude_desktop_config.json on Windows. If it doesn't exist, create it as {"mcpServers":{}}.
   - Copy it to claude_desktop_config.backup.json in the same folder first.
   - Under "mcpServers", add (or update, if one already exists with this name) an entry named exactly "second-brain-vault":
     command: the absolute path to node (from `which node` on macOS or `where node` on Windows; the desktop app doesn't always see your shell's PATH)
     args: [absolute path to vault-only.js, absolute vault path]
   - Keep every other server and setting exactly as it is, and check the result is valid JSON.
   - Show me the entry and explain in two sentences what vault-only.js does: the Claude app normally hands local connectors the folder of whichever Claude Code session is open, so the wrapper keeps this connector on my vault folder and nothing else.

5. Show me this text and ask whether to add it to ~/.claude/CLAUDE.md (create the file if missing, keep everything already there):

   ## Second Brain chat
   My Obsidian vault at <vault path> is shared memory between you and Codex. When you make a meaningful change in it (a new or edited note, a project update, a decision or preference saved), append one to three lines to chat/Second Brain.md following chat/Second Brain rules.md, with `claude` as the sender. When starting work that touches the vault, read the last 20 or so chat lines so you know what Codex changed.

6. Tell me to fully quit the Claude app (macOS: Cmd+Q; Windows: right-click the tray icon, Quit), reopen it, open a new Claude Code session in this repo folder, and paste this same prompt. Stop here, unless tools named like mcp__second-brain-vault__read_text_file are already in your tool list, in which case continue with part 2.

PART 2: page and sync (only when the second-brain-vault tools are available to you)

7. Check the connector: call its list_allowed_directories tool and confirm my vault path is listed, then read chat/Second Brain.md through it. If the vault isn't listed, the wrapper isn't active: recheck the config entry from step 4 and ask me to restart again.

8. Publish page/second-brain.html as a new private artifact with the Artifact tool, unchanged, with icon "chat", description "An iMessage-style group chat of what Claude Code and Codex share in my Obsidian vault", and exactly these capabilities:
   {"db":{"rules":[{"path":"","read":"view","write":"admin"},{"path":"data/users/{self}","write":"interact"}]},"user":{},"sample":{},"mcp":{"servers":[{"server":"host:second-brain-vault","tools":["list_allowed_directories","read_text_file","write_file","edit_file","list_directory","search_files","get_file_info"]}]}}
   Give me the link. Mention that it stays private to me, and that pages using a local connector can't be shared by public link.

9. Create the hourly sync. Take the prompt inside the code block in prompts/sync-task.md, replace {{VAULT}} with my vault path and {{PAGE_URL}} with the page link, and use my working Python command in place of python3. Create a scheduled task named "second-brain-sync" with cron "7 * * * *" and that prompt. If you can't create scheduled tasks, or a permission check blocks it, give me the filled-in prompt and tell me to create it myself from Scheduled in the Claude app sidebar (hourly). Either way, tell me it only runs while the Claude app is open, and suggest I click Run now once so it asks for its permissions up front.

10. Post the first chat line: append to chat/Second Brain.md, under "## Messages", a line in the rules' format from `claude`, for example:
    - <current UTC time, like 2026-01-01T12:00:00Z> | claude | chat/Second Brain rules.md | - | Second Brain is set up. Codex, say hi when you get here.
    Run the script's to-json again to confirm it now finds 1 message.

11. Show me prompts/CODEX.md with my vault path filled in, ready to paste into Codex.

12. Tell me how to check it:
    - Open the page link in the Claude desktop app (not a browser) and allow the vault connector and Claude when asked.
    - A green dot next to "Second Brain" means it's reading my vault. My first message from Claude should be there.
    - Send a test text, e.g. "what's in this vault?". Claude's typing dots should appear, and a reply should arrive within a minute.
    - If there's no green dot, ask you to read the page's diagnostic: ArtifactData get on the page link, collection data/users/me, doc diag. It lists the folders the connector offered and what failed.

Finish with a short summary of everything you changed on my computer and how to undo it (the Undo section of README.md).
```

## If something goes wrong

- **No green dot.** The page can't reach the vault through the connector. In Claude Code, ask Claude to read the page's diagnostic: ArtifactData `get` on your page link, collection `data/users/me`, doc `diag`. It lists the folders the connector offered and what failed. The usual cause is the config entry pointing at the wrong node or vault path, or the app not fully restarted.
- **The second-brain-vault tools never show up in Claude Code.** Check Settings, Developer in the Claude app: the connector should be listed as running. If it shows an error, the node path or a file path in the config entry is wrong.
- **"Not Delivered" on a text.** The page couldn't save to its storage. Reload; if it keeps happening, update the Claude app.
- **Undo.** Remove the `second-brain-vault` entry from the config (or restore the backup), restart Claude, delete the scheduled task, and remove the Second Brain section from `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`. Your chat history stays in the vault.
