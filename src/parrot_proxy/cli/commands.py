import json

import typer

from rich import box, print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from parrot_proxy.db.database import init_db
from parrot_proxy.db.repository import get_all_requests, get_request_by_id
from parrot_proxy.services.capture_service import capture_request

console = Console()
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

    panel = Panel.fit(
        f"[bold green]Request Saved[/bold green]\n\n"
        f"[cyan]ID:[/cyan] {saved_request.id}\n"
        f"[cyan]Method:[/cyan] {saved_request.method}\n"
        f"[cyan]Path:[/cyan] {saved_request.path}",
        title="Parrot Proxy",
        border_style="green",
    )

    console.print(panel)

@app.command(name="list-requests")
def list_requests():
    # List stored requests.

    requests = get_all_requests()

    table = Table(title="Captured Requests", box=box.ROUNDED)

    table.add_column("ID", style="cyan", width=6)
    table.add_column("Method", style="green")
    table.add_column("Path", style="yellow")
    table.add_column("Created", style="magenta")

    for request in requests:
        table.add_row(
            str(request.id),
            request.method,
            request.path,
            str(request.created_at),
        )

        console.print(table)

@app.command(name="show")
def show_request(request_id: int):
    request = get_request_by_id(request_id)

    if not request:
        console.print("[red]Request not found[/red]")
        return
    
    headers = json.loads(request.headers)

    panel = Panel.fit(
        f"[bold cyan]{request.method} {request.path}[/bold cyan]\n\n"
        f"[yellow]Headers:[/yellow]\n{json.dumps(headers, indent=2)}\n\n"
        f"[magenta]Body:[/magenta]\n{request.body}",
        title = f"Request #{request.id}",
        border_style = "cyan",
    )

    console.print(panel)