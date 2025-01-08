import pyautogui
import time


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


while True:
    move_cursor()
