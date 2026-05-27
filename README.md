# hckfetch 🍎💀

> A neofetch-style pentesting activity tracker for hackers who want to gamify their terminal.

hckfetch shows a colourful dashboard of cumulative tool-usage statistics (time spent, run count, last session) for common Kali Linux pentesting tools — automatically tracked via transparent shell wrappers.

---

## Screenshot

```
        .-"""""""""""-.
       /  Apple  Pie   \
      /   ___________   \
     |  /             \  |
     | |  ~~~~~~~~~~~  | |
     | |  ~  H A C K ~ | |
     | |  ~~~~~~~~~~~  | |
     |  \___________/  |
      \    [_______]   /
       \    |     |   /
        '-._|_____|_.-'
         |  |  |  |
         |__|  |__|

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

## Installation

```bash
git clone https://github.com/QmFkLVBp/hckfetch
cd hckfetch
chmod +x install.sh
./install.sh
source ~/.bashrc   # or source ~/.zshrc
```

The installer:
1. Copies `hckfetch` and `hckfetch-wrap` to `~/.local/bin/` (or `/usr/local/bin/` as root).
2. Creates `~/.hckfetch_logs/` to store per-session log files.
3. Appends tool-tracking **aliases** to your `~/.bashrc` / `~/.zshrc`.
4. Adds an **auto-launch** line so the dashboard appears on every new terminal.

---

## Usage

| Command | Description |
|---|---|
| `hckfetch` | Display the full dashboard (logo + stats) |
| `hckfetch --no-logo` | Display stats only (no ASCII art) |
| `hckfetch --reset` | Wipe all usage logs and start fresh |
| `hckfetch --help` | Show help |

Set `HCKFETCH_SILENT=1` in your environment to suppress the auto-launch on terminal open.

---

## How Tracking Works

`hckfetch-wrap` is a thin wrapper that:
1. Records a **start timestamp** (unix epoch) to `~/.hckfetch_logs/<tool>/<timestamp>.log`.
2. Executes the **real binary** with all original arguments.
3. Records an **end timestamp** to the same file.

`hckfetch` reads every `.log` file, sums the durations, and displays the result.

The aliases installed look like:

```bash
alias nmap='hckfetch-wrap nmap'
alias sqlmap='hckfetch-wrap sqlmap'
# ... etc.
```

---

## Tracked Tools

| Icon | Tool | Icon | Tool |
|---|---|---|---|
| 🔍 | nmap | 🔓 | hashcat |
| 💀 | metasploit | 🌊 | wfuzz |
| 🕷️ | burpsuite | ⚡ | ffuf |
| 🗄️ | sqlmap | 🗺️ | crackmapexec |
| 🐉 | hydra | 🐧 | enum4linux |
| 🔑 | john | 🚀 | gobuster |
| 📡 | aircrack-ng | 🕵️ | nikto |
| 🦈 | wireshark | | |

Edit the `TOOLS` and `TOOL_ICONS` arrays in `hckfetch` to add your own.

---

## Uninstallation

```bash
./uninstall.sh           # interactive (asks whether to delete logs)
./uninstall.sh --purge   # remove everything including logs
```

---

## Requirements

- Bash 4+
- Standard Unix tools: `date`, `awk`, `find`, `mkdir`
- Optional: `lsb_release` for distro detection
- No heavy dependencies — works on Kali Linux and any Debian-based distro

---

## Files

| File | Description |
|---|---|
| `hckfetch` | Main dashboard script |
| `hckfetch-wrap` | Transparent logging wrapper |
| `install.sh` | Installation script |
| `uninstall.sh` | Uninstallation script |
