import argparse
from ahk_cursor.stop import main as stop
from ahk_cursor.move_cursor import main as move_cursor
import logging
from pathlib import Path
import subprocess

CURRENT = Path(__file__).resolve().parent
log_file = CURRENT.parent.joinpath("soda-ahk.cursor.log")
logging.basicConfig(filename=str(log_file))
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--stop", action="store_true", default=False, help="Stop the script if it's running"
)


def check_running():
    x = subprocess.run(args=["powershell", "-c", "Get-Process -Name BGI"], check=True)


def main():
    args = parser.parse_args()

    if args.stop:
        stop()
    else:
        move_cursor()
