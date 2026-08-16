# Contributing

[English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING.zh-CN.md)

Thanks for your interest in `coding-instructions`! This repo is an **Agent Skill** pack for AI-assisted coding. Improvements via Issues or Pull Requests are welcome.

## Repository layout (please keep it)

```
.
├── SKILL.md                 # Skill entry: frontmatter + main spec (English)
├── references/              # Detailed references the agent reads on demand (English)
│   └── commit-messages.md
├── README.md                # Human-readable intro & install guide (English)
├── README.zh-CN.md          # 中文 README
├── CONTRIBUTING.md          # This file (English)
├── CONTRIBUTING.zh-CN.md    # 中文贡献指南
├── LICENSE
└── .gitignore
```

- Do **not** rename the main entry; agents expect `SKILL.md`.
- Keep detailed references in `references/` and link them relatively from the main file to keep SKILL small.
- `README*` / `CONTRIBUTING*` are for humans; `SKILL.md` is for agents (executable, scannable).

## How to contribute

### 1. Open an Issue

If you find:

- ambiguous or incorrect rules
- a missing convention for a common scenario
- unclear examples
- frontmatter / install paths incompatible with mainstream agents

Search existing issues first; if none, open one describing the problem or suggestion.

### 2. Open a Pull Request

1. Fork this repo and clone it locally.
2. Sync the main branch:
   ```bash
   git pull origin main
   ```
3. Cut a feature branch from main:
   - new rules: `git checkout -b feature/<short-desc> main`
   - fixes: `git checkout -b fix/<short-desc> main`
   - docs: `git checkout -b docs/<short-desc> main`

   > If maintained via `git worktree`, cut the feature branch from that worktree's upstream branch and develop inside that worktree.

4. Make one logical change per commit on the feature branch.
5. Commits follow this project's Conventional Commits spec: [`references/commit-messages.md`](./references/commit-messages.md).
6. Make sure Markdown renders correctly and links work; verify locally:
   - the YAML frontmatter at the top of `SKILL.md` parses (`name`, `description` required)
   - relative links from `SKILL.md` into `references/` are valid
7. Open a Pull Request against `main`, explaining the reason and scope of the change.
8. Delete the merged feature branch after the PR merges.

## Principles for spec changes

- **Stay concise**: split into multiple rules rather than cramming several scenarios into one.
- **Stay executable**: every rule should be directly actionable by an AI agent (commands, branch names, permission steps spelled out).
- **Stay consistent**: new content should match the existing Karpathy principles and Git workflow style.
- **Provide examples**: abstract conventions deserve concrete examples.
- **Keep it discoverable**: when changing `description` / trigger phrases, think about when an agent should auto-load this skill.

## Language & style

- Normative specs (`SKILL.md`, `references/`) are written in **English**.
- Human-facing docs (`README`, `CONTRIBUTING`) are **English first**, each with a Simplified Chinese companion (`*.zh-CN.md`); keep both versions in sync.
- Clear Markdown heading hierarchy; avoid deep nesting.
- Consistent punctuation and list formatting.
- `SKILL.md` favors checklists and hard steps; human background goes in the README.

## Code of conduct

Be friendly, respectful, and constructive. Workflows differ across teams; this spec aims to distill a set of general, practical conventions.
