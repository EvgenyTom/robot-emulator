#!/usr/bin/env python3
"""
Робот-эмулятор клавиш (исправленная версия)
Поддерживает:
- Запуск с аргументом: robot_emulator.exe commands.txt --delay 0.5
- Запуск без аргументов: программа попросит ввести имя файла
"""

import sys
import time
import argparse
import pyautogui

# Настройки
DEFAULT_DELAY = 1.0          # задержка между командами (сек)
PAUSE_AFTER_Z = 0.05         # пауза между Z и основной клавишей

def press_command(command):
    """Выполняет одно действие: Z + основная клавиша."""
    print(f"   → Нажимаю Z, затем {command}")
    pyautogui.press('z')
    time.sleep(PAUSE_AFTER_Z)
    
    if command == "Shift+S":
        pyautogui.hotkey('shift', 's')
    else:
        # Для одиночных клавиш (a, d, w, j, k, l, m, n...)
        pyautogui.press(command.lower())

def main():
    # --- Разбор аргументов командной строки ---
    parser = argparse.ArgumentParser(description="Эмулятор клавиш для робота")
    parser.add_argument("commands_file", nargs="?", help="Путь к файлу с командами")
    parser.add_argument("--delay", "-d", type=float, default=DEFAULT_DELAY,
                        help=f"Задержка после каждой команды (сек), по умолчанию {DEFAULT_DELAY}")
    args = parser.parse_args()

    # --- Получение имени файла ---
    filename = args.commands_file
    if not filename:
        # Если не передан аргументом, спрашиваем у пользователя
        filename = input("Введите имя файла с командами (например, robot_commands.txt): ").strip()
        if not filename:
            print("Ошибка: имя файла не может быть пустым.")
            input("Нажмите Enter для выхода...")
            sys.exit(1)

    # --- Чтение файла ---
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() != ""]
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
        input("Нажмите Enter для выхода...")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        input("Нажмите Enter для выхода...")
        sys.exit(1)

    # --- Проверка формата ---
    if len(lines) < 2:
        print("Ошибка: файл должен содержать минимум две строки (ширина и высота).")
        input("Нажмите Enter для выхода...")
        sys.exit(1)

    try:
        width = int(lines[0])
        height = int(lines[1])
        commands = lines[2:]
    except ValueError:
        print("Ошибка: первые две строки должны быть целыми числами (ширина и высота).")
        input("Нажмите Enter для выхода...")
        sys.exit(1)

    # --- Вывод информации ---
    print(f"\n{'='*50}")
    print(f"Размер поля: {width} x {height}")
    print(f"Всего команд: {len(commands)}")
    print(f"Задержка между командами: {args.delay} сек")
    print(f"Пауза после Z: {PAUSE_AFTER_Z} сек")
    print(f"{'='*50}")
    print("Переключитесь на окно игры в течение 5 секунд...")
    time.sleep(5)
    print("НАЧИНАЮ ЭМУЛЯЦИЮ. Для остановки нажмите Ctrl+C.\n")

    # --- Основной цикл ---
    try:
        for i, cmd in enumerate(commands, 1):
            if not cmd:
                continue
            # Показываем прогресс
            print(f"[{i:4d}/{len(commands)}] {cmd}")
            press_command(cmd)
            # Основная задержка после команды
            time.sleep(args.delay)
    except KeyboardInterrupt:
        print("\n\nПрерывание пользователя. Эмуляция остановлена.")
    except Exception as e:
        print(f"\nОшибка во время выполнения: {e}")
    else:
        print("\n✅ Эмуляция завершена успешно.")
    
    input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()
