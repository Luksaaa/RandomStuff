import random
import time
import threading
import msvcrt
import sys

REFRESH_TIME = 12 
paused = False
running = True
lock = threading.Lock()
MODE = 1


COMMON_DEF_CUES = [
    "Slip(Dolje)", "Duck(Cucanj)", "Roll(L/R Cucanj)", "Parry(Take a hit)", "Block", "Pivot(Promjeni smjer)", "Step Back"
]

ALL_DEF_CUES = [
    "Slip", "Slip L", "Slip R",
    "Duck", "Bob", "Weave", "Bob & Weave",
    "Roll", "Roll Under", "Pull Back", "Lean Back",
    "Block", "High Guard", "Cover", "Shell",
    "Parry", "Catch", "Catch & Shoot", "Frame",
    "Step Back", "Step In", "Pivot", "Angle",
    "Side Step", "Slide Left", "Slide Right",
    "Circle Left", "Circle Right",
    "Clinch", "Tie Up", "Smother", "Push Off", "Inside Control",
    "Cut the Angle", "Get Off the Line", "Reset",
    "Hold Center", "Corner Out", "Back to Center",
    "Slip & Counter", "Roll & Fire",
    "Block & Counter", "Parry & Jab", "Catch & Cross"
]


def generate_normal_combo():
    return [random.randint(1, 6) for _ in range(random.randint(3, 6))]

def generate_komb_combo():
    length = random.choices([2, 3, 4, 5], weights=[30, 30, 30, 10])[0]
    combo, backhand = [], 0

    for _ in range(length):
        punch = random.randint(1, 6)

        if punch in (2, 4, 6):
            backhand += 1
            if backhand > 2:
                punch = 1
        else:
            backhand = 0

        if punch in (5, 6) and random.random() < 0.6:
            punch = random.choice([1, 2, 3])

        combo.append(punch)

    return combo

def generate_def_cue():
    if MODE == 3:
        return random.choice(COMMON_DEF_CUES)
    if MODE == 4:
        return random.choice(ALL_DEF_CUES)
    return ""


def print_combo():
    with lock:
        if not running:
            return

        if MODE == 1:
            combo = generate_normal_combo()
            print_block("PUNCH COMBINATION", combo)
            return

        if MODE == 2:
            combo = generate_komb_combo()
            print_block("Combo", combo)
            return

        combo1 = generate_komb_combo()
        combo2 = generate_komb_combo()
        cue = generate_def_cue()

        line = f"{' - '.join(map(str, combo1))} {cue} - {' - '.join(map(str, combo2))}"

        print("\n==============================")
        print(" Combo:")
        print(" ", line)
        print("==============================")
        print("[ENTER] New  |  [SPACE] Pause  |  [ESC] Stop")

def print_block(title, combo):
    print("\n==============================")
    print(f" {title}:")
    print(" ", " - ".join(map(str, combo)))
    print("==============================")
    print("[ENTER] New  |  [SPACE] Pause  |  [ESC] Stop")

def timer_loop():
    global running
    while running:
        for _ in range(REFRESH_TIME):
            time.sleep(1)
            if not running or paused:
                break
        if running and not paused:
            print_combo()

def keyboard_loop():
    global paused, running
    while running:
        if msvcrt.kbhit():
            key = msvcrt.getch()

            if key == b'\r' and not paused:
                print_combo()

            elif key == b' ':
                with lock:
                    paused = not paused
                    print(f"\n--- {'PAUSED' if paused else 'RESUMED'} ---")

            elif key == b'\x1b':  # exit sa esc
                with lock:
                    running = False
                return

        time.sleep(0.05)

def select_mode():
    print("\nBOXING TRAINING GENERATOR")
    print("-------------------------")
    print("1 - NORMAL (random)")
    print("2 - COMBO (real boxing)")
    print("3 - COMBO + DEF (common 7 coach cues)")
    print("4 - COMBO + DEF (ALL 44 defensive cues)")

    while True:
        choice = input("Select mode (1-4): ").strip()
        if choice in ("1", "2", "3", "4"):
            return int(choice)

def main():
    global MODE, running, paused

    while True:
        MODE = select_mode()
        running = True
        paused = False

        print_combo()

        t1 = threading.Thread(target=timer_loop)
        t2 = threading.Thread(target=keyboard_loop)

        t1.start()
        t2.start()

        t2.join()
        t1.join()

        answer = input("\nDo you want to restart? (Y/N): ").strip().upper()
        if answer != "Y":
            sys.exit()

if __name__ == "__main__":
    main()
