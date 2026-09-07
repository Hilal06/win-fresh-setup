# AI Agent Directory (`.agents/`) 🤖

Welcome to the **`.agents/`** directory. This directory houses operational guidelines, context prompts, and automation scripts intended for AI coding assistants (Antigravity, Cursor, Windsurf, Copilot) and project maintainers.

---

## 📁 Directory Layout

```text
.agents/
├── README.md               # Overview of the agent directory
├── auto-push.md            # SOP for Test-Driven commit and push automation
└── scripts/
    └── auto_push.ps1       # Executable PowerShell test-and-push script
```

---

## 📖 Workflows

- **[auto-push.md](file:///D:/Workspace/Script/.agents/auto-push.md)**: Rules and procedures for testing, updating docs (`README.md` & `CHANGELOG.md`), committing, and pushing code.
- **[scripts/auto_push.ps1](file:///D:/Workspace/Script/.agents/scripts/auto_push.ps1)**: The core executable script that validates the test suite before permitting any Git push.
