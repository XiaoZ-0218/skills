# coding-instructions

[English](README.md) | [简体中文](README.zh-CN.md)

> Andrej Karpathy coding principles + Conventional Commits + feature-branch workflow + cute-tone replies

An **Agent Skill** pack for AI-assisted coding: helps individuals and small teams keep code simple, commit history clean, and merges controlled while coding with AI.

## Features

- **Minimalist coding**: start from the shortest, self-contained, zero-dependency implementation; add complexity gradually
- **Copy first, innovate later**: reuse proven solutions; introduce one complexity at a time
- **Understand the fundamentals**: no black boxes; code shows understanding of the underlying mechanism
- **Feature-branch development**: cut a branch from the current upstream; works with plain repos and `git worktree`
- **Conventional Commits**: type + concise description (see `references/commit-messages.md`)
- **Merge only after tests pass**: full tests and explicit user permission required; never merge on your own
- **Cute-tone conversation**: all replies use a cute, gentle, playful tone

## Skill package layout

The repo root is itself an installable skill directory (per Grok / Claude Code Agent Skill conventions):

```
coding-instructions/
├── SKILL.md                      # Entry point: frontmatter + agent-executable spec (English)
├── references/
│   ├── commit-messages.md        # Detailed commit-message reference (English)
│   └── python.md                 # Python project conventions: use uv
├── README.md                     # This file (English)
├── README.zh-CN.md               # 中文 README
├── CONTRIBUTING.md               # Contribution guide (English)
├── CONTRIBUTING.zh-CN.md         # 中文贡献指南
├── LICENSE
└── .gitignore
```

| File | Purpose |
| ---- | ------- |
| `SKILL.md` | Skill entry. Contains `name`/`description` frontmatter plus coding, git, and tone rules |
| `references/commit-messages.md` | Commit format, type table, examples, and AI commit rules |
| `references/python.md` | Python project conventions: use uv for dependencies and environments |
| `README.md` / `README.zh-CN.md` | Project intro and installation guide (EN / 中文) |
| `CONTRIBUTING.md` / `CONTRIBUTING.zh-CN.md` | Contribution guide (EN / 中文) |
| `LICENSE` | MIT license |

## Install

Place this repo (or its skill directory) on the skills scan path of your tool. Recommended directory name: `coding-instructions`.

### Grok

```bash
# user-level (available in all projects)
git clone <repo URL> ~/.grok/skills/coding-instructions

# or project-only
git clone <repo URL> .grok/skills/coding-instructions
```

- Slash command: `/coding-instructions`
- Auto-trigger: when the description matches intents like "write code / commit / branch / merge / cute tone"

### Claude Code

```bash
# user-level
git clone <repo URL> ~/.claude/skills/coding-instructions

# or project-level
git clone <repo URL> .claude/skills/coding-instructions
```

### Cursor

```bash
git clone <repo URL> ~/.cursor/skills/coding-instructions
# or
git clone <repo URL> .cursor/skills/coding-instructions
```

### Manual sync / symlink

If already cloned elsewhere, symlink to avoid copies:

```bash
ln -s /path/to/coding-instructions ~/.grok/skills/coding-instructions
ln -s /path/to/coding-instructions ~/.claude/skills/coding-instructions
```

> To update the skill: `git pull` in the clone.

## Usage

1. Install into the skills directory as above
2. Start a new session, or run `/coding-instructions` explicitly
3. The AI agent should automatically follow the spec while coding, committing, branching, and merging

**Quick sanity check**: if replies are no longer in the cute tone, the skill is probably not loaded in the current context — re-activate it or check the install path.

## Spec summary

### Coding principles

1. Minimalism — start simple
2. "Don't be a hero" — copy first, innovate later
3. Understand the fundamentals
4. Simple to complex
5. Clean code style
6. Minimal dependencies

### Git workflow

- Cut `feature|fix|test|docs/<description>` from the current upstream
- Commit after each logical step (format: `references/commit-messages.md`)
- Run the full test suite before merging and ask the user for permission
- Merge into main with `git merge --no-ff`; never substitute squash/rebase merges
- Delete merged feature branches

### Tone

- Cute, gentle, playful; technical content stays professional and accurate

Full executable spec: [`SKILL.md`](./SKILL.md).

## Contributing

Suggestions via Issues or Pull Requests are welcome. Please read [`CONTRIBUTING.md`](./CONTRIBUTING.md) first (中文：[CONTRIBUTING.zh-CN.md](./CONTRIBUTING.zh-CN.md)).

## License

This project is licensed under [MIT](./LICENSE).
