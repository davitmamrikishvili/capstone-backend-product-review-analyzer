import sys
import uvicorn
from rich import print

from cli.cli import app as cli_app
from api.api import app as api_app


def main():
    commands = [command.name for command in cli_app.registered_commands]

    info = f"Please specify [bold yellow]{', '.join(commands)}[/bold yellow] to launch the CLI or [bold yellow]api[/bold yellow] to launch the API."
    if len(sys.argv) > 1:
        if sys.argv[1] in commands:
            cli_app()
        elif sys.argv[1] == "api":
            uvicorn.run(api_app, host="127.0.0.1", port=8000)
        else:
            print(f"[bold red]Invalid argument.[/bold red] {info}")
    else:
        print(f"[bold red]Argument missing.[/bold red] {info}")


if __name__ == "__main__":
    main()
