from dirx.cli.app import app
from dirx.constants import HOME_DIRECTORY


def setup() -> None:
    HOME_DIRECTORY.mkdir()


def main() -> None:
    if not HOME_DIRECTORY.exists():
        setup()
    app()


if __name__ == "__main__":
    main()
