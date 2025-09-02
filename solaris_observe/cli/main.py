import typer

app = typer.Typer(help="Solaris Observe CLI")

@app.command()
def schedule(file: str, site: str = "TG", driver: str = "sim"):
    """Run an observation schedule from FILE."""
    typer.echo(f"Running schedule {file} at site={site} with driver={driver}")

@app.command()
def track(target: str, duration: int = 60, site: str = "TG"):
    """Track a target for a given duration (seconds)."""
    typer.echo(f"Tracking {target} for {duration}s at site={site}")

if __name__ == "__main__":
    app()
