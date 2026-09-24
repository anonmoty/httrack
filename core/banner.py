# core/banner.py
# ============================================
#   HTTrackX — GIANT SKULL Matrix Banner v6.0
#   ☠️ Giant Skull + Falling Matrix Rain
#   RED + DARK GREEN | Full Screen | 3 Sec
# ============================================

import sys
import os
import time
import random
import shutil

from core.colors import C

# ── Custom Hacker Colors ──
RED = '\033[1;31m'
DARK_GREEN = '\033[1;32m'
DIM_GREEN = '\033[2;32m'
BRIGHT_RED = '\033[1;91m'
DIM_RED = '\033[2;31m'
WHITE = '\033[1;37m'
DIM = '\033[2;90m'
RESET = '\033[0m'
HIDE_CURSOR = '\033[?25l'
SHOW_CURSOR = '\033[?25h'
HOME = '\033[H'

# ── Matrix Characters with Skulls ──
MATRIX = list("01アイウエオカキクケコ{}[]<>|=+-*&^%$#@!░▓█╬╫")
SKULL_CHARS = ["☠️", "☠", "💀", "𖤍"]

# ── GIANT SKULL BRAILLE ART (Red + Dark Green Alternate) ──
# Note: Syntax fully fixed to prevent invalid escape errors!
GIANT_SKULL = [
    ("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", RED),
    ("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⠿⠛⠛⠛⠉⠛⠫⠿⢷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", DARK_GREEN),
    ("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢻⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", RED),
    ("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢹⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", DARK_GREEN),
    ("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", RED),
    ("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", DARK_GREEN),
    ("⠀⠀⠀⢀⣤⣦⣤⣤⣄⠀⠀⣿⣤⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⠘⣿⠇⠀⣀⣀⣀⡀⠀⠀⠀⠀⠀", RED),
    ("⠀⠀⣰⣿⠁⠀⠀⠀⠉⣧⣀⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠙⢾⣿⣢⡿⠛⠉⠙⠛⢷⣦⡄⠀⠀", DARK_GREEN),
    ("⠀⠀⢿⣷⠀⠀⠀⠀⠸⣿⣿⠃⢠⣴⣶⣤⣾⣿⣿⣧⢀⠀⢠⣾⣿⣷⣄⣀⣤⡄⠀⠹⣿⣷⠀⠀⠀⠀⢀⣿⠃⠀⠀", RED),
    ("⠀⣴⣾⠿⣷⡄⠀⠀⠀⠙⣿⣆⠸⣿⣿⣿⣿⣿⣿⡏⠀⠀⠸⣿⣿⣿⣿⣿⣿⡗⠀⢰⣿⠟⠀⠀⠀⣨⣾⣧⣄⠀⠀", DARK_GREEN),
    ("⣾⡿⠁⢰⡿⠁⠀⠀⠀⠀⢸⣿⠀⠹⣹⣿⣿⣿⡿⠈⢀⡀⠀⠀⢿⣿⣿⣿⡿⠁⠀⣿⡏⠀⠀⠀⠈⠿⡇⠈⠹⣿⡀", RED),
    ("⢿⡇⠀⠀⠀⠀⢀⡀⠀⠀⠘⣿⣀⠀⠈⠙⢿⠃⠀⣴⣿⣷⣄⠀⠈⠿⠛⠁⠀⠀⣁⣿⠇⠀⠀⠀⠀⠀⠁⠀⠀⢹⡇", DARK_GREEN),
    ("⠸⣿⣤⣀⣠⣤⠿⠟⠻⠶⢶⣤⡙⢻⣷⣦⡀⠀⠀⢿⠟⠿⠟⠀⠀⠀⢀⣴⣷⡛⣉⣡⣤⣤⠶⢶⣦⡀⠀⣀⣤⡟⠀", RED),
    ("⠀⠀⣀⣤⣤⣤⣄⠀⠀⠠⠀⠀⠉⣻⣟⣡⢀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢀⢈⣿⡟⠋⠁⠀⠀⠀⠀⢉⣛⡛⠛⠉⠀⠀", DARK_GREEN),
    ("⢠⣿⠋⠉⠀⠈⢻⣧⣀⣤⣶⡶⠿⠿⣿⣿⣾⡄⣸⠀⢰⡆⠀⢴⠀⢻⣜⣿⣿⢷⣶⣄⡀⠀⢀⣼⡿⠛⠛⢷⣦⡀⠀", RED),
    ("⣸⣇⠀⠀⠀⠀⠀⠙⠋⠉⠀⠀⠀⠀⢈⣙⣿⣿⣿⣷⡾⡿⣦⣿⣿⣾⡏⠈⠀⠀⠀⠉⠛⠛⠛⠉⠀⠀⠀⠀⣻⣷⠀", DARK_GREEN),
    ("⠸⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡶⠟⠋⠁⠉⠀⠀⠀⠀⠀⠀⠈⠉⠛⠶⢦⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⠇⠀", RED),
    ("⠀⢀⣽⣿⠻⡇⠀⠀⠀⢰⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⣷⡄⠀⠀⠀⣼⡾⢿⡋⠁⠀⠀", DARK_GREEN),
    ("⠀⢀⣿⣇⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣿⠀⠀⠀⠘⠠⢸⣇⠀⠀⠀", RED),
    ("⠀⠉⢿⣿⣀⠀⠀⠀⣠⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠀⠀⠀⠀⠀⠀⢿⡀⠀⠀⠀⠀⣼⡟⠀⠀⠀", DARK_GREEN),
    ("⠀⠀⠈⠙⠛⠷⠿⠿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⠶⠶⠶⠾⠋⠁⠀⠀⠀", RED)
]

