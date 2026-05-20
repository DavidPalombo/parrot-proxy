import typer
from rich import print

from parrot_proxy.db.database import init_db
from parrot_proxy.db.repository import get_all_requests
from parrot_proxy.services.capture_service import capture_request

app = typer.Typer()

@app.callback()
def startup():
    init_db()


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

    saved_request = capture_request(raw_request)

    print("\n[bold cyan]Parsed Request:[/bold cyan]")
    print(f"ID: {saved_request.id}")
    print(f"Method: {saved_request.method}")
    print(f"Path: {saved_request.path}")

@app.command(name="list-requests")
def list_requests():
    # List stored requests.

    requests = get_all_requests()

    print("\n[bold cyan]Stored Requests:[/bold cyan]\n")

    for request in requests:
        print(
            f"[green]#{request.id}[/green] "
            f"{request.method} "
            f"{request.path}"
        )