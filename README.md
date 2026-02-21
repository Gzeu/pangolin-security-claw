# 🛡️ Pangolin Security Claw

Pangolin Security Claw is a **biomimetic local security dashboard and manager** built for the **OpenClaw / ClawHub ecosystem**. Inspired by the pangolin, it features layered defense mechanisms (Scales), network threat discovery (Scent), and a panic mode for aggressive process isolation (Curl-Up).

## 🚀 Features

- **Modulul Scent:** Network discovery utilizing Scapy/Nmap algorithms to detect local devices, visualizing threats as a gradient from "Safe Pangolin Green" to "Red Alert".
- **Modulul Curl-Up:** A CPU Watchdog that isolates and quarantines unknown or rogue processes exceeding 80% usage, simulating defensive port blocking.
- **Stealth UI:** A Glassmorphism & Hexagonal React Dashboard featuring a stealth mode (`Shift + S`) that drops opacity to 10%.
- **OpenClaw Agent Skill:** Natural language command integration to trigger security scans and defense mechanisms via OpenClaw NLP.

## 🛠️ Tech Stack

- **Backend:** Python (FastAPI, Psutil, Scapy)
- **Frontend:** React, Tailwind CSS (Vite)
- **AI Agent Integration:** OpenClaw (`skill.json`)

## 📦 Installation & Setup

### 1. Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
*(Note: Some modules like Scapy require Root/Administrator privileges).*

### 2. Frontend (React + Tailwind)
```bash
cd frontend
npm install
npm run dev
```

### 3. OpenClaw Skill Installation
Using the OpenClaw CLI, install the local skill directly from the repository directory:
```bash
npx clawhub@latest install pangolin-security-claw
```
Command examples:
- *"Claw, scanează rețeaua"* (Triggers Scent API)
- *"Claw, intră în panică"* (Triggers Curl-Up CPU Watchdog)

## 🤝 Contributing
Open to PRs for new "organ modules" like the `Long Tongue` (Data Leak Detection) or `Scales` (File Encryption).

**License:** MIT