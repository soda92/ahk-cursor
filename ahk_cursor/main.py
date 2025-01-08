import argparse
from ahk_cursor.stop import stop
from ahk_cursor.move_cursor import main as move_cursor
from ahk_cursor.gen import gen
import logging
import logging.handlers
from pathlib import Path
import subprocess
from multiprocessing import Process
import multiprocessing
import time
from fastapi import FastAPI


# sending checking reuslts
queue_status = multiprocessing.Queue()
# signals
queue_signals = multiprocessing.Queue()

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
            queue.put("stopped")
        else:
            queue.put("running")

        if not queue2.empty():
            sig = queue2.get()
            print(sig)
            if sig == "shutdown":
                break
        time.sleep(3)


queue4 = multiprocessing.Queue()


def server(queue_signals, queue4):
    app = FastAPI()

    @app.get("/force_run")
    def hello_world():
        queue_signals.put("force_run")
        return "111"

    @app.get("/shutdown_server")
    def shutdown():
        queue_signals.put("shutdown")
        queue4.put("shutdown")
        return "222"

    import uvicorn

    uvicorn.run(app, port=12345)


def server_checker(queue_status, queue_signals, queue4):
    p = Process(target=server, args=(queue_signals, queue4))
    p.start()

    while True:
        if queue4.empty():
            time.sleep(1)
        else:
            p.terminate()
            queue_signals.put("shutdown")
            break


def main():
    gen()
    args = parser.parse_args()

    if args.stop:
        stop()
    else:
        t2 = Process(target=move_cursor, args=[queue_status, queue_signals])
        t2.start()

        t3 = Process(target=server_checker, args=[queue_status, queue_signals, queue4])
        t3.start()

        t = Process(
            target=check_running_loop,
            args=(
                queue_status,
                queue_signals,
            ),
        )
        t.start()
        t.join()


if __name__ == "__main__":
    main()
