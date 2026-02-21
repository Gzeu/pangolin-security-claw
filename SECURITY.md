# Security Policy — Pangolin-Guard OS

## Guiding Principles

This project follows a **minimal attack surface** philosophy:

- **Zero unnecessary dependencies.** Every library in `requirements.txt` is present for a specific, irreplaceable reason.
- **No `shell=True`.** All subprocess calls use a strict argument list to prevent command injection.
- **Path traversal protection.** All user-supplied file paths are sanitized using `os.path.normpath()` and validated against the working directory before use.
- **CORS restricted to localhost.** The FastAPI backend only accepts requests from `localhost:5173` and `localhost:3000`. No wildcard `*` allowed.
- **Pinned dependency versions.** `requirements.txt` specifies exact versions to prevent supply-chain attacks from upstream package updates.
- **No raw packet injection without fallback.** The Scent module uses the system `arp` CLI (no root required) instead of raw Scapy packets.

## Dependencies Audit

| Package | Version | Purpose | Can Be Replaced? |
|---|---|---|---|
| fastapi | 0.111.0 | HTTP API framework | No (core) |
| uvicorn | 0.30.1 | ASGI server | No (core) |
| psutil | 5.9.8 | Process inspection (Curl-Up) | No — stdlib has no equivalent |
| pycryptodome | 3.20.0 | AES-256 GCM encryption (Scales) | No — stdlib `hashlib` does not support GCM |
| sqlite3 | stdlib | Data persistence | ✅ Already stdlib |
| subprocess | stdlib | ARP scan (Scent) | ✅ Already stdlib |
| re | stdlib | Regex leak detection (Long Tongue) | ✅ Already stdlib |

## Removed Dependencies
- `scapy` — replaced by system `arp` CLI via stdlib `subprocess`.
- `sqlalchemy` — replaced by stdlib `sqlite3`.

## Reporting Vulnerabilities
Please open a private security advisory via GitHub's Security tab. Do not open public issues for security vulnerabilities.
