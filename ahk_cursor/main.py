import os
import sys
import time
from multiprocessing import Process, Manager, Event
from pathlib import Path
import argparse
import win32pipe
import win32file
import pywintypes
import msvcrt

from ahk_cursor.stop import stop
from ahk_cursor.move_cursor import main as move_cursor
from ahk_cursor.gen import gen
from ahk_cursor.check_running import check_running

CURRENT = Path(__file__).resolve().parent
LOCK_FILE = CURRENT.joinpath("program.lock")
PIPE_NAME = r"\\.\pipe\ahk_cursor_pipe"


def acquire_lock():
    """Ensure only one instance of the program is running."""
    lock_file = open(LOCK_FILE, "w")
    try:
        msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        print("Another instance is already running. Exiting.")
        sys.exit(1)
    return lock_file


def create_named_pipe():
    """Create a named pipe for inter-process communication."""
    try:
        pipe = win32pipe.CreateNamedPipe(
            PIPE_NAME,
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
            1, 65536, 65536,
            0,
            None,
        )
        return pipe
    except pywintypes.error as e:
        print(f"Failed to create named pipe: {e}")
        sys.exit(1)


def listen_to_pipe(stop_event):
    """Listen to commands from the named pipe."""
    pipe = create_named_pipe()
    print("Waiting for client to connect to the pipe...")
    win32pipe.ConnectNamedPipe(pipe, None)

    while not stop_event.is_set():
        try:
            result, data = win32file.ReadFile(pipe, 64 * 1024)
            command = data.decode("utf-8").strip()
            if command == "shutdown":
                stop_event.set()
            elif command == "reload":
                print("Reloading configuration...")
        except pywintypes.error as e:
            print(f"Pipe error: {e}")
            break

    win32file.CloseHandle(pipe)


def check_running_loop(shared_data, stop_event, executable_name):
    while not stop_event.is_set():
        x = check_running(executable_name)
        shared_data["status"] = "stopped" if x == -1 else "running"

        if shared_data.get("shutdown", False):
            break
        time.sleep(1.2)


def server(shared_data, stop_event):
    from fastapi import FastAPI

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
        "-e",
        type=str,
        default="BGI.exe",
        help="The name of the executable to monitor (default: BGI.exe)",
    )
    args = parser.parse_args()

    # Acquire lock to ensure single instance
    lock_file = acquire_lock()

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
        t = Process(
            target=check_running_loop, args=(shared_data, stop_event, args.executable)
        )
        t.start()

        pipe_listener = Process(target=listen_to_pipe, args=(stop_event,))
        pipe_listener.start()

        t.join()
        t2.join()
        t3.join()
        pipe_listener.join()

    # 释放锁
    lock_file.close()
    os.remove(LOCK_FILE)


if __name__ == "__main__":
    main()
