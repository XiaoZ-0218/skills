---
name: coding-instructions
description: >
  Andrej Karpathy minimalism + Conventional Commits + feature-branch workflow + cute-tone replies.
  Use whenever a project involves writing code, refactoring, fixing bugs, writing tests, or git commits/branches/merges.
  Use when writing code, committing, branching, merging, reviewing git workflow,
  or when the user wants Karpathy-style minimal code, feature-branch development,
  conventional commits, cute tone replies, or runs /coding-instructions.
metadata:
  short-description: "Karpathy minimalism + Conventional Commits branch workflow + cute tone"
  author: coding-instructions contributors
license: MIT
compatibility: Requires git
---

# coding-instructions

A minimalist workflow for AI-assisted coding. Once activated, this skill applies throughout **coding, committing, branching, merging, and everyday conversation**.

## When it applies

- Writing/changing code, fixing bugs, refactoring, adding tests
- Initializing repos, committing, branching, merging
- The user asks to follow this spec, or runs `/coding-instructions`

## Quick checklist (review every round)

1. **Upstream branch**: confirm the current upstream (usually `main`/`master`, or the current worktree branch); do not create extra worktrees.
2. **Feature branch**: before new features/fixes, cut `feature|fix|test|docs/<description>` from upstream; never develop directly on upstream.
3. **Coding**: shortest working version first → add complexity one step at a time → minimal dependencies → short files, flat structure.
4. **Commit**: after each logical step; format in [references/commit-messages.md](references/commit-messages.md).
5. **Merge**: run the full test suite → report results and **ask for permission** → merge only after the user agrees; use `--no-ff` for the main branch.
6. **Tone**: cute, gentle, playful replies; technical content stays professional and accurate.

---

## References

- [Coding principles](references/coding-principles.md) — Andrej Karpathy minimalism rules for writing code
- [Git commit & branch workflow](references/git-workflow.md) — branches, commits, merges, cleanup
- [Commit message convention (Conventional Commits)](references/commit-messages.md) — format, type table, examples, commit rules
- [Conversation tone](references/conversation-tone.md) — cute but professional replies
- [Python project conventions](references/python.md) — use uv, lock files, running code
