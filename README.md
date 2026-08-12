# My Claude Code Skills

This directory is the single source of truth for custom skills, system rules, and templates to use globally across all software projects.

## How to Load a Skill in Claude Code
When starting Claude Code in a project, you can load a skill from this directory:
```bash
claude --plugin-dir D:\Code\myskills\<skill-name>
```

---

## Active Skills Index

### 1. [ui-ux-pro-max](ui-ux-pro-max/SKILL.md)
*   **Purpose**: Guidelines for building premium SaaS interfaces with glassmorphism, spring physics, and high contrast.
*   **Source**: Inspired by Emil Kowalski's physics-based UI components.

### 2. [franchise-ops-helper](franchise-ops-helper/SKILL.md)
*   **Purpose**: Structure rules for designing franchise operations (QSR recipes, audits, visual merchandising compliance, and multi-tenant isolation).

### 3. [db-migration-helper](db-migration-helper/SKILL.md)
*   **Purpose**: Strict rules for writing database migrations, RLS (Row-Level Security) policies, and maintaining clean schema updates.

---

## Cloned Repositories

### 1. [emilkowalski-skills](emilkowalski-skills)
*   **Purpose**: Professional design engineering and animation guides.
*   **Key Skills Included**:
    *   `emil-design-eng`: Core design-to-code practices.
    *   `animate`: Physics-based motion curves & duration principles.
    *   `apple-design`: Designing natural, fluid Apple-inspired interfaces.
    *   `improve-animations`: Codebase-wide motion audits.
    *   `prototype`: Quick variant building.
    *   `pick-ui-library`: UI package comparisons.

### 2. [claude-code-best-practice](claude-code-best-practice)
*   **Purpose**: A massive library of best practices, orchestration guides, and MCP setups.
*   **Key Files**:
    *   [Orchestration Workflow](claude-code-best-practice/orchestration-workflow/orchestration-workflow.md)
    *   [Subagent Best Practices](claude-code-best-practice/best-practice/claude-subagents.md)
    *   [Memory Management Rules](claude-code-best-practice/best-practice/claude-memory.md)

---

## Recommended Repositories to Watch
*   **[hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)**: Canonical curated directory for Claude Code customizations.
*   **[worldflowai/everything-claude-code](https://github.com/worldflowai/everything-claude-code)**: Deep reference implementations, specialized agents, and custom hooks.
*   **[punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)**: A huge list of Model Context Protocol (MCP) integrations.
