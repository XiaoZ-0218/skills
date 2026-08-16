# Python project conventions

Guidelines for Python projects created under this skill.

## Package manager

Use **[uv](https://docs.astral.sh/uv/)** for Python dependency and environment management.

- Initialize new projects with `uv init`.
- Add dependencies with `uv add <package>`.
- Run commands and scripts with `uv run <command>`.
- Pin the Python version with a `.python-version` file (managed via `uv python pin`).

Do **not** use `pip`, `pipenv`, `poetry`, or `conda` unless the project explicitly requires an ecosystem only they support. If an exception is needed, document the reason in the README.

## Lock file

Commit `uv.lock` so environments are reproducible. Update it with `uv lock` or `uv sync`.

## Virtual environment

Let uv manage the virtual environment automatically. Avoid committing `.venv/`; it is already ignored by default in `uv init` templates.

## Running code

Prefer `uv run` over activating the virtual environment manually:

```bash
uv run python script.py
uv run pytest
uv run ruff check .
```

## Quick start template

```bash
uv init my-project
cd my-project
uv python pin 3.12
uv add pytest
uv run pytest
```
