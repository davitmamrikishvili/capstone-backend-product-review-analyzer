from typing import List, Optional
from typing_extensions import Annotated
from cli.progress import progress_bar
from service.service import reviews_to_csv, summarize_reviews
from cli.model import Order
import typer
from pathlib import Path
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn


app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command("scrape")
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
    with progress_bar("Scraping..."):
        reviews_to_csv(url, count, sort, destination)
    print(
        f"[bold green]Reviews saved to [italic]{destination}[/italic]![/bold green] :white_heavy_check_mark:"
    )


@app.command("analyze")
def analyze(
    source: Annotated[
        Path,
        typer.Argument(dir_okay=False, help="Source of the CSV file"),
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
    if aspects is None:
        print(
            "[yellow]No aspects provided. Performing general sentiment analysis.[/yellow]"
        )
    else:
        print(
            f"[yellow]Analyzing sentiment for aspects: [italic]{', '.join(aspects)}[/italic][/yellow]"
        )


@app.command("summarize")
def summarize(
    source: Annotated[
        Path,
        typer.Argument(dir_okay=False, help="Source of the CSV file"),
    ],
):
    """
    Summarize reviews from a CSV file.
    """
    if source.suffix != ".csv":
        raise typer.BadParameter("The source file must be a CSV file.")
    print(
        f"[bold yellow]Summarizing the reviews from [italic]{source}[/italic][/bold yellow] :hourglass_not_done:"
    )
    with progress_bar("Summarizing..."):
        summary = summarize_reviews(source)
    print(f"[bold green]Summary completed![/bold green] :white_heavy_check_mark:")
    print(summary)


@app.callback()
def cli():
    """
    CLI for scraping and analyzing reviews.
    """
    pass


if __name__ == "__main__":
    app()
