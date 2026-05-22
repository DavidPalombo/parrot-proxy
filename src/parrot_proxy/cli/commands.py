import json

import typer

from rich import box, print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from parrot_proxy.db.database import init_db
from parrot_proxy.db.repository import export_request_raw, get_all_requests, get_replay_history, get_request_by_id
from parrot_proxy.services.analysis_service import compare_request_replays
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

@app.command(name="compare")
def compare(
    request_id: int,
    header: list[str] = typer.Option(None),
    body: str = typer.Option(None),
):
    # Compare baseline vs modified replay.

    try:
        result = compare_request_replays(
            request_id = request_id,
            modified_headers = header,
            modified_body = body,
        )

        diff = result["diff"]

        table = Table(
            title = f"Replay Comparison #{request_id}",
            box = box.ROUNDED,
        )

        table.add_column("Check", style="cyan")
        table.add_column("Result", style="green")

        table.add_row(
            "Status Changed",
            str(diff["status_changed"]),
        )

        table.add_row(
            "Original Status",
            str(diff["original_status"]),
        )

        table.add_row(
            "Modified Status",
            str(diff["modified_status"]),
        )

        table.add_row(
            "Body Length Changed",
            str(diff["body_length_changed"]),
        )

        table.add_row(
            "Original Length",
            str(diff["original_length"]),
        )

        table.add_row(
            "Modified Length",
            str(diff["modified_length"]),
        )

        table.add_row(
            "Reflection Detected",
            str(result["reflection_detected"]),
        )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")

@app.command(name="history")
def history(request_id: int):
    # Show replay history for a request

    history_items = get_replay_history(request_id)

    if not history_items:
        console.print("[yellow]No replay history found[/yellow]")
        return
    
    table = Table(
        title = f"Replay History #{request_id}",
        box = box.ROUNDED,
    )

    table.add_column("ID", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Length", style="yellow")
    table.add_column("Reflection", style="magenta")
    table.add_column("Status Diff", style="red")
    table.add_column("Body Diff", style="blue")
    table.add_column("Created", style="white")

    for item in history_items:
        table.add_row(
            str(item.id),
            str(item.status_code),
            str(item.response_length),
            str(item.reflection_detected),
            str(item.diff_status_changed),
            str(item.diff_body_changed),
            str(item.created_at),
        )

    console.print(table)