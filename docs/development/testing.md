# Testing

See [testing_architecture.md](../testing_architecture.md) for test strategy.

Run all unit and integration tests:

```powershell
uv run pytest tests/unit/ tests/integration/ -q
```

Run only unit tests:

```powershell
uv run pytest tests/unit/ -q
```

Run hardware-in-the-loop tests (requires real robot):

```powershell
uv run pytest tests/hil/ -q
```

## Test layout

| Directory | Scope | Requirements |
|---|---|---|
| `tests/unit/` | Fast isolated tests, mocked I/O | None |
| `tests/integration/` | Loopback stub-server tests | None |
| `tests/hil/` | Real hardware tests | Connected robot |
