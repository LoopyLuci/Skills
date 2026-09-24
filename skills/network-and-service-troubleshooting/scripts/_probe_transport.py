"""Read-only transport probe: hold TLS connections open and compare routes.

Reproduces long-poll flapping without calling any API method, so it never
conflicts with a live bot. Tests auto/IPv4/IPv6 routes to a host:port.

Usage:
    python scripts/_probe_transport.py [rounds] [hold_seconds]
    python scripts/_probe_transport.py 8 10
"""
from __future__ import annotations

import socket
import ssl
import statistics
import sys
import time

HOST = "api.telegram.org"
PORT = 443


def resolve(family: int | None) -> list[str]:
    fam = family if family is not None else 0
    try:
        infos = socket.getaddrinfo(HOST, PORT, fam, socket.SOCK_STREAM)
    except OSError as e:
        print(f"    getaddrinfo failed: {e}")
        return []
    seen, out = set(), []
    for *_, sa in infos:
        ip = sa[0]
        if ip not in seen:
            seen.add(ip)
            out.append(ip)
    return out


def one(family: int | None, hold: float) -> tuple[bool, float, str]:
    ctx = ssl.create_default_context()
    t0 = time.monotonic()
    try:
        fam = family if family is not None else 0
        infos = socket.getaddrinfo(HOST, PORT, fam, socket.SOCK_STREAM)
        af, socktype, proto, _, sa = infos[0]
        s = socket.socket(af, socktype, proto)
        s.settimeout(20)
        s.connect(sa)
        with ctx.wrap_socket(s, server_hostname=HOST) as ss:
            time.sleep(hold)
            ss.sendall(
                f"HEAD / HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n".encode()
            )
            data = ss.recv(64)
        dt = time.monotonic() - t0
        if not data:
            return False, dt, "empty read after hold"
        return True, dt, data.split(b"\r\n")[0].decode(errors="replace")
    except Exception as e:
        return False, time.monotonic() - t0, f"{type(e).__name__}: {str(e)[:60]}"


def run(label: str, family: int | None, rounds: int, hold: float) -> None:
    ips = resolve(family)
    print(f"  [{label}] resolves to: {ips or 'NOTHING'}")
    ok, lat, fails = 0, [], []
    for i in range(1, rounds + 1):
        good, dt, msg = one(family, hold)
        if good:
            ok += 1
            lat.append(dt)
            print(f"  [{label}] {i:>2}/{rounds} ok    {dt:5.2f}s  {msg}")
        else:
            fails.append(msg.split(":")[0])
            print(f"  [{label}] {i:>2}/{rounds} FAIL  {dt:5.2f}s  {msg}")
    print(f"  --> [{label}] {ok}/{rounds} ok", end="")
    if lat:
        print(f", median {statistics.median(lat):.2f}s", end="")
    print(f", failures={fails}" if fails else ", no failures")
    print()


def main() -> int:
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    hold = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
    print(f"Holding TLS connections to {HOST}:{PORT} for {hold:.0f}s, {rounds} rounds each.")
    print("(No API methods called — the live bot is untouched.)\n")
    run("auto", None, rounds, hold)
    run("v4", socket.AF_INET, rounds, hold)
    run("v6", socket.AF_INET6, rounds, hold)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
