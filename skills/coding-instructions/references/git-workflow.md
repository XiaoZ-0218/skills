# Git commit & branch workflow

## Upstream branch & worktrees

- **Upstream branch**: the branch you cut feature branches from and eventually merge back into.
- When the user is already in a **git worktree**: that worktree's current branch is the upstream. Cut the feature branch **inside the same worktree**; do **not** create extra worktrees.

## 0. New project initialization

For a new project, **initialize Git first**, then write business code:

```bash
git init
# create a proper .gitignore and README.md
git add -A && git commit -m "chore: initial commit"
```

- Do **not** attach remotes automatically; the user handles remotes.

### Python projects

If the project uses Python, use **[uv](https://docs.astral.sh/uv/)** for dependency and environment management:

```bash
uv init
uv python pin 3.12
uv add pytest
uv run pytest
```

- Prefer `uv add`, `uv run`, and `uv sync` over `pip`, `pipenv`, `poetry`, or `conda`.
- Commit `uv.lock` for reproducible environments.
- Full conventions: [python.md](python.md).

## 1. Feature-branch development

Before starting a feature/fix, cut a branch from upstream:

| Prefix | Purpose | Example |
| ------ | ------- | ------- |
| `feature/` | New feature | `feature/user-login` |
| `fix/` | Bug fix | `fix/null-pointer-in-auth` |
| `test/` | Tests | `test/add-unit-tests` |
| `docs/` | Docs | `docs/update-readme` |

```bash
git checkout -b feature/user-login <upstream-branch>
```

## 2. Commit convention

- Format: `<type>: <description>`
- **Commit after each logical step**; split mixed intents into separate commits.
- Pausing midway: `wip: ...`
- Full type table, examples, and AI commit rules: **must read** [commit-messages.md](commit-messages.md).

## 3. Pre-merge tests & permission (mandatory)

1. Run the project's full test suite (unit/integration/e2e, as applicable).
2. After tests pass, report to the user: change summary + test results, and **explicitly ask for merge permission**.
3. Merge **only after explicit user approval**; never merge on your own.
4. If CI/CD exists, wait for the pipeline to pass.

## 4. Merging back to upstream

1. If upstream has new commits: first `git merge <upstream>` on the feature branch (fast-forward allowed); resolve conflicts **on the feature branch**, then re-run tests.
2. Check out upstream and merge:
   - Upstream is `main`/`master`: **must** use `git merge --no-ff <feature-branch>` (never let default fast-forward drop the merge node).
   - Upstream is a worktree branch (non-main): plain `git merge` or `--no-ff` is fine.
3. **Never** use rebase / squash merge to bring a feature branch into upstream.
4. Suggested merge commit title: `feat: complete xxx` in the same convention.

### Rebase only for catching up with upstream

- With parallel feature branches and a moved upstream: you may `git rebase <upstream>` **on an unmerged feature branch** to stay linear.
- **Never** use rebase instead of merge to land changes on upstream.

## 5. Post-merge cleanup

```bash
git checkout <upstream-branch>
git branch -d feature/user-login
# delete the remote feature branch too, if any
```

## AI agent git rules

1. New feature/fix: cut a feature branch before touching code.
2. **Commit proactively** after every meaningful change; don't wait to be asked.
3. User says "save progress / leave it" → `wip`.
4. Before merging: full tests → report → **wait for permission**.
5. Merging into main must use `--no-ff`.
