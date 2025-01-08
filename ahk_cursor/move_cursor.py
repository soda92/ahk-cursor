import time
import pyautogui
from pathlib import Path

CURRENT = Path(__file__).resolve().parent


def move_cursor():
    x, y = pyautogui.position()
    for i in range(5):
        pyautogui.moveTo(x + 1, y, 0.1)
        time.sleep(0.1)
        x, y = pyautogui.position()
    for i in range(5):
        pyautogui.moveTo(x - 1, y, 0.1)
        time.sleep(0.1)
        x, y = pyautogui.position()


CURRENT.joinpath("running").write_text("a", encoding="utf8")


def main():
    stop_file = CURRENT.joinpath("stop")

    while True:
        if stop_file.exists():
            CURRENT.joinpath("running").unlink()
            stop_file.unlink()
            break
        else:
            try:
                move_cursor()
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main()
