<div align="center">

<img src="https://raw.githubusercontent.com/Gzeu/pangolin-security-claw/main/assets/logo.png" alt="Pangolin Security Claw" width="600"/>

# Pangolin Security Claw

**Biomimetic Local Security Dashboard & OpenClaw Skill**

[![License: MIT](https://img.shields.io/badge/License-MIT-a88a75.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3d2b1f?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-1a1a1b?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61dafb?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange?style=for-the-badge)](https://clawhub.dev)
[![Security](https://img.shields.io/badge/AES--256-GCM-red?style=for-the-badge&logo=shield)]()
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()

---

> *"Like the pangolin — the world's most trafficked mammal — this tool survives through layered armor,*
> *instinct-driven defense, and the ability to vanish completely when threatened."*

---

</div>

## What is Pangolin Security Claw?

**Pangolin Security Claw** is a fully local, biomimetic security dashboard and **OpenClaw ecosystem skill**.
It draws its entire architecture from the biology of the pangolin, mapping each defensive organ to a real security function:

| Pangolin Biology | Security Module | Function |
|:---:|:---:|:---|
| ⬡ **Keratin Scales** | `Scales` | AES-256-GCM layered file encryption — one key per chunk |
| 👃 **Scent Glands** | `Scent` | ARP-based network discovery — threat gradient from green to red |
| 🔴 **Curl-Up Reflex** | `Curl-Up` | CPU Watchdog — quarantines rogue processes above 80% usage |
| 👅 **Long Tongue** | `Long Tongue` | Deep regex scan of `.env`, `.log`, `.json` for credential leaks |
| 👁️ **Night Vision** | `Stealth UI` | `Shift+S` drops UI opacity to 10% and hides all window titles |
| 🧠 **Instinct** | `OpenClaw Skill` | Natural language agent — control everything via NLP commands |

---

## Architecture

```
pangolin-security-claw/
├── backend/                  # FastAPI — The Pangolin's nervous system
│   ├── main.py               # API entrypoint & CORS (localhost only)
│   ├── database.py           # SQLite3 stdlib — zero ORM overhead
│   ├── models.py             # EncryptedScale | ThreatRadar | DataLeak
│   ├── modules/
│   │   ├── scales.py         # AES-256-GCM + PBKDF2 + HKDF + secure wipe
│   │   ├── curl_up.py        # psutil watchdog — path-based whitelist
│   │   ├── long_tongue.py    # Regex leak scanner — line-by-line, 5MB cap
│   │   └── scent.py          # ARP cache reader — no root required
│   └── requirements.txt      # Only 4 pinned dependencies
├── frontend/                 # React + Tailwind — The Pangolin's skin
│   └── src/
│       ├── App.jsx           # Layout + Stealth Mode (Shift+S)
│       └── components/
│           ├── HexButton.jsx      # Hexagonal clip-path buttons
│           ├── ScaleCard.jsx      # Danger gradient network cards
│           └── ScalesPanel.jsx    # Drag & Drop encrypt/decrypt UI
└── openclaw-skill/           # The Pangolin's instinct — NLP Agent
    ├── skill.json            # Skill metadata & network permissions
    └── index.js              # Native fetch only — zero npm deps
```

---

## Security Philosophy

```
[ DEPENDENCY SURFACE — MINIMAL BY DESIGN ]

fastapi==0.111.0      → API framework
uvicorn==0.30.1       → ASGI server
psutil==5.9.8         → Process inspection
pycryptodome==3.20.0  → AES-256-GCM cryptography

Everything else: Python stdlib only.
No SQLAlchemy. No Scapy. No axios.
```

**Core hardening decisions:**

- CORS restricted to `localhost:5173` and `localhost:3000` only — no wildcard
- File uploads use `uuid4` prefixes to prevent race conditions
- Long Tongue reads files **line-by-line** with a **5MB hard cap** — no RAM bombs
- Scent uses `arp -n` / `arp -a` via `subprocess(shell=False)` — no raw sockets
- Curl-Up checks absolute **executable paths**, not process names (bypasses whitelist spoofing)
- AES master key derived via **PBKDF2 (200,000 iterations)** — never stored in plaintext
- Each chunk uses **HKDF-derived layer keys** — not SHA256 shortcuts
- Source files are **securely overwritten** with `os.urandom` before deletion

---

## Quick Start

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload  # API running at http://localhost:8000
```

> Note: `Scent` module reads the system ARP cache and does **not** require root/administrator.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev  # Dashboard running at http://localhost:5173
```

### 3. OpenClaw Skill (via ClawHub)

```bash
npx clawhub@latest install pangolin-security-claw
```

**Natural Language Commands:**

```
"Claw, scan the network"       → triggers Scent ARP sweep
"Claw, activate panic mode"    → arms Curl-Up CPU watchdog
"Claw, search for leaks"       → runs Long Tongue regex scan
"Claw, encrypt file report.pdf" → calls Scales AES-256 endpoint
```

---

## Stealth Mode

Press `Shift + S` anywhere in the dashboard to enter **Stealth Mode**:

- UI opacity drops to **10%**
- All panel titles are hidden
- Application becomes visually undetectable at a glance
- Press `Shift + S` again to restore

---

## Modules At a Glance

### ⬡ Scales — Layered File Encryption

Files are split into **64KB chunks** (scales). Each scale receives a unique AES-256-GCM key derived via HKDF from a PBKDF2 master. Output is a `.pangolin` binary file. Decryption requires the original password.

### 👃 Scent — Network Threat Radar

Reads the OS ARP cache to discover live devices on the subnet. Each device is assigned a **scent level (1–100)** visualized as a color gradient: `#22c55e` (safe) → `#ef4444` (alert).

### 🔴 Curl-Up — CPU Panic Watchdog

Monitors all running processes. Any unknown executable exceeding **80% CPU** is immediately suspended and flagged. Uses absolute path verification — not process name — to prevent whitelist bypass.

### 👅 Long Tongue — Credential Leak Scanner

Scans `.env`, `.log`, and `.json` files with high-precision regex patterns for:
`AWS_ACCESS_KEY` · `GITHUB_TOKEN` · `STRIPE_KEY` · `PASSWORD=` · `API_KEY=`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | Python 3.10+ / FastAPI |
| Cryptography | PyCryptodome (AES-256-GCM, PBKDF2, HKDF) |
| Process Monitor | psutil |
| Database | SQLite3 (stdlib) |
| Frontend | React 18 + Tailwind CSS + Vite |
| UI Theme | Glassmorphism · Hex Grid · Dark Mode (`#1a1a1b`, `#3d2b1f`) |
| AI Agent | OpenClaw Skill (native fetch, zero npm deps) |

---

## Contributing

Open to PRs for new **organ modules**. Ideas:

- `Ear` — passive traffic listener (pcap-based)
- `Burrow` — encrypted local vault for secrets
- `Baby Pangolin` — lightweight CLI-only version

Please read [`SECURITY.md`](SECURITY.md) before contributing.

---

**Built with the instincts of the most armored mammal on Earth.**
`pangolin-security-claw` · MIT License · OpenClaw Ecosystem
