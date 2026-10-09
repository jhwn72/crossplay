#!/usr/bin/env python3
"""Second Brain chat helper: parse `chat/Second Brain.md`.

Each message is one line in the chat file:
  - <ISO UTC time> | <claude|codex|user> | <vault note path or -> | <reaction or -> | <text>
A reaction looks like "like codex" (type, then who reacted).
User messages end with an Obsidian block id (" ^um-...") that matches the page's outbox id.

Usage (from the vault root):
  python3 tools/second_brain_chat.py to-json OUT.json   write the messages as JSON rows
  python3 tools/second_brain_chat.py ids                print ids already in the chat
"""
import hashlib, json, os, re, sys

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAT = os.path.join(VAULT, "chat", "Second Brain.md")
LINE = re.compile(r"^- (\d{4}-\d{2}-\d{2}T[\d:.]+Z) \| (claude|codex|user) \| (.*?) \| (.*?) \| (.+)$")
BLOCK = re.compile(r"\s\^([A-Za-z0-9-]+)\s*$")


def parse():
    rows = []
    with open(CHAT, encoding="utf-8") as f:
        for raw in f:
            m = LINE.match(raw.rstrip("\r\n"))
            if not m:
                continue
            ts, sender, note, react, text = m.groups()
            b = BLOCK.search(text)
            if b:
                mid, text = b.group(1), text[: b.start()]
            else:
                mid = "m-" + hashlib.sha1(f"{ts}|{sender}|{text}".encode()).hexdigest()[:10]
            note = "" if note.strip() in ("-", "") else note.strip()
            react = "" if react.strip() in ("-", "") else react.strip()
            tb, tb_by = (react.split(" ", 1) + [""])[:2] if react else ("", "")
            rows.append({"id": mid, "ts": ts, "sender": sender, "text": text.strip(),
                         "file": note, "tapback": tb, "tapback_by": tb_by})
    rows.sort(key=lambda r: r["ts"])
    return rows


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "to-json" and len(sys.argv) == 3:
        rows = parse()
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=0)
        print(f"{len(rows)} messages -> {sys.argv[2]}")
    elif cmd == "ids":
        print("\n".join(r["id"] for r in parse()))
    else:
        print(__doc__)
        sys.exit(1)
