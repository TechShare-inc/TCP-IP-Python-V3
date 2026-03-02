# About the Testing Strategy

<!-- Diátaxis type: Explanation -->

This page explains the rationale behind the project's three-layer testing
architecture. For practical test commands, see [Testing](../development/testing.md).

---

## The V-Model approach

This project follows a "V-Model" approach where each level of the code is
verified against a progressively more realistic environment.

### Level 1: Unit Isolation (The "Brain" Test)

**Goal:** Verify internal logic without any network calls.

**Environment:** Local machine using `unittest.mock`.

**Focus:**

- **Serialization:** Does a command turn into the correct byte string?
- **Deserialization:** Does a malformed byte string raise the appropriate
  exception?
- **State machine:** If the API is in a disconnected state, does calling
  `send()` raise a custom exception?

### Level 2: Loopback Integration (The "Wire" Test)

**Goal:** Verify TCP/IP stack handling — handshakes, buffers, and packet
framing.

**Environment:** Localhost using a stub server (`tests/integration/stub_server.py`).

**Focus:**

- **Connection lifecycle:** Can the API connect, disconnect, and reconnect
  100 times without leaking sockets?
- **Packet fragmentation:** If the stub sends half a response, waits 100 ms,
  and sends the other half, does the API wait or crash?
- **Concurrency:** If two threads call the API at once, is there a `Lock`
  preventing corrupted data on the wire?

### Level 3: Hardware-in-the-Loop — HIL (The "Metal" Test)

**Goal:** Verify timing, power states, and firmware quirks.

**Environment:** Real hardware connected via a dedicated test bench.

**Focus:**

- **Boot time:** Does the API timeout if the hardware takes 10 seconds to
  start?
- **Power cycles:** If the hardware is rebooted, does the API recover the
  session?
- **Throughput:** Can the hardware handle the request rate the API is capable
  of sending?

---

## Specialized testing approaches

### Contract testing

Define a "contract" (e.g., a schema) and run the same suite against both the
stub server and the real hardware. If the real hardware fails but the stub
passes, the stub needs updating.

### Fault injection (Negative testing)

Hardware fails in unpredictable ways. We intentionally inject faults to verify
resilience:

- **Network jitter** — simulate latency or packet loss.
- **Malformed packets** — send garbage data to confirm graceful handling.

### Fuzz testing

Send semi-random byte sequences through the API to ensure it never hangs
indefinitely waiting for a response that will never come.

---

## Test pyramid summary

| Category | Tool | Frequency |
|---|---|---|
| Static analysis | `mypy`, `ruff` | Every commit |
| Unit tests | `pytest` + `unittest.mock` | Every commit |
| Integration tests | `pytest` + stub server | Daily / every PR |
| HIL tests | Physical hardware | Before each release |
