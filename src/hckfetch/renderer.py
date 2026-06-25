import random
import time
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from pyfiglet import Figlet
from .config import get_logo_path, get_levels
from .levels import get_level
from .analyzer import format_duration

# Вбудовані ASCII-арти (якщо logo.txt не задано)
BUILTIN_ART = [
    r"""
    ⠀⠀⠀⠀⠀⢀⣠⣤⣶⣶⣶⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀
    """,
    r"""
      ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
     ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌
     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌
     ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌
     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
     ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌
     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌
     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌
     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌
     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌
    """,
    r"""
        _.-="_-         _
       _.-="   _-          | ||"""""""---._______     __..
   .--"   .-="             | ||               .--" __.."
  ."     ."                | ||            .-" _.-"
 /     ."                  | ||          ."  ."
/     /                    | ||         /   /
|    |                     | ||        /   /
|    |                     | ||       /   /
|    |                    /  ||      /   /
 \   |                   /   ||     /   /
  \  |                  /   _||    /   /
   \ \                 /   / ||   /   /
    \ \                \  /  ||  /   /
     \ \                \/   || /   /
      \ \                 /  ||/   /
       \ \         .-"    |  ||   /
        \ \       /       |  ||  /
         \ \     /        |  || /
          \ \   /         |  ||/
           \ \ /          |  ||
            \ |           |  ||
            /             |  |
           /              |  |
          /               |  |
         /                /  |
        |                /   |
        |               /    |
        |              /     |
         \            /      |
          \          /       |
           \        /        |
            \      /         |
             \    /          |
              \  /           |
               \/            |
    """
]

def get_ascii_art(use_random: bool = True) -> str:
    """Повертає ASCII-арт з файлу або випадковий вбудований."""
    logo_path = get_logo_path()
    if logo_path and logo_path.exists():
        with open(logo_path, 'r') as f:
            return f.read()
    # Якщо файл не існує, беремо випадковий вбудований
    if use_random:
        return random.choice(BUILTIN_ART)
    else:
        return BUILTIN_ART[0]  # перший за замовчуванням

def render(stats: dict, total_hours: float):
    """Головна функція виводу."""
    console = Console()

    # 1. ASCII-арт
    art = get_ascii_art(use_random=True)  # можна зробити конфігураційним
    console.print(Panel(art, style="bold yellow", border_style="bright_blue"))

    # 2. Рівень
    level_name = get_level(total_hours)
    # Генеруємо банер рівня через pyfiglet (опціонально)
    try:
        level_banner = Figlet(font="slant").renderText(level_name.split(" ", 1)[-1] if " " in level_name else level_name)
    except:
        level_banner = level_name
    console.print(level_banner, style="bold cyan")

    # 3. Загальна інформація
    console.print(f"[bold]Загальний час:[/] [green]{format_duration(int(total_hours * 3600))}[/]")
    console.print(f"[bold]Кількість інструментів:[/] [yellow]{len(stats)}[/]")

    # 4. Таблиця топ-інструментів (за часом)
    if stats:
        table = Table(title="Статистика інструментів", show_lines=True)
        table.add_column("Інструмент", style="cyan", no_wrap=True)
        table.add_column("Час", style="green")
        table.add_column("Запусків", style="magenta", justify="right")
        table.add_column("Останній запуск", style="blue")

        # Сортуємо за часом (спадання)
        sorted_items = sorted(stats.items(), key=lambda x: x[1]["total_sec"], reverse=True)
        for tool, data in sorted_items[:15]:  # топ-15
            time_str = format_duration(data["total_sec"])
            last_str = time.ctime(data["last_start"]) if data["last_start"] else "Невідомо"
            table.add_row(tool, time_str, str(data["runs"]), last_str)

        console.print(table)
    else:
        console.print("[italic]Поки що немає даних. Запустіть будь-який інструмент зі списку.[/]")

    # 5. Поточний запущений процес (якщо є)
    # можна показати, які інструменти зараз виконуються – додатково
