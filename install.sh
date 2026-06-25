#!/bin/bash
set -e

echo "Встановлення hckfetch..."

# Переконатися, що poetry встановлено
if ! command -v poetry &> /dev/null; then
    echo "poetry не знайдено. Встановлюємо..."
    pip install poetry
fi

# Встановити проект
poetry install --only main

# Створити симлінки на виконувані файли (у ~/.local/bin)
mkdir -p ~/.local/bin
poetry run which hckfetch | xargs -I {} ln -sf {} ~/.local/bin/hckfetch
poetry run which hckfetch-daemon | xargs -I {} ln -sf {} ~/.local/bin/hckfetch-daemon

# Додати ~/.local/bin у PATH, якщо ще немає
if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' ~/.bashrc; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi
if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' ~/.zshrc; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
fi

# Налаштувати systemd --user для автозапуску демона
mkdir -p ~/.config/systemd/user
cp hckfetch.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable hckfetch.service
systemctl --user start hckfetch.service

echo "Встановлення завершено. Демон запущено."
echo "Використовуйте команду hckfetch для перегляду статистики."