# ── Falling skull shapes for Matrix Rain background ──
RAIN_SKULL = [
    "  ☠️☠️☠️  ",
    " ☠️💀☠️ ",
    "  ☠️☠️☠️  ",
]

def get_size():
    """Terminal dimensions determine karo"""
    try:
        return shutil.get_terminal_size((80, 24))
    except:
        return 80, 24

def clear():
    """OS clear execution"""
    os.system("cls" if os.name == "nt" else "clear")

def big_skull_matrix_rain(duration=3):
    """
    3 Seconds Full Screen Dark Skull Matrix Rain
    RED and DARK GREEN flowing engine
    """
    cols, rows = get_size()
    end_time = time.time() + duration

    # Background matrix drop vectors
    drops = [random.randint(-rows, 0) for _ in range(cols)]
    speeds = [random.uniform(0.5, 1.6) for _ in range(cols)]

    # Dynamic mid-air skull positions (animated overlay)
    big_skulls = []
    for _ in range(3):
        big_skulls.append({
            "x": random.randint(5, max(cols - 15, 10)),
            "y": random.randint(-10, -2),
            "speed": random.uniform(0.2, 0.5),
            "color": random.choice([RED, DARK_GREEN, BRIGHT_RED])
        })

    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()

    while time.time() < end_time:
        lines = []

        for row in range(rows - 1):
            line_chars = []
            for col in range(cols):
                drop_pos = int(drops[col])
                char = " "
                color = RESET

                # Drop heads logic
                if row == drop_pos:
                    if random.random() > 0.65:
                        char = random.choice(SKULL_CHARS)
                        color = random.choice([RED, BRIGHT_RED, WHITE])
                    else:
                        char = random.choice(MATRIX)
                        color = WHITE
                elif row == drop_pos - 1:
                    char = random.choice(["☠", "💀", "▓", "█"])
                    color = random.choice([RED, DARK_GREEN])
                elif row == drop_pos - 2:
                    char = random.choice(MATRIX)
                    color = DARK_GREEN
                elif row == drop_pos - 3:
                    char = random.choice(MATRIX)
                    color = DIM_GREEN
                elif row == drop_pos - 4:
                    char = "·"
                    color = DIM
                else:
                    if random.random() > 0.98:
                        char = random.choice(["☠", "💀", "0", "1"])
                        color = random.choice([DIM_RED, DIM_GREEN])

                line_chars.append(f"{color}{char}{RESET}")

            lines.append("".join(line_chars))

        # Overlay Skull Clusters on the Matrix Stream
        for skull in big_skulls:
            sy = int(skull["y"])
            sx = skull["x"]
            sc = skull["color"]

            for i, skull_line in enumerate(RAIN_SKULL):
                target_row = sy + i
                if 0 <= target_row < len(lines):
                    line = lines[target_row]
                    try:
                        before = line[:sx * 5]  # Colored characters buffer padding
                        after = line[(sx + len(skull_line)) * 5:]
                        skull_colored = f"{sc}{skull_line}{RESET}"
                        lines[target_row] = before + skull_colored + after
                    except:
                        pass

        # Flush raw stream
        sys.stdout.write(HOME)
        sys.stdout.write("\n".join(lines))
        sys.stdout.flush()

        # Update background drop iterations
        for col in range(cols):
            drops[col] += speeds[col]
            if drops[col] > rows + 5:
                drops[col] = random.randint(-15, -3)
                speeds[col] = random.uniform(0.5, 1.6)

        # Update mid-air skulls vertical vectors
        for skull in big_skulls:
            skull["y"] += skull["speed"]
            if skull["y"] > rows + 5:
                skull["y"] = random.randint(-15, -5)
                skull["x"] = random.randint(5, max(cols - 15, 10))
                skull["color"] = random.choice([RED, DARK_GREEN, BRIGHT_RED])

        time.sleep(0.06)

    sys.stdout.write(SHOW_CURSOR)
    sys.stdout.flush()

