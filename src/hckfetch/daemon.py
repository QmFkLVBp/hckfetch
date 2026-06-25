#!/usr/bin/env python3
import time
import psutil
import signal
import sys
from pathlib import Path
from .config import get_tools, DB_FILE
from .analyzer import init_db, add_session

# Глобальні змінні для graceful shutdown
running = True

def signal_handler(sig, frame):
    global running
    running = False
    print("\nДемон зупинено.", file=sys.stderr)

def main():
    init_db()
    tools = set(get_tools())
    if not tools:
        print("Немає інструментів для відстеження. Перевірте конфіг.", file=sys.stderr)
        return

    # {pid: (tool_name, start_timestamp)}
    tracked = {}
    # Для швидкого пошуку: pid -> tool (запам'ятовуємо при старті)
    # Також потрібно знати, які процеси були зафіксовані як запущені, але ще не завершені.

    print(f"Демон запущено. Відстежуємо {len(tools)} інструментів.", file=sys.stderr)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while running:
        now = int(time.time())
        # Отримати всі поточні процеси
        current_pids = set()
        # Словник pid -> (tool, create_time) для нових
        for proc in psutil.process_iter(['pid', 'name', 'create_time']):
            try:
                name = proc.info['name']
                if name and name in tools:
                    pid = proc.info['pid']
                    create_time = int(proc.info['create_time'])
                    current_pids.add(pid)
                    if pid not in tracked:
                        # Новий процес
                        tracked[pid] = (name, create_time)
                        add_session(name, create_time)
                        # print(f"Старт: {name} (PID {pid})", file=sys.stderr)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Перевірити, які процеси зникли
        to_remove = []
        for pid, (tool, start_ts) in tracked.items():
            if pid not in current_pids:
                # Процес завершився – логуємо end
                add_session(tool, start_ts, now)
                # print(f"Завершено: {tool} (PID {pid})", file=sys.stderr)
                to_remove.append(pid)
        for pid in to_remove:
            del tracked[pid]

        time.sleep(0.5)  # перевіряємо кожні 0.5 с

    # Завершення демона – записуємо end для всіх незавершених
    now = int(time.time())
    for pid, (tool, start_ts) in tracked.items():
        add_session(tool, start_ts, now)
    print("Демон завершено.", file=sys.stderr)

if __name__ == "__main__":
    main()
