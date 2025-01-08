import time
import pyautogui
from pathlib import Path
import multiprocessing
import queue as q

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


def main(queue1: multiprocessing.Queue = None, queue2: multiprocessing.Queue = None):
    while True:
        if queue1 is not None and queue2 is not None:
            if not queue1.empty():
                x = queue1.get_nowait()
                queue2.put(x)
                break

        try:
            move_cursor()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
