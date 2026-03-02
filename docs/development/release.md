# Release Guide

<!-- Diátaxis type: How-to -->

This guide describes the steps to cut a new release of `dobot_api_v3`.

## 1. Update version

Bump the version in `pyproject.toml`:

```toml
[project]
version = "3.0.0"
```

## 2. Update the changelog

Add a new section to [changelog.md](../changelog.md) following
[Conventional Commits](https://www.conventionalcommits.org/) categories
(`Added`, `Changed`, `Removed`, `Fixed`).

## 3. Run quality checks

```powershell
uv run ruff check .
uv run ruff format --check .
uv run mypy dobot_api_v3
uv run pytest tests/unit/ tests/integration/ -q
```

All checks must pass before proceeding.

## 4. Build documentation

```powershell
cd docs
npm run docs:build
```

Verify the build completes without warnings.

## 5. Create a release commit

```powershell
git add -A
git commit -m "chore: release v3.0.0"
git tag v3.0.0
git push origin main --tags
```

## 6. Publish the package

Follow your organization's package publishing workflow (e.g., `uv build` and
upload to a private index).

## 7. Post-release

- Verify the published package installs correctly.
- Update any downstream projects that depend on the new version.
