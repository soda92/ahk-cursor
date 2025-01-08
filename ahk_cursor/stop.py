from pathlib import Path
import os

CURRENT = Path(__file__).resolve().parent


def stop():
    os.startfile(CURRENT.joinpath("stop.ahk"))


if __name__ == "__main__":
    stop()
