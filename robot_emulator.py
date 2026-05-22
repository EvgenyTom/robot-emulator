#!/usr/bin/env python3
"""
Эмулятор клавиш для робота.
Правила:
- Shift+S -> нажать Shift+S, потом Z
- A, D, W -> нажать Shift+клавиша, потом Z, потом просто клавиша
- Остальные (J, K, L, M, N...) -> только клавиша
После каждого нажатия делается пауза (задержка).
"""

import sys
import time
import argparse
import pydirectinput as pyautogui

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
        sys.exit(1)

    if len(lines) < 2:
        print("Ошибка: файл должен содержать минимум две строки (ширина и высота).")
        sys.exit(1)

    try:
        width = int(lines[0])
        height = int(lines[1])
        commands = lines[2:]
    except ValueError:
        print("Ошибка: первые две строки должны быть целыми числами.")
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
            # 1. Shift+S
            pyautogui.hotkey('shift', 's')
            time.sleep(args.delay)
            # 2. Z
            pyautogui.press('z')
            time.sleep(args.delay)

        elif cmd in ("A", "D", "W"):
            key = cmd.lower()  # 'a', 'd', 'w'
            # 1. Shift + клавиша
            pyautogui.hotkey('shift', key)
            time.sleep(args.delay)
            # 2. Z
            pyautogui.press('z')
            time.sleep(args.delay)
            # 3. просто клавиша
            pyautogui.press(key)
            time.sleep(args.delay)

        else:
            # Остальные команды (J, K, L, M, N...)
            pyautogui.press(cmd.lower())
            time.sleep(args.delay)

    print("✅ Эмуляция завершена.")

if __name__ == "__main__":
    main()
