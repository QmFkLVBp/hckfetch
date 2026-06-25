import sqlite3
import time
from pathlib import Path
from typing import Dict, List, Tuple
from .config import DB_FILE, get_tools

def init_db():
    """Створити таблицю, якщо її немає."""
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_FILE))
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool TEXT NOT NULL,
            start_ts INTEGER NOT NULL,
            end_ts INTEGER
        )
    ''')
    c.execute('CREATE INDEX IF NOT EXISTS idx_tool ON sessions(tool)')
    conn.commit()
    conn.close()

def add_session(tool: str, start_ts: int, end_ts: int = None):
    """Додати запис про запуск (при старті) або оновити end_ts при завершенні."""
    conn = sqlite3.connect(str(DB_FILE))
    c = conn.cursor()
    if end_ts is None:
        c.execute('INSERT INTO sessions (tool, start_ts) VALUES (?, ?)', (tool, start_ts))
    else:
        # Оновлюємо останній незавершений запис для цього інструменту
        c.execute('''
            UPDATE sessions 
            SET end_ts = ? 
            WHERE tool = ? AND start_ts = ? AND end_ts IS NULL
        ''', (end_ts, tool, start_ts))
    conn.commit()
    conn.close()

def get_stats() -> Tuple[Dict[str, Dict], float]:
    """
    Повертає статистику по інструментах та загальний час у годинах.
    Повертає: (stats_dict, total_hours)
    stats_dict: { tool: {"runs": int, "total_sec": int, "last_start": int} }
    """
    conn = sqlite3.connect(str(DB_FILE))
    c = conn.cursor()
    # Отримуємо всі завершені сесії
    c.execute('''
        SELECT tool, start_ts, end_ts 
        FROM sessions 
        WHERE end_ts IS NOT NULL
    ''')
    rows = c.fetchall()
    conn.close()

    stats = {}
    total_sec = 0
    for tool, start, end in rows:
        duration = end - start
        if duration < 0:  # захист від помилок
            continue
        total_sec += duration
        if tool not in stats:
            stats[tool] = {"runs": 0, "total_sec": 0, "last_start": 0}
        stats[tool]["runs"] += 1
        stats[tool]["total_sec"] += duration
        if start > stats[tool]["last_start"]:
            stats[tool]["last_start"] = start

    # Додаємо інструменти, які зараз виконуються (незавершені сесії)
    conn = sqlite3.connect(str(DB_FILE))
    c = conn.cursor()
    c.execute('''
        SELECT tool, start_ts 
        FROM sessions 
        WHERE end_ts IS NULL
    ''')
    running = c.fetchall()
    conn.close()
    now = int(time.time())
    for tool, start in running:
        duration = now - start
        if duration < 0:
            continue
        total_sec += duration
        if tool not in stats:
            stats[tool] = {"runs": 0, "total_sec": 0, "last_start": 0}
        stats[tool]["total_sec"] += duration
        # Кількість запусків не збільшуємо, бо це ще незавершений
        # можна додати +1, щоб показати, що він запущений
        # але ми не знаємо, чи він вважається "запуском" – поки не завершився
        # Тому додаємо +1 тільки якщо це не перший запис
        # Краще не збільшувати runs, щоб статистика була консистентною після завершення
        # Але час додаємо.
        if start > stats[tool]["last_start"]:
            stats[tool]["last_start"] = start

    total_hours = total_sec / 3600.0
    return stats, total_hours

def format_duration(seconds: int) -> str:
    """Перетворити секунди у читабельний рядок (наприклад, 2h 15m)."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if secs and not hours:
        parts.append(f"{secs}s")
    return " ".join(parts) if parts else "0s"
