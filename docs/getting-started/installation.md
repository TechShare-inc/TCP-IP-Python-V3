# Installation

## Requirements

- Python 3.9+
- Network access to the robot controller

## Install

```powershell
uv venv
uv pip install -e .
```

## Development dependencies

```powershell
uv pip install -e .[dev]
```

## Documentation dependencies

```powershell
uv pip install -e .[docs]
```

> **Note:** Always use `uv` for environment and package management.
> Do not use bare `pip install` or `python -m venv`.
