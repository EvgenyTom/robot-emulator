#!/usr/bin/env python3
"""
Эмулятор клавиш для робота (исправленная версия).
Использует pydirectinput для надёжной отправки в игры.
"""

import sys
import time
import argparse
import pydirectinput

def main():
    parser = argparse.ArgumentParser(description="Эмулятор команд для робота")
    parser.add_argument("commands_file", help="Путь к файлу с командами")
    parser.add_argument("--delay", "-d", type=float, default=1.0,
                        help="Задержка после каждого нажатия (сек). По умолчанию 1.0")
    args = parser.parse_args()

    # Чтение файла
    try:
        with open(args.commands_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() != ""]
    except FileNotFoundError:
        print(f"Ошибка: файл '{args.commands_file}' не найден.")
        input("Нажмите Enter для выхода...")
        sys.exit(1)

    if len(lines) < 2:
        print("Ошибка: файл должен содержать минимум две строки (ширина и высота).")
        input("Нажмите Enter для выхода...")
        sys.exit(1)

    try:
        width = int(lines[0])
        height = int(lines[1])
        commands = lines[2:]
    except ValueError:
        print("Ошибка: первые две строки должны быть целыми числами.")
        input("Нажмите Enter для выхода...")
        sys.exit(1)

    print(f"Размер поля: {width} x {height}")
    print(f"Всего команд: {len(commands)}")
    print(f"Задержка после каждого нажатия: {args.delay} сек")
    print("Переключитесь на окно игры. Старт через 5 секунд...")
    time.sleep(5)

    # Основной цикл
    for i, cmd in enumerate(commands, 1):
        print(f"[{i}/{len(commands)}] {cmd}")

        if cmd == "Shift+S":
            # 1. Нажать Shift+S (вручную)
            pydirectinput.keyDown('shift')
            time.sleep(0.05)
            pydirectinput.press('s')
            time.sleep(0.05)
            pydirectinput.keyUp('shift')
            time.sleep(0.05)
            # 2. Нажать Z
            pydirectinput.press('z')
            time.sleep(args.delay)

        elif cmd in ("A", "D", "W"):
            key = cmd.lower()
            # 1. Нажать Shift+клавиша
            pydirectinput.keyDown('shift')
            time.sleep(0.05)
            pydirectinput.press(key)
            time.sleep(0.05)
            pydirectinput.keyUp('shift')
            time.sleep(0.05)
            # 2. Нажать Z
            pydirectinput.press('z')
            time.sleep(args.delay)
            # 3. Нажать просто клавишу
            pydirectinput.press(key)
            time.sleep(args.delay)

        else:
            # Остальные команды (J, K, L, M, N, ...)
            pydirectinput.press(cmd.lower())
            time.sleep(args.delay)

    print("✅ Эмуляция завершена.")
    input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()
