import os
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta

# ╔══════════════════════════════════════════════════════════════╗
# ║                                                                ║
# ║        🎨  GitHub Contribution Graph Art Generator  🎨         ║
# ║                                                                ║
# ║        Paint custom pixel art on your contribution graph       ║
# ║        by back-dating commits across a chosen year.            ║
# ║                                                                ║
# ║        Developed by  ➜  Mrinal Kanth Padhi (MinalKanth)        ║
# ║        GitHub         ➜  https://github.com/MinalKanth          ║
# ║                                                                ║
# ║        ⭐ Like it? Drop a star on the repo!                     ║
# ║                                                                ║
# ╚══════════════════════════════════════════════════════════════╝

# ----------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------
PATTERN_FILE = "pattern.json"
FILE_PATH = "info.txt"

COMMITS_PER_PIXEL = 5   # intensity per "lit" pixel (higher = darker green)


# ----------------------------------------------------------------
# ANSI Colors (for a clean terminal experience)
# ----------------------------------------------------------------
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    RED = "\033[91m"
    GRAY = "\033[90m"


# ----------------------------------------------------------------
# Loading Animation (smooth spinner)
# ----------------------------------------------------------------
def loading_animation(duration=3):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0

    sys.stdout.write(f"\n{C.CYAN}{C.BOLD}  Initializing Contribution Art Engine  {C.RESET}")
    sys.stdout.flush()

    while time.time() < end_time:
        sys.stdout.write(f"{C.GREEN}{frames[i % len(frames)]}{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.08)
        sys.stdout.write("\b")
        i += 1

    print(f"{C.GREEN}{C.BOLD}✔{C.RESET}\n")


# ----------------------------------------------------------------
# Banner — Start
# ----------------------------------------------------------------
def show_start_credit():
    print(rf"""{C.GREEN}{C.BOLD}
   ____            _        _ _           _   _
  / ___|___  _ __ | |_ _ __(_) |__  _   _| |_(_) ___  _ __
 | |   / _ \| '_ \| __| '__| | '_ \| | | | __| |/ _ \| '_ \
 | |__| (_) | | | | |_| |  | | |_) | |_| | |_| | (_) | | | |
  \____\___/|_| |_|\__|_|  |_|_.__/ \__,_|\__|_|\___/|_| |_|

         _         _      ____                           _
        / \   _ __| |_   / ___| ___ _ __   ___ _ __ __ _| |_ ___  _ __
       / _ \ | '__| __| | |  _ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
      / ___ \| |  | |_  | |_| |  __/ | | |  __/ | | (_| | || (_) | |
     /_/   \_\_|   \__|  \____|\___|_| |_|\___|_|  \__,_|\__\___/|_|
{C.RESET}{C.DIM}
   ────────────────────────────────────────────────────────────────
{C.RESET}{C.CYAN}{C.BOLD}     Developed by  ➜  Mrinal Kanth Padhi  (MinalKanth){C.RESET}
{C.GRAY}     GitHub        ➜  https://github.com/MinalKanth{C.RESET}{C.DIM}
   ────────────────────────────────────────────────────────────────
{C.RESET}""")


# ----------------------------------------------------------------
# Banner — End
# ----------------------------------------------------------------
def show_end_credit():
    print(rf"""{C.MAGENTA}{C.BOLD}
   __  __ _         _                    ____                      _
  |  \/  (_)___ ___(_) ___  _ __        / ___|___  _ __ ___  _ __ | | ___| |_ ___
  | |\/| | / __/ __| |/ _ \| '_ \      | |   / _ \| '_ ` _ \| '_ \| |/ _ \ __/ _ \
  | |  | | \__ \__ \ | (_) | | | |     | |__| (_) | | | | | | |_) | |  __/ ||  __/
  |_|  |_|_|___/___/_|\___/|_| |_|      \____\___/|_| |_| |_| .__/|_|\___|\__\___|
                                                            |_|
{C.RESET}{C.GREEN}{C.BOLD}
   ✔  History has been rewritten.
   ✔  The timeline has shifted.
   ✔  Your contribution graph is now a canvas.
{C.RESET}{C.DIM}
   ────────────────────────────────────────────────────────────────
{C.RESET}{C.YELLOW}   ⭐ Enjoyed this? Star the repo and share the art!{C.RESET}
{C.GRAY}   👉 https://github.com/MinalKanth{C.RESET}
{C.CYAN}   Crafted with ❤  by Mrinal Kanth Padhi{C.RESET}{C.DIM}
   ────────────────────────────────────────────────────────────────
{C.RESET}""")


# ----------------------------------------------------------------
# Git Commit (back-dated, allows empty)
# ----------------------------------------------------------------
def git_commit(message, commit_date):
    subprocess.run(["git", "add", FILE_PATH], check=True)

    env = os.environ.copy()
    date_str = commit_date.strftime("%Y-%m-%dT12:00:00")

    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str

    subprocess.run(
        [
            "git",
            "commit",
            "--allow-empty",   # allows commit even if file content is unchanged
            "-m",
            message,
            "--date",
            date_str
        ],
        env=env,
        check=True
    )

    print(f"{C.GREEN}   ✔{C.RESET} {C.DIM}{message}{C.RESET}")


# ----------------------------------------------------------------
# Git Push
# ----------------------------------------------------------------
def git_push():
    print(f"\n{C.CYAN}{C.BOLD}   ⇡ Pushing commits to remote...{C.RESET}")
    subprocess.run(["git", "push"], check=True)
    print(f"{C.GREEN}{C.BOLD}   ✔ Push complete!{C.RESET}")


# ----------------------------------------------------------------
# Load Pattern
# ----------------------------------------------------------------
def load_pattern():
    with open(PATTERN_FILE, "r") as f:
        return json.load(f)


# ----------------------------------------------------------------
# Find first Sunday of a year (graph rows start on Sunday)
# ----------------------------------------------------------------
def first_sunday(year):
    d = datetime(year, 1, 1)
    while d.weekday() != 6:  # Sunday
        d += timedelta(days=1)
    return d


# ----------------------------------------------------------------
# Generate commits from the pattern grid
# ----------------------------------------------------------------
def make_commits_from_pattern(year):
    pattern = load_pattern()
    start_date = first_sunday(year)

    total_pixels = sum(1 for row in pattern for ch in row if ch != " ")
    print(f"{C.BLUE}{C.BOLD}   🖌  Painting {total_pixels} pixels for year {year}{C.RESET}\n")

    for row_idx, row in enumerate(pattern):
        for col_idx, char in enumerate(row):
            if char == " ":
                continue  # empty pixel

            commit_date = start_date + timedelta(
                weeks=col_idx,
                days=row_idx
            )

            for i in range(1, COMMITS_PER_PIXEL + 1):
                msg = f"{commit_date.date()} pixel commit {i}"

                with open(FILE_PATH, "w") as f:
                    f.write(msg)

                git_commit(msg, commit_date)

    git_push()


# ----------------------------------------------------------------
# Entry Point
# ----------------------------------------------------------------
if __name__ == "__main__":
    loading_animation(3)
    show_start_credit()

    try:
        year = int(input(f"{C.YELLOW}{C.BOLD}   👉 Enter the year to draw your pattern  📆 ➤  {C.RESET}"))
    except ValueError:
        print(f"{C.RED}{C.BOLD}   ✘ Invalid year. Please enter a number like 2024.{C.RESET}")
        sys.exit(1)

    make_commits_from_pattern(year)
    show_end_credit()