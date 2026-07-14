"""CLI entry point for integrity-checker."""
import click
from rich.console import Console
from .checker import IntegrityChecker
from .formatter import Formatter
from .monitor import Monitor

console = Console()

@click.group()
@click.version_option(version="0.1.0")
def main():
    """integrity-checker — Android SafetyNet & Play Integrity checker."""
    pass

@main.command()
@click.option("--device", required=True, help="Device IP:PORT (e.g. 192.168.1.100:5555)")
@click.option("--format", "fmt", default="text", type=click.Choice(["text", "json", "csv"]))
@click.option("--output", "-o", help="Write output to file")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def check(device, fmt, output, verbose):
    """Check integrity of a single device."""
    checker = IntegrityChecker(device)
    result = checker.run_check()

    formatted = Formatter.format(result, fmt)
    console.print(formatted)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(formatted)
        console.print(f"[green]Report saved to {output}[/green]")

@main.command()
@click.option("--file", required=True, help="File with device list (one IP:PORT per line)")
@click.option("--format", "fmt", default="json", type=click.Choice(["text", "json", "csv"]))
@click.option("--output", "-o", help="Write output to file")
@click.option("--parallel", is_flag=True, help="Parallel checking")
def batch(file, fmt, output, parallel):
    """Batch check multiple devices."""
    with open(file) as f:
        devices = [line.strip() for line in f if line.strip()]

    console.print(f"[blue]Checking {len(devices)} devices...[/blue]")
    results = []
    for device in devices:
        try:
            checker = IntegrityChecker(device)
            result = checker.run_check()
            results.append(result)
        except Exception as e:
            results.append({"device": device, "error": str(e)})

    formatted = Formatter.format_batch(results, fmt)
    console.print(formatted)
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(formatted)

@main.command()
@click.option("--device", required=True, help="Device IP:PORT")
@click.option("--interval", default=300, help="Check interval in seconds")
@click.option("--alert-on-fail", is_flag=True, help="Alert when check fails")
@click.option("--webhook", help="Webhook URL for alerts")
def monitor(device, interval, alert_on_fail, webhook):
    """Continuous integrity monitoring."""
    mon = Monitor(device, interval, alert_on_fail, webhook)
    mon.run()

@main.command()
@click.option("--port", default=8080, help="Server port")
@click.option("--host", default="127.0.0.1", help="Server host")
def serve(port, host):
    """Start REST API server."""
    from .api_server import app
    console.print(f"[blue]Starting API server on {host}:{port}...[/blue]")
    app.run(host=host, port=port)

if __name__ == "__main__":
    main()
