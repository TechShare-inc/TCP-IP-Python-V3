"""TCP stub server for Level 2 integration tests.

The stub replaces a real Dobot controller on localhost, allowing tests of the
full send/recv stack (auth handshake, framing, concurrency, fault injection)
without physical hardware.

Usage::

    server = StubServer(response_map={"EnableRobot": "0,0,EnableRobot();"})
    server.start()
    # ... run tests against server.host / server.port ...
    server.stop()

``response_map`` maps command *prefixes* (i.e. the protocol command name, e.g.
``"EnableRobot"``) to the verbatim response string.  If no prefix matches, the
server echoes back the command with a ``"0,0,"`` header.
"""

from __future__ import annotations

import random
import socket
import threading
import time
from typing import Dict, Optional


class StubServer:
    """Single-accepted-connection-at-a-time TCP stub server."""

    host: str = "127.0.0.1"
    port: int = 0  # populated after start()

    def __init__(
        self,
        response_map: Optional[Dict[str, str]] = None,
        *,
        recv_timeout: float = 2.0,
    ) -> None:
        self._response_map: Dict[str, str] = response_map or {}
        self._recv_timeout = recv_timeout
        self._server_sock: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None
        self._running = False

    # ------------------------------------------------------------------

    def start(self) -> "StubServer":
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_sock.bind((self.host, 0))
        self.port = self._server_sock.getsockname()[1]
        self._server_sock.listen(10)
        self._server_sock.settimeout(0.5)
        self._running = True
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()
        return self

    def stop(self) -> None:
        self._running = False
        if self._server_sock is not None:
            try:
                self._server_sock.close()
            except OSError:
                pass
        if self._thread is not None:
            self._thread.join(timeout=3.0)

    def __enter__(self) -> "StubServer":
        self.start()
        return self

    def __exit__(self, *_: object) -> None:
        self.stop()

    # ------------------------------------------------------------------
    # Internal

    def _serve(self) -> None:
        while self._running:
            try:
                conn, _ = self._server_sock.accept()  # type: ignore[union-attr]
            except (socket.timeout, OSError):
                continue
            try:
                self._handle_connection(conn)
            except Exception:
                pass
            finally:
                try:
                    conn.close()
                except OSError:
                    pass

    def _handle_connection(self, conn: socket.socket) -> None:
        conn.settimeout(self._recv_timeout)
        buf = b""
        while self._running:
            try:
                chunk = conn.recv(4096)
            except (socket.timeout, ConnectionResetError):
                break
            if not chunk:
                break
            buf += chunk
            # Each Dobot command ends with ')'
            while b")" in buf:
                end = buf.index(b")") + 1
                raw_cmd = buf[:end]
                buf = buf[end:]
                cmd_str = raw_cmd.decode("utf-8", errors="replace").strip()
                response = self._build_response(cmd_str)
                conn.sendall(response.encode("utf-8"))

    def _build_response(self, cmd: str) -> str:
        for prefix, resp in self._response_map.items():
            if cmd.startswith(prefix):
                return resp
        return f"0,0,{cmd};"

    # ------------------------------------------------------------------
    # Convenience: update response map at runtime

    def set_response(self, prefix: str, response: str) -> None:
        self._response_map[prefix] = response


# ---------------------------------------------------------------------------
# Specialised variants
# ---------------------------------------------------------------------------


class DelayedStubServer(StubServer):
    """Adds a fixed latency before each response (simulates slow network)."""

    def __init__(self, delay: float = 0.1, **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._delay = delay

    def _build_response(self, cmd: str) -> str:
        time.sleep(self._delay)
        return super()._build_response(cmd)


class FragmentedStubServer(StubServer):
    """Sends each response in two halves with a configurable gap between them.

    Used to verify that the client handles TCP fragmentation correctly.
    """

    def __init__(self, gap: float = 0.02, **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._gap = gap

    def _handle_connection(self, conn: socket.socket) -> None:
        conn.settimeout(self._recv_timeout)
        buf = b""
        while self._running:
            try:
                chunk = conn.recv(4096)
            except (socket.timeout, ConnectionResetError):
                break
            if not chunk:
                break
            buf += chunk
            while b")" in buf:
                end = buf.index(b")") + 1
                raw_cmd = buf[:end]
                buf = buf[end:]
                cmd_str = raw_cmd.decode("utf-8", errors="replace").strip()
                payload = self._build_response(cmd_str).encode("utf-8")
                mid = max(1, len(payload) // 2)
                conn.sendall(payload[:mid])
                time.sleep(self._gap)
                conn.sendall(payload[mid:])


class GarbageStubServer(StubServer):
    """Responds with random ASCII garbage (fault-injection)."""

    def _build_response(self, cmd: str) -> str:
        return "".join(chr(random.randint(0x20, 0x7E)) for _ in range(48)) + "\n"
