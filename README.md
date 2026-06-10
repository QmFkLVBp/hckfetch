# hckfetch 🍎💀

<p align="center">
  <strong>Neofetch-style pentesting activity tracker for your terminal.</strong>
</p>

<p align="center">
  <img alt="Shell: Bash 4.0+" src="https://img.shields.io/badge/Bash-4.0%2B-121011?logo=gnu-bash">
  <img alt="Platform: Linux" src="https://img.shields.io/badge/Platform-Linux-2ea44f?logo=linux">
  <img alt="Target distro: Kali Linux" src="https://img.shields.io/badge/Made%20for-Kali-557C94">
</p>

hckfetch gives you a clean dashboard of cumulative pentest tool statistics:

- total time spent per tool
- execution count (runs)
- last session timestamp

Tracking is automatic via transparent command wrappers.

---

## ✨ Highlights

- **Neofetch-like terminal UI**
- **Automatic usage tracking** with no manual logging
- **Per-tool analytics** (time, runs, last session)
- **Easy install/uninstall scripts**
- **Lightweight** (pure Bash, no heavy dependencies)

---

## 📸 Example Output

```text
         (
          )
     __..---..__
 ,-='  /  |  \  `=-.
:--..___________..--;
 \.,_____________,./

╔══════════════════════════════════════════════════╗
║  hckfetch v1.0.0 — pentest activity tracker      ║
╚══════════════════════════════════════════════════╝

 System Info
 ──────────────────────────────
 User:      hacker@kali
 OS:        Kali GNU/Linux Rolling
 Kernel:    6.6.0-kali1-amd64
 Arch:      x86_64
 Uptime:    3h 42m
 Shell:     /usr/bin/zsh

 Tool Usage Statistics
 ──────────────────────────────────────────────────
     Tool              Time        Runs    Last Session
 ──────────────────────────────────────────────────
 🔍  nmap              2h 34m      47      2026-05-26 22:11
 💀  metasploit        1h 12m      18      2026-05-25 19:45
 🕷️  burpsuite         0m 00s       0      never
 ...
```

---

## 🚀 Installation

```bash
git clone https://github.com/QmFkLVBp/hckfetch
cd hckfetch
chmod +x install.sh
./install.sh
source ~/.bashrc   # or source ~/.zshrc
```

Installer actions:
1. Copies `hckfetch` and `hckfetch-wrap` to `~/.local/bin/` (or `/usr/local/bin/` when run as root)
2. Creates `~/.hckfetch_logs/` for session logs
3. Appends tracking aliases to your shell config (`~/.bashrc` / `~/.zshrc`)
4. Adds auto-launch so the dashboard appears in new terminals

---

## 🧪 Usage

| Command | Description |
|---|---|
| `hckfetch` | Show full dashboard (logo + stats) |
| `hckfetch --no-logo` | Show stats only |
| `hckfetch --reset` | Clear all usage logs |
| `hckfetch --help` | Show help |

To disable automatic startup in new terminals:

```bash
export HCKFETCH_SILENT=1
```

Add the line to `~/.bashrc` or `~/.zshrc` for a persistent setting.

---

## ⚙️ How Tracking Works

`hckfetch-wrap`:
1. Writes a **start timestamp** to `~/.hckfetch_logs/<tool>/<timestamp>.log`
2. Runs the real tool command with all original arguments
3. Writes an **end timestamp** to the same log file

`hckfetch` then reads all `.log` files and aggregates totals.

Installed aliases look like:

```bash
alias nmap='hckfetch-wrap nmap'
alias sqlmap='hckfetch-wrap sqlmap'
# ...
```

---

## 🛠️ Tracked Tools

| Icon | Tool |
|---|---|
| 🔍 | nmap |
| 💀 | metasploit |
| 🕷️ | burpsuite |
| 🗄️ | sqlmap |
| 🐉 | hydra |
| 🔑 | john |
| 📡 | aircrack-ng |
| 🦈 | wireshark |
| 🔓 | hashcat |
| 🌊 | wfuzz |
| ⚡ | ffuf |
| 🗺️ | crackmapexec |
| 🐧 | enum4linux |
| 🚀 | gobuster |
| 🕵️ | nikto |

You can extend tracked tools by editing `TOOLS` and `TOOL_ICONS` in `hckfetch`.

---

## 🧹 Uninstallation

```bash
./uninstall.sh           # interactive (asks whether to delete logs)
./uninstall.sh --purge   # remove everything including logs
```

---

## 📦 Requirements

- Bash 4+
- Standard Unix tools: `date`, `awk`, `find`, `mkdir`
- Optional: `lsb_release` (for distro detection)
- Designed for Kali Linux and compatible with Debian-based distros

---

## 📁 Project Files

| File | Description |
|---|---|
| `hckfetch` | Main dashboard script |
| `hckfetch-wrap` | Usage logging wrapper |
| `install.sh` | Installer |
| `uninstall.sh` | Uninstaller |
