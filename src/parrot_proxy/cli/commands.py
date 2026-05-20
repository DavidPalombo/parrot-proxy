import typer
from rich import print

from parrot_proxy.services.capture_service import capture_request

app = typer.Typer()

@app.command()
def capture():
    # Capture a raw HTTP request.

    print("[bold green]Paste your raw HTTP request.[/bold green]")
    print("[bold yellow]Press CTRL+D when finished.[/bold yellow]")

    raw_request = ""

    try:
        while True:
            raw_request += input() + "\n"

    except EOFError:
        pass

    parsed = capture_request(raw_request)

    print("\n[bold cyan]Parsed Request:[/bold cyan]")
    print(parsed)