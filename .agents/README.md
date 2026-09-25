# AI Agent Directory (`.agents/`) 🤖

Welcome to the **`.agents/`** directory. This directory houses operational guidelines, context prompts, and automation scripts intended for AI coding assistants (Antigravity, Cursor, Windsurf, Copilot) and project maintainers.

---

## 📁 Directory Layout

```text
.agents/
├── README.md               # Overview of the agent directory
├── auto-push.md            # SOP for Test-Driven commit and push automation
├── plugins/
│   └── win-fresh-setup-kit/
│       ├── plugin.json     # Plugin manifest
│       └── mcp_config.json # Local MCP server definitions (fetch & github)
├── skills/
│   └── win-app-manager/
│       └── SKILL.md        # Instructions for managing apps & presets
└── scripts/
    └── auto_push.ps1       # Executable PowerShell test-and-push script
```

---

## 📖 Workflows & Capabilities

- **[auto-push.md](file:///D:/Workspace/Script/.agents/auto-push.md)**: Rules and procedures for testing, updating docs (`README.md` & `CHANGELOG.md`), committing, and pushing code.
- **[plugins/win-fresh-setup-kit/](file:///D:/Workspace/Script/.agents/plugins/win-fresh-setup-kit/)**: Antigravity customization plugin exposing MCP servers (`fetch` dan `github`) untuk otomasi pengambilan data web dan operasi GitHub.
- **[skills/win-app-manager/](file:///D:/Workspace/Script/.agents/skills/win-app-manager/)**: Skill terpadu agen untuk validasi Winget catalog di `apps.json` dan profil di `presets.json`.
- **[scripts/auto_push.ps1](file:///D:/Workspace/Script/.agents/scripts/auto_push.ps1)**: The core executable script that validates the test suite before permitting any Git push.
