---
name: git-workflow
description: Standard flow for branches, commits, and pull requests: inspect, change, test, diff, commit, PR. Use when committing, branching, opening or reviewing a PR, or comparing history.
---

# git-workflow

Announce "Using git-workflow to <purpose>".

## Split
- git CLI: local branches, commits, diffs, rebase, stash.
- GitHub MCP or `gh`: PRs, issues, reviews, CI status.

## Flow
1. `git status` and `git log -5` to see state. Never work on the default branch; branch first.
2. Make the change, run tests.
3. `git diff` and read it. Remove unrelated edits.
4. Commit logically: one concern per commit, message states why.
5. Push and open a PR only when asked. PR body: summary, test evidence, risks.

## Never
Force push, skip hooks, or amend published commits without explicit instruction.
