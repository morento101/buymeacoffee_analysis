import click
import json
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from typing import Optional
from .analyzer import BuyMeACoffeeAnalyzer

console = Console()


def get_cache_dir() -> Path:
    """Get the cache directory path and create it if it doesn't exist."""
    cache_dir = Path.home() / ".bmac-cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Buy Me a Coffee Creator Stats Analyzer CLI"""
    pass


@cli.command()
@click.argument("creator_id")
@click.option("--no-cache", is_flag=True, help="Bypass cache and fetch fresh data")
@click.option("--format", "-f", type=click.Choice(["table", "json"]), default="table",
              help="Output format (table or json)")
def stats(creator_id: str, no_cache: bool, format: str):
    """Get statistics for a Buy Me a Coffee creator"""
    try:
        with console.status(f"[bold green]Analyzing stats for {creator_id}..."):
            analyzer = BuyMeACoffeeAnalyzer(creator_id, use_cache=not no_cache)
            stats = analyzer.analyze_stats()

        if format == "json":
            click.echo(json.dumps(stats, indent=2))
        else:
            _display_stats_table(stats, creator_id)

    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}")
        raise click.Abort()


@cli.command()
@click.argument("creator_id")
@click.option("--clear", is_flag=True, help="Clear cache for the specified creator")
def cache(creator_id: str, clear: bool):
    """Manage cache for a creator"""
    cache_dir = get_cache_dir()
    cache_file = cache_dir / f"{creator_id}.json"

    if clear:
        if cache_file.exists():
            cache_file.unlink()
            console.print(f"[green]Cache cleared for {creator_id}")
        else:
            console.print(f"[yellow]No cache exists for {creator_id}")
    else:
        if cache_file.exists():
            stats = {
                "size": f"{cache_file.stat().st_size / 1024:.2f} KB",
                "last_modified": datetime.fromtimestamp(cache_file.stat().st_mtime).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }
            _display_cache_info(creator_id, stats)
        else:
            console.print(f"[yellow]No cache exists for {creator_id}")


@cli.command()
def clear_all():
    """Clear all cached data"""
    cache_dir = get_cache_dir()

    if not any(cache_dir.iterdir()):
        console.print("[yellow]Cache is already empty")
        return

    with console.status("[bold red]Clearing all cached data..."):
        for cache_file in cache_dir.glob("*.json"):
            cache_file.unlink()

    console.print("[green]All cache cleared successfully")


def _display_stats_table(stats: dict, creator_id: str):
    """Display statistics in a formatted table"""
    # Summary Table
    summary_table = Table(title=f"📊 Statistics for {creator_id}", show_header=False)
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="green")

    for key, value in stats["summary"].items():
        summary_table.add_row(
            key.replace("_", " ").title(),
            str(value)
        )
    console.print(summary_table)

    # Support Patterns Table
    patterns_table = Table(title="👥 Support Patterns", show_header=False)
    patterns_table.add_column("Metric", style="cyan")
    patterns_table.add_column("Value", style="green")

    for key, value in stats["support_patterns"].items():
        patterns_table.add_row(
            key.replace("_", " ").title(),
            str(value)
        )
    console.print(patterns_table)

    # Monthly Trends Table
    trends_table = Table(title="📈 Monthly Trends", show_header=False)
    trends_table.add_column("Metric", style="cyan")
    trends_table.add_column("Value", style="green")

    trends = stats["monthly_trends"]
    trends_table.add_row(
        "Best Month",
        f"{trends['best_month']['date']} ({trends['best_month']['coffees']} coffees)"
    )
    trends_table.add_row(
        "Worst Month",
        f"{trends['worst_month']['date']} ({trends['worst_month']['coffees']} coffees)"
    )
    trends_table.add_row(
        "Average Monthly Supporters",
        f"{trends['monthly_averages']['supporters']:.1f}"
    )
    trends_table.add_row(
        "Average Monthly Coffees",
        f"{trends['monthly_averages']['coffees']:.1f}"
    )
    console.print(trends_table)


def _display_cache_info(creator_id: str, stats: dict):
    """Display cache information in a formatted table"""
    table = Table(title=f"💾 Cache Info for {creator_id}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    for key, value in stats.items():
        table.add_row(key.replace("_", " ").title(), str(value))

    console.print(table)


if __name__ == "__main__":
    cli()