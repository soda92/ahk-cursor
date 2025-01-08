import argparse
from ahk_cursor.stop import stop
from ahk_cursor.move_cursor import main as move_cursor
from ahk_cursor.gen import gen
import logging
import logging.handlers
from pathlib import Path
import subprocess
from multiprocessing import Process
import queue as q
import multiprocessing
import time

# send checking status
queue = multiprocessing.Queue()
# receive result
queue2 = multiprocessing.Queue()

CURRENT = Path(__file__).resolve().parent
log_file = CURRENT.parent.joinpath("soda-ahk.cursor.log")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(
    logging.handlers.RotatingFileHandler(
        log_file,
        mode="a",
        maxBytes=1024 * 1024 * 10,
        backupCount=5,
        encoding="utf8",
        delay=True,
        errors=None,
    )
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--stop", action="store_true", default=False, help="Stop the script if it's running"
)


def check_running():
    x = ""
    try:
        x = subprocess.run(
            args=["powershell", "-c", "Get-Process -Name BGI"], check=True
        )
    except Exception as e:
        logger.info(e)
        return -1
    else:
        print(x)
        return x


def check_running_loop(queue: multiprocessing.Queue, queue2: multiprocessing.Queue):
    while True:
        x = check_running()
        if x == -1:
            queue.put(1)
            if not queue2.empty():
                exit(0)
        time.sleep(1)


def main():
    gen()
    args = parser.parse_args()

    if args.stop:
        stop()
    else:
        t2 = Process(target=move_cursor, args=[queue, queue2])
        t2.start()

        t = Process(
            target=check_running_loop,
            args=(
                queue,
                queue2,
            ),
        )
        t.start()
        t.join()


if __name__ == "__main__":
    main()
