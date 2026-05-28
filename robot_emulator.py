#!/usr/bin/env python3
import sys, time, argparse, os, threading
import pydirectinput
import keyboard

PROGRESS_FILE = "progress.txt"
paused = False
running = True
current_index = 0
total_commands = 0
commands_list = []
width = height = 0
args = None

def listen_hotkey():
    global paused, running
    while running:
        if keyboard.is_pressed('p'):
            paused = not paused
            print(f"\n*** {'ПАУЗА' if paused else 'ПРОДОЛЖЕНИЕ'} ***")
            if paused:
                save_progress()
            time.sleep(0.5)
        time.sleep(0.1)

def save_progress():
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        f.write(f"{current_index}\n{width}\n{height}\n{args.delay}\n")
        for cmd in commands_list:
            f.write(cmd + "\n")
    print(f"💾 Прогресс сохранён (команда {current_index})")

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return 0, [], 0, 0, 1.0
    with open(PROGRESS_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    if len(lines) < 4:
        return 0, [], 0, 0, 1.0
    idx = int(lines[0]); w = int(lines[1]); h = int(lines[2]); delay = float(lines[3]); cmds = lines[4:]
    return idx, cmds, w, h, delay

def execute_action(action, delay_between_chars=0.05):
    if not action:
        return
    for ch in action:
        if ch == ' ':
            continue
        pydirectinput.press(ch.lower())
        time.sleep(delay_between_chars)

def main():
    global paused, running, current_index, total_commands, commands_list, width, height, args
    parser = argparse.ArgumentParser()
    parser.add_argument("commands_file", nargs="?", help="Файл команд")
    parser.add_argument("--delay", "-d", type=float, default=1.0)
    args = parser.parse_args()

    start_idx, saved_cmds, saved_w, saved_h, saved_delay = load_progress()
    if start_idx > 0:
        print(f"Найден прогресс: выполнено {start_idx} команд")
        choice = input("Продолжить? (C - да, N - заново): ").strip().lower()
        if choice == 'c':
            commands_list = saved_cmds
            width, height = saved_w, saved_h
            args.delay = saved_delay
            current_index = start_idx
        else:
            os.remove(PROGRESS_FILE)
            if not args.commands_file:
                print("Укажите файл команд")
                sys.exit(1)
            with open(args.commands_file, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
            width = int(lines[0]); height = int(lines[1]); commands_list = lines[2:]
            current_index = 0
    else:
        if not args.commands_file:
            print("Укажите файл команд")
            sys.exit(1)
        with open(args.commands_file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        width = int(lines[0]); height = int(lines[1]); commands_list = lines[2:]

    total_commands = len(commands_list)
    if current_index >= total_commands:
        print("Все команды уже выполнены")
        if os.path.exists(PROGRESS_FILE): os.remove(PROGRESS_FILE)
        return

    print(f"Размер: {width}x{height}, команд: {total_commands}, старт с {current_index+1}")
    print("Нажмите P для паузы. Переключитесь на окно игры через 5 секунд...")
    time.sleep(5)

    hotkey_thread = threading.Thread(target=listen_hotkey, daemon=True)
    hotkey_thread.start()

    i = current_index
    while i < total_commands:
        if paused:
            time.sleep(0.2)
            continue
        cmd = commands_list[i]
        print(f"[{i+1}/{total_commands}] {cmd}")
        current_index = i + 1

        if cmd == "Shift+S":
            pydirectinput.keyDown('shift'); time.sleep(0.05)
            pydirectinput.press('s'); time.sleep(0.05)
            pydirectinput.keyUp('shift'); time.sleep(0.05)
            pydirectinput.press('z'); time.sleep(args.delay)
        elif cmd in ("A","D","W"):
            key = cmd.lower()
            pydirectinput.keyDown('shift'); time.sleep(0.05)
            pydirectinput.press(key); time.sleep(0.05)
            pydirectinput.keyUp('shift'); time.sleep(0.05)
            pydirectinput.press('z'); time.sleep(args.delay)
            pydirectinput.press(key); time.sleep(args.delay)
        else:
            execute_action(cmd, delay_between_chars=0.05)
            time.sleep(args.delay)
        i += 1

    print("✅ Эмуляция завершена")
    if os.path.exists(PROGRESS_FILE): os.remove(PROGRESS_FILE)
    input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()
