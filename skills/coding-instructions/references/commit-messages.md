# Commit Message Convention (Conventional Commits)

The Git workflow in `SKILL.md` references this file as the detailed commit-message spec. Check it before writing any commit message.

## Format

```
<type>: <description>
```

- `<type>`: lowercase English type, see the table below
- `<description>`: concise summary of the change; avoid vagueness

Optional extensions (use when needed, not required):

```
<type>(<scope>): <description>

<body>

<footer>
```

- `<scope>`: affected module/area, e.g. `feat(auth): ...`
- Breaking changes: append `!` after the type (e.g. `feat!: drop the legacy login API`), or add `BREAKING CHANGE: ...` in the footer

## Type table

| Type     | When to use                                  |
| -------- | -------------------------------------------- |
| feat     | New feature                                  |
| fix      | Bug fix                                      |
| refactor | Code restructuring without behavior change   |
| style    | UI/styling tweaks                            |
| docs     | Documentation or comment updates             |
| wip      | Work in progress; checkpointing              |
| perf     | Performance improvement                      |
| test     | Adding or updating tests                     |
| deps     | Dependency install/update/removal            |
| config   | Configuration file changes                   |
| deploy   | Deployment related                           |
| format   | Code formatting                              |
| build    | Build system/scripts changes                 |
| chore    | Maintenance, cleanup, misc non-feature work  |
| remove   | Deleting code/files                          |
| move     | Moving/renaming files                        |
| revert   | Reverting changes                            |

## Commit frequency

- **Commit often**: once per logical step, e.g.:
  - feature completed, bug fixed, refactor done
  - WIP checkpoint, dependency update, docs/comment update
  - tests passing, style/UI tweaks
- **Err on the side of more commits**: don't batch unrelated changes; each commit does one thing

## Examples

```
feat: add user login
fix: fix null pointer in password reset API
refactor: extract auth logic into a dedicated service
style: tweak homepage card shadow
docs: update API docs
wip: shopping cart module in progress
test: add unit tests for registration
deps: add axios
chore: remove dead comments and logs
```

## AI agent commit rules

1. **Commit proactively after every code change**; don't wait for the user to ask
2. Messages must be **concise but meaningful** — it should be clear what changed
3. User asks to "save progress" or "leave it" → use a `wip` commit
4. Mixed intents → **split into multiple commits**
5. Format and type choice must strictly follow this file
