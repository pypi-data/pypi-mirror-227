import time
from pathlib import Path

import typer
from typing_extensions import Annotated
from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

from dirx.console import ConsoleStyles, console

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command(help="Add a directory to the list of monitored directories")
def watch(
    directory: Annotated[
        Path,
        typer.Argument(
            file_okay=False,
            dir_okay=True,
            readable=True,
        ),
    ]
) -> None:
    if not directory.joinpath(".dirx").exists():
        console.print(
            f"[!] Error: no configuration file found for {directory.absolute()}",
            style=ConsoleStyles.error,
        )
        raise typer.Exit(1)
    print(f"[*] Added {directory.absolute()} to the list of monitored directories")


@app.command(help="Remove a directory to the list of monitored directories")
def unwatch(
    directory: Annotated[
        Path,
        typer.Argument(
            file_okay=False,
            dir_okay=True,
            readable=True,
        ),
    ]
) -> None:
    ...


@app.command(help="Launch a monitoring session")
def monitor() -> None:
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


@app.command(help="Manage dirx's configuration")
def config() -> None:
    ...
