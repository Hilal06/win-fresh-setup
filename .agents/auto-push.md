# Agent SOP: Test-Driven Commit & Push Workflow 🤖

> **Target Audience**: AI Agents (Antigravity, Cursor, GitHub Copilot, Windsurf) & Human Maintainers.

---

## 🎯 Objectives
This workflow enforces strict **Test-Driven Delivery** for the `win-fresh-setup` repository:
1. Guarantee that broken code is **never committed or pushed** to the remote repository.
2. Ensure documentation (`README.md` and `CHANGELOG.md`) is kept strictly in sync with the codebase state.

---

## 📋 Mandatory Rules for AI Agents

### Rule 1: Always Test Before Commit
Before committing any changes, the test suite **MUST** run and pass with a 100% success rate (11/11 test suites passing).
- Command:
  ```powershell
  .\.venv\Scripts\python.exe test_installer.py
  ```
- Or run the automated pipeline directly:
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\.agents\scripts\auto_push.ps1 -CommitMessage "type: description"
  ```

### Rule 2: Halt Immediately on Test Failure
If any test fails:
- **DO NOT commit or push**.
- Capture and display the full error traceback and diagnostic output.
- Explain the exact cause of failure to the user before attempting any fix.

### Rule 3: Keep Documentation Synchronized
Whenever a feature, fix, or behavior changes:
1. **Update `README.md`**:
   - Reflect changes in the `Features` list or installation/run methods.
   - Keep the `Changelog (Dev Summary)` code block updated.
2. **Update `CHANGELOG.md`**:
   - Record additions, modifications, and bug fixes under `[Unreleased]` according to [Keep a Changelog](https://keepachangelog.com/).

---

## 🛠️ Execution Tools & Methods

### Method 1: Automated Script (`.agents/scripts/auto_push.ps1`)
- **Script Location**: [`.agents/scripts/auto_push.ps1`](file:///D:/Workspace/Script/.agents/scripts/auto_push.ps1)
- **Usage**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\.agents\scripts\auto_push.ps1 -CommitMessage "<commit_message>"
  ```
- **Execution Lifecycle**:
  1. Identifies repository root dynamically.
  2. Executes `.venv\Scripts\python.exe test_installer.py`.
  3. Halts with exit code 1 if any failure occurs.
  4. Stages all files (`git add -A`), commits, and resolves `GITHUB_PERSONAL_ACCESS_TOKEN` from user environment.
  5. Sets `GIT_TERMINAL_PROMPT=0` to prevent hanging UI prompts, securely pushing directly to origin.

### Method 2: GitHub MCP Server (`win-fresh-setup-kit_github`)
When running agent-driven operations or in headless environments:
- Use MCP tools (`push_files`, `create_or_update_file`, `list_commits`, `create_pull_request`) configured via `.agents/plugins/win-fresh-setup-kit/mcp_config.json`.
- Eliminates reliance on interactive Git credential managers or local network blocking.
