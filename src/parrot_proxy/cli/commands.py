import json

import typer

from rich import box, print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from parrot_proxy.db.database import init_db
from parrot_proxy.db.repository import export_request_raw, get_all_requests, get_request_by_id
from parrot_proxy.services.capture_service import capture_request
from parrot_proxy.services.replay_service import replay_saved_request

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
    # Show single request

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

@app.command(name="export")
def export(request_id: int, file: str = None):
    # Export Raw Request

    raw = export_request_raw(request_id)

    if not raw:
        console.print("[red]Request not found[/red]")
        return
    
    if file:
        with open(file, "w") as f:
            f.write(raw)
        
        console.print(f"[green]Exported to {file}[/green]")
    else:
        console.print(raw)

@app.command(name="replay")
def replay(
    request_id: int,
    method: str = typer.Option(None),
    body: str = typer.Option(None),
    header: list[str] = typer.Option(None),
):
    # Replay a Stored Request

    try:
        result = replay_saved_request(
            request_id = request_id,
            override_method = method,
            override_body = body,
            override_headers = header,
        )

        if not result:
            console.print("[red]Request not found[/red]")
            return
        
        response = result["response"]

        panel = Panel.fit(
            f"[bold green]Replay Complete[/bold green]\n\n"
            f"[cyan]Status:[/cyan] {response.status_code}\n"
            f"[cyan]Response Length:[/cyan] {len(response.text)}\n"
            f"[cyan]Content-Type:[/cyan] "
            f"{response.headers.get('content-type', 'unknown')}",
            title=f"Replay #{request_id}",
            border_style="green",           
        )

        console.print(panel)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")