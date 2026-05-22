#!/usr/bin/env python3
"""
Робот-эмулятор клавиш.
Читает текстовый файл (формат: ширина, высота, затем список команд).
Для каждой команды:
  1. Нажимает клавишу Z
  2. Нажимает основную клавишу/комбинацию
  3. Ждёт заданную задержку (по умолчанию 1 секунда)

Требования: установить pyautogui
   pip install pyautogui
"""

import sys
import time
import argparse
import pyautogui

# Небольшая пауза между нажатием Z и основной командой (сек)
PAUSE_AFTER_Z = 0.05

def parse_arguments():
    parser = argparse.ArgumentParser(description="Эмуляция нажатий клавиш для робота из текстового файла.")
    parser.add_argument("commands_file", help="Путь к текстовому файлу с командами")
    parser.add_argument("--delay", "-d", type=float, default=1.0,
                        help="Задержка после каждой команды (секунды). По умолчанию 1.0")
    parser.add_argument("--pause-after-z", type=float, default=0.05,
                        help="Пауза между Z и основной клавишей (сек). По умолчанию 0.05")
    return parser.parse_args()

def press_command(command, pause_after_z):
    """Выполняет одно действие: Z + основная клавиша."""
    # 1. Нажать Z
    pyautogui.press('z')
    time.sleep(pause_after_z)

    # 2. Основная клавиша
    if command == "Shift+S":
        pyautogui.hotkey('shift', 's')
    else:
        # Для одиночных клавиш (J, D, A, W, K, L, M, N и т.д.)
        # Приводим к нижнему регистру, т.к. press ожидает 'j', а не 'J'
        pyautogui.press(command.lower())

def main():
    args = parse_arguments()

    try:
        with open(args.commands_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() != ""]
    except FileNotFoundError:
        print(f"Ошибка: файл {args.commands_file} не найден.")
        sys.exit(1)

    if len(lines) < 2:
        print("Ошибка: файл должен содержать минимум две строки (ширина и высота).")
        sys.exit(1)

    try:
        width = int(lines[0])
        height = int(lines[1])
        commands = lines[2:]
    except ValueError:
        print("Ошибка: первые две строки должны быть целыми числами (ширина и высота).")
        sys.exit(1)

    print(f"Размер поля: {width} x {height}")
    print(f"Всего команд: {len(commands)}")
    print(f"Задержка после команды: {args.delay} сек")
    print(f"Пауза после Z: {args.pause_after_z} сек")
    print("Старт через 3 секунды... Наведите мышь на окно игры и не двигайте её.")
    time.sleep(3)
    print("Начинаем эмуляцию... Нажмите Ctrl+C для прерывания.")

    try:
        for i, cmd in enumerate(commands, 1):
            # Пропускаем пустые строки (на всякий случай)
            if not cmd:
                continue
            # Выводим прогресс (каждые 100 команд или если команда особенная)
            if i % 100 == 0 or i == 1:
                print(f"Команда {i}/{len(commands)}: {cmd}")

            press_command(cmd, args.pause_after_z)

            # Основная задержка после всей команды
            time.sleep(args.delay)
    except KeyboardInterrupt:
        print("\nПрерывание пользователя. Эмуляция остановлена.")
    except Exception as e:
        print(f"\nОшибка: {e}")

    print("Эмуляция завершена.")

if __name__ == "__main__":
    main()