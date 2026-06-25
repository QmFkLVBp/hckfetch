import time
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from pyfiglet import Figlet
from .config import get_logo_path
from .levels import get_level
from .analyzer import format_duration

def get_ascii_art() -> str | None:
    """
    Повертає вміст файлу logo.txt, якщо він існує.
    Якщо файлу немає — повертає None (арт не виводиться).
    """
    logo_path = get_logo_path()
    if logo_path and logo_path.exists():
        with open(logo_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def render(stats: dict, total_hours: float):
    """Головна функція візуалізації — без вбудованих артів."""
    console = Console()

    # 1. ASCII-арт (тільки якщо є файл)
    art = get_ascii_art()
    if art:
        console.print(Panel(art, style="bold bright_yellow", border_style="bright_blue", width=80))
    else:
        # Якщо арту немає — виводимо просто декоративну риску
        console.print("─" * 60, style="dim")

    # 2. Банер рівня (через pyfiglet)
    level_name = get_level(total_hours)
    try:
        clean_name = level_name.split(" ", 1)[-1] if " " in level_name else level_name
        level_banner = Figlet(font="slant").renderText(clean_name)
    except Exception:
        level_banner = level_name

    emoji = level_name.split(" ", 1)[0] if " " in level_name else "🔥"
    console.print(f"{emoji}  {level_banner}", style="bold cyan")

    # 3. Загальний час та кількість інструментів
    hours_int = int(total_hours)
    minutes = int((total_hours - hours_int) * 60)
    console.rule(f"[bold white]Загальний час: {hours_int} год {minutes} хв  |  Інструментів: {len(stats)}[/]")

    # 4. Таблиця з топ-інструментами
    if stats:
        table = Table(title="🏆 Топ інструментів за часом", show_lines=True, header_style="bold magenta")
        table.add_column("№", style="dim", width=4, justify="right")
        table.add_column("Інструмент", style="cyan", no_wrap=True)
        table.add_column("Час", style="green")
        table.add_column("Запусків", style="yellow", justify="right")
        table.add_column("Останній запуск", style="blue", no_wrap=True)

        sorted_items = sorted(stats.items(), key=lambda x: x[1]["total_sec"], reverse=True)
        for idx, (tool, data) in enumerate(sorted_items[:15], 1):
            time_str = format_duration(data["total_sec"])
            last_str = time.ctime(data["last_start"]) if data["last_start"] else "Немає"
            table.add_row(str(idx), tool, time_str, str(data["runs"]), last_str)

        console.print(table)
    else:
        console.print("[italic bright_black]Статистики поки немає. Запустіть будь-який інструмент зі списку.[/]")

    # 5. Підпис
    console.print(Align.right(f"[dim]~ hckfetch v2.0 | {time.strftime('%Y-%m-%d %H:%M')} ~[/]"))
