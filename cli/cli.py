from typing import List, Optional
from typing_extensions import Annotated
from service.service import reviews_to_csv, summarize_reviews
from cli.model import Order
import typer
from pathlib import Path
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn


app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def scrape(
    url: str,
    count: Annotated[
        int,
        typer.Option(
            "--count", "-c", min=1, max=1000, help="Number of reviews to scrape"
        ),
    ] = 100,
    sort: Annotated[
        Order,
        typer.Option(
            "--order", "-o", case_sensitive=False, help="Sorting method for the reviews"
        ),
    ] = Order.relevancy,
    destination: Annotated[
        Path,
        typer.Option(
            "--destination", "-d", dir_okay=False, help="Destination of the CSV file"
        ),
    ] = Path("reviews.csv"),
):
    """
    Scrape reviews from a product URL and save them to a CSV file.
    """
    print(
        f"[yellow]Scraping [italic][link={url}]reviews[/link][/italic][/yellow] :hourglass_not_done:"
    )
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        progress.add_task(description="Scraping...", total=None)
        reviews_to_csv(url, count, sort, destination)
    print(
        f"[green]Reviews saved to [italic]{destination}[/italic]![/green] :white_heavy_check_mark:"
    )


@app.command()
def analyze(
    source: Annotated[
        Path,
        typer.Option("--source", "-s", dir_okay=False, help="Source of the CSV file"),
    ],
    aspects: Annotated[
        Optional[List[str]],
        typer.Option("--aspect", "-a", help="List of aspects to analyze"),
    ] = None,
):
    """
    Analyze sentiment from a CSV file.
    """
    if source.suffix != ".csv":
        raise typer.BadParameter("The source file must be a CSV file.")


@app.command()
def summarize(
    source: Annotated[
        Path,
        typer.Option("--source", "-s", dir_okay=False, help="Source of the CSV file"),
    ],
):
    """
    Summarize reviews from a CSV file.
    """
    if source.suffix != ".csv":
        raise typer.BadParameter("The source file must be a CSV file.")
    print(
        f"[yellow]Summarizing the reviews from [italic]{source}[/italic][/yellow] :hourglass_not_done:"
    )
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        progress.add_task(description="Summarizing...", total=None)
        summary = summarize_reviews(source)
    print(f"[green]Summary completed![/green] :white_heavy_check_mark:")
    print(summary)


if __name__ == "__main__":
    app()