def show_giant_skull():
    """
    Shows Center-Aligned Giant Braille Skull (Cleaned & Fixed)
    """
    cols, _ = get_size()

    print()
    border = "☠️💀" * (cols // 4)
    print(f"  {RED}{border[:cols-4]}{RESET}")
    print()

    # Center-aligned output parser
    for line_text, color in GIANT_SKULL:
        padding = max(0, (cols - len(line_text)) // 2)
        # Gentle flicker glitch style
        if random.random() > 0.9:
            alt_color = DARK_GREEN if color == RED else RED
            print(f"{' ' * padding}{alt_color}{line_text}{RESET}")
            time.sleep(0.02)
            sys.stdout.write("\033[1A\r")
            sys.stdout.flush()
        print(f"{' ' * padding}{color}{line_text}{RESET}")
        time.sleep(0.035)

    print()
    skull_emoji_line = "☠️  ☠️  ☠️  ☠️  ☠️  ☠️  ☠️  ☠️  ☠️"
    padding = max(0, (cols - len(skull_emoji_line)) // 2)
    print(f"{' ' * padding}{RED}{skull_emoji_line}{RESET}")
    print()
    print(f"  {DARK_GREEN}{border[:cols-4]}{RESET}")
    print()

def typing(text, speed=0.02, color=""):
    """Terminal Typewriter system"""
    for c in text:
        sys.stdout.write(f"{color}{c}{RESET}")
        sys.stdout.flush()
        time.sleep(speed)
    print()

def skull_border():
    cols, _ = get_size()
    b = "☠️⋆𖤍⋆" * (cols // 6)
    return f"  {RED}{b[:cols-4]}{RESET}"

def show():
    """MAIN SEQUENCER"""
    clear()

    # PHASE 1: Big Skull Matrix Rain
    big_skull_matrix_rain(duration=3)
    clear()

    # PHASE 2: Fixed Giant Braille Skull Art
    show_giant_skull()
    time.sleep(0.5)

    # PHASE 3: Dark Progress Loading Bar
    sys.stdout.write(f"  {RED}☠️💀 {DARK_GREEN}Loading Core Engines ")
    sys.stdout.flush()
    for i in range(25):
        c = RED if i % 2 == 0 else DARK_GREEN
        sys.stdout.write(f"{c}█{RESET}")
        sys.stdout.flush()
        time.sleep(0.04)
    print(f" {RED}100% ☠️💀{RESET}")
    print()
    time.sleep(0.3)
    clear()

    # PHASE 4: ASCII Frame Output
    print(skull_border())
    print()

    banner = [
        f"{RED}  ██╗  ██╗████████╗    {DARK_GREEN}████████╗██████╗  █████╗  ██████╗██╗  ██╗",
        f"{RED}  ██║  ██║╚══██╔══╝    {DARK_GREEN}╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝",
        f"{RED}  ███████║   ██║       {DARK_GREEN}   ██║   ██████╔╝███████║██║     █████╔╝ ",
        f"{RED}  ██╔══██║   ██║       {DARK_GREEN}   ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ",
        f"{RED}  ██║  ██║   ██║       {DARK_GREEN}   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗",
        f"{RED}  ╚═╝  ╚═╝   ╚═╝       {DARK_GREEN}   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝",
    ]

    for line in banner:
        print(line)
        time.sleep(0.05)

    print()
    print(skull_border())
    print()

    # PHASE 5: Typewrite Details
    infos = [
        (f"  ☠️💀☠️  HTTrackX v6.0 | 20 Powerful Methods", RED),
        (f"  ⋆𖤍⋆  Full Clone: HTML+CSS+JS+IMG+Fonts+Media", DARK_GREEN),
        (f"  ☠️☠️☠️  Auto Link Fix + Bug Fix + Deep Crawl", RED),
        (f"  💀⋆💀  Matrix Engine | Retry | Progress Bar", DARK_GREEN),
    ]

    for text, color in infos:
        typing(text, speed=0.015, color=color)
        time.sleep(0.05)

    print()
    print(skull_border())
    print()

    # PHASE 6: Border footer check
    footer_skulls = "☠️💀☠️💀☠️💀☠️💀☠️💀☠️💀☠️💀☠️💀"
    cols, _ = get_size()
    print(f"  {RED}{footer_skulls[:cols//2]}{RESET}")
    print()
