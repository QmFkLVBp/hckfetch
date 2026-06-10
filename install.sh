#!/usr/bin/env bash

# Встановлення hckfetch
# Працює в Linux та Termux

set -e

INSTALL_DIR="$HOME/.local/bin"
SCRIPT_NAME="hckfetch"
WRAP_NAME="hckfetch-wrap"

# Створюємо теку для встановлення, якщо її немає
mkdir -p "$INSTALL_DIR"

# Перевіряємо, чи існують файли вихідників
if [ ! -f "./$SCRIPT_NAME" ] || [ ! -f "./$WRAP_NAME" ]; then
    echo "Помилка: не знайдено файлів $SCRIPT_NAME або $WRAP_NAME у поточній теці."
    echo "Запустіть скрипт із кореня репозиторію hckfetch."
    exit 1
fi

# Копіюємо з правами на виконання
cp "./$SCRIPT_NAME" "$INSTALL_DIR/"
cp "./$WRAP_NAME" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/$SCRIPT_NAME"
chmod +x "$INSTALL_DIR/$WRAP_NAME"

echo "Файли скопійовано до $INSTALL_DIR"

# Додаємо ~/.local/bin до PATH, якщо його ще немає
# Визначаємо, який файл конфігурації використовується
SHELL_RC=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ] || [ -n "$TERMUX_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
else
    # За замовчуванням .bashrc
    SHELL_RC="$HOME/.bashrc"
fi

# Перевіряємо, чи вже є запис про ~/.local/bin у PATH
if [ -f "$SHELL_RC" ]; then
    if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo '# Додано hckfetch: додаємо ~/.local/bin до PATH' >> "$SHELL_RC"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        echo "Додано $INSTALL_DIR до PATH у $SHELL_RC"
    else
        echo "PATH вже налаштовано у $SHELL_RC"
    fi
else
    # Якщо файлу конфігурації немає, створюємо .bashrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' > "$SHELL_RC"
    echo "Створено $SHELL_RC з налаштуванням PATH"
fi

# Робимо PATH доступним у поточній сесії
export PATH="$HOME/.local/bin:$PATH"

echo "Готово! Тепер команда 'hckfetch' має бути доступна."
echo "Спробуйте запустити: hckfetch"
