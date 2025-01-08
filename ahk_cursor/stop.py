from pathlib import Path

CURRENT = Path(__file__).resolve().parent


def main():
    file = CURRENT.joinpath("stop")
    file.write_text("aa", encoding="utf8")


if __name__ == "__main__":
    main()
