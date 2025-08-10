import time
from pathlib import Path
import argparse
from threading import Event as ThreadEvent  # 新增：单进程模式使用线程事件

from ahk_cursor.move_cursor import move_cursor as jiggle_cursor
from ahk_cursor.gen import gen
from ahk_cursor.check_running import check_running

CURRENT = Path(__file__).resolve().parent


def run_single_process(executable_name: str):
    if executable_name == "":
        try:
            while True:
                jiggle_cursor()
                time.sleep(0.1)
        except KeyboardInterrupt:
            return
    stop_evt = ThreadEvent()
    try:
        while not stop_evt.is_set():
            running = check_running(executable_name) != -1  # 调用: ahk_cursor.check_running.check_running
            if running:
                jiggle_cursor()  # 调用: ahk_cursor.move_cursor.move_cursor（一次性抖动）
            time.sleep(0.1)  # 节流，避免过于频繁
    except KeyboardInterrupt:
        pass

def main_args(executable, s_gen=False):
    if s_gen:
        gen()

    # 无多进程模式：简单轮询 + 抖动
    run_single_process(executable)

def main():
    parser = argparse.ArgumentParser(description="AHK Cursor Manager")
    parser.add_argument(
        "--executable",
        "-e",
        type=str,
        default="",
        help="The name of the executable to monitor",
    )
    args = parser.parse_args()

    main_args(args.executable)


if __name__ == "__main__":
    main()
