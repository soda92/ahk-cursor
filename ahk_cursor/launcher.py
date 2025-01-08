from gen import gen, script, CURRENT
import os
from autostart import create


def launcher():
    gen()
    # os.startfile(CURRENT.joinpath("stop.ahk"))
    create(script)
    os.startfile(str(script))


if __name__ == "__main__":
    launcher()
