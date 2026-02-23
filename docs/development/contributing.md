# Contributing

## Setup

```powershell
uv venv
uv pip install -e .[dev]
```

## Running checks

```powershell
uv run ruff check .
uv run ruff format .
uv run mypy dobot_api_v3
uv run pytest
```

## Coding style

- Use `snake_case` for methods, parameters, and variables
- Use `PascalCase` for class names
- All new public APIs must use Google-style docstrings
- Boolean parameters prefixed with `is_`, `has_`, `should_`, or `can_`
- Constants in `UPPER_SNAKE_CASE`
- No deprecated PascalCase aliases — the API is exclusively `snake_case`

See `.github/copilot-instructions.md` for the complete naming convention
reference.
