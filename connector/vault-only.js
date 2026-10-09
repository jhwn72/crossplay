#!/usr/bin/env node
// Runs the filesystem MCP server so it always serves only the folders given on the
// command line (your Obsidian vault). The Claude app sends each session's folders as
// MCP "roots", and the server would replace its folder list with them; this wrapper
// hides the roots capability from the server so the vault stays the allowed folder.
// Undo: remove the second-brain-vault entry from claude_desktop_config.json and restart Claude.
const { spawn } = require("child_process");
const path = require("path");

const server = path.join(__dirname, "node_modules/@modelcontextprotocol/server-filesystem/dist/index.js");
const child = spawn(process.execPath, [server, ...process.argv.slice(2)], { stdio: ["pipe", "inherit", "inherit"] });

let buf = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => {
  buf += chunk;
  let i;
  while ((i = buf.indexOf("\n")) >= 0) {
    const out = rewrite(buf.slice(0, i));
    buf = buf.slice(i + 1);
    if (out !== null) child.stdin.write(out + "\n");
  }
});
process.stdin.on("end", () => {
  if (buf.trim()) {
    const out = rewrite(buf);
    if (out !== null) child.stdin.write(out + "\n");
  }
  child.stdin.end();
});

function rewrite(line) {
  if (!line.trim()) return line;
  let msg;
  try { msg = JSON.parse(line); } catch { return line; }
  if (msg.method === "initialize" && msg.params && msg.params.capabilities) {
    delete msg.params.capabilities.roots;
    return JSON.stringify(msg);
  }
  if (msg.method === "notifications/roots/list_changed") return null;
  return line;
}

child.on("exit", (code, signal) => process.exit(code ?? (signal ? 1 : 0)));
for (const sig of ["SIGINT", "SIGTERM"]) process.on(sig, () => child.kill(sig));
