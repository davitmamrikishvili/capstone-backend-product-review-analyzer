from typing import List, Optional
from service.service import reviews_to_csv
from cli.model import Order
import typer
from pathlib import Path
from rich import print
from typing_extensions import Annotated

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
    print(f"Scraping reviews from {url}...")
    reviews_to_csv(url, count, sort, destination)
    print(f"Reviews saved to {destination}")


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
    typer.echo(f"Analyzing sentiment from CSV file: {source}...")


if __name__ == "__main__":
    app()
