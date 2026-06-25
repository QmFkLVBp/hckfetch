import os
import yaml
from pathlib import Path
from typing import List, Dict, Any

CONFIG_DIR = Path.home() / ".config" / "hckfetch"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
LOGO_FILE = CONFIG_DIR / "logo.txt"
DB_FILE = Path.home() / ".hckfetch_logs" / "history.db"

# Список інструментів Kali, що відстежуються за замовчуванням
DEFAULT_TOOLS = [
    "nmap", "masscan", "gobuster", "dirb", "nikto",
    "sqlmap", "hydra", "john", "aircrack-ng", "reaver",
    "metasploit", "msfconsole", "msfvenom", "searchsploit",
    "wpscan", "droopescan", "whatweb", "wafw00f",
    "burpsuite", "zaproxy", "bettercap", "ettercap",
    "tcpdump", "tshark", "wireshark", "responder",
    "impacket", "bloodhound", "neo4j", "crackmapexec"
]

# Шкала рівнів (години -> назва, емодзі)
LEVELS = [
    (0, "🐣 Script Kiddie"),
    (1, "🕵️ Cyber Tourist"),
    (15, "🧑‍💻 Terminal Wanderer"),
    (50, "⚔️ Digital Mercenary"),
    (100, "🦅 Elite Hacker"),
    (500, "👻 Phantom Operator"),
    (1000, "💀 Architect of Chaos")
]

def ensure_config():
    """Створити конфіг за замовчуванням, якщо відсутній. LOGO_FILE не створюється."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        default_config = {
            "tools": DEFAULT_TOOLS,
            "levels": [{"hours": h, "name": n} for h, n in LEVELS],
            "logo_file": str(LOGO_FILE),  # шлях, але файл може не існувати
            "use_random_logo": False,     # не використовуємо вбудовані
            "color_scheme": "default"
        }
        with open(CONFIG_FILE, 'w') as f:
            yaml.safe_dump(default_config, f, default_flow_style=False)

    # logo.txt НЕ створюємо — користувач сам його додасть, якщо захоче

def load_config() -> dict:
    ensure_config()
    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f)

def get_tools() -> List[str]:
    cfg = load_config()
    return cfg.get("tools", DEFAULT_TOOLS)

def get_levels() -> List[tuple]:
    cfg = load_config()
    lvls = cfg.get("levels")
    if lvls:
        return [(item["hours"], item["name"]) for item in lvls]
    return LEVELS

def get_logo_path() -> Path:
    """Повертає шлях до файлу з ASCII-артом, навіть якщо він не існує."""
    cfg = load_config()
    logo_path = cfg.get("logo_file")
    if logo_path:
        return Path(logo_path)
    return LOGO_FILE  # за замовчуванням
