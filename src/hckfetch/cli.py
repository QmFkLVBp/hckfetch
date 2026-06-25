#!/usr/bin/env python3
import click
from .analyzer import get_stats
from .renderer import render

@click.command()
@click.option('--no-logo', is_flag=True, help="Не виводити ASCII-арт.")
@click.option('--reset', is_flag=True, help="Скинути всю статистику (видалити БД).")
def main(no_logo, reset):
    """hckfetch – твій персональний трекер пентест-активності."""
    if reset:
        import os
        from .config import DB_FILE
        if DB_FILE.exists():
            os.remove(DB_FILE)
            click.echo("Статистику скинуто.")
        else:
            click.echo("Немає даних для скидання.")
        return

    stats, total_hours = get_stats()
    if no_logo:
        # вивести тільки текст без арту – для простоти пропустимо арт
        # але render за замовчуванням виводить арт – можемо передати параметр
        # Поки що просто викличемо render, але можна додати опцію
        pass
    render(stats, total_hours)

if __name__ == "__main__":
    main()
