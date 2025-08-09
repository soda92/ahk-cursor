from pathlib import Path
from multiprocessing import Process, Manager, Event
import time
from fastapi import FastAPI
import argparse

from ahk_cursor.stop import stop
from ahk_cursor.move_cursor import main as move_cursor
from ahk_cursor.gen import gen
from ahk_cursor.check_running import check_running


CURRENT = Path(__file__).resolve().parent


def check_running_loop(shared_data, stop_event, executable_name):
    while not stop_event.is_set():
        x = check_running(executable_name)
        shared_data["status"] = "stopped" if x == -1 else "running"

        if shared_data.get("shutdown", False):
            break
        time.sleep(1.2)


def server(shared_data, stop_event):
    app = FastAPI()

    @app.get("/force_run")
    def force_run():
        shared_data["force_run"] = True
        return "111"

    @app.get("/shutdown_server")
    def shutdown():
        shared_data["shutdown"] = True
        stop_event.set()
        return "222"

    import uvicorn

    uvicorn.run(app, port=12345)


def server_checker(shared_data, stop_event):
    p = Process(target=server, args=(shared_data, stop_event))
    p.start()

    while not stop_event.is_set():
        time.sleep(0.5)

    p.terminate()
    p.join()


def main():
    parser = argparse.ArgumentParser(description="AHK Cursor Manager")
    parser.add_argument(
        "--executable",
        type=str,
        default="BGI.exe",
        help="The name of the executable to monitor (default: BGI.exe)",
    )
    args = parser.parse_args()

    stop()
    gen()

    with Manager() as manager:
        shared_data = manager.dict({"status": "unknown"})
        stop_event = Event()

        # 启动 move_cursor 进程
        t2 = Process(target=move_cursor, args=(shared_data,))
        t2.start()

        # 启动 server_checker 进程
        t3 = Process(target=server_checker, args=(shared_data, stop_event))
        t3.start()

        # 启动 check_running_loop 进程
        t = Process(target=check_running_loop, args=(shared_data, stop_event, args.executable))
        t.start()

        t.join()
        t2.join()
        t3.join()


if __name__ == "__main__":
    main()
