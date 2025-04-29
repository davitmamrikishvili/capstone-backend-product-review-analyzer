from typing import List, Optional
from typing_extensions import Annotated
from cli.progress import progress_bar
from service.service import (
    aspect_based_sentiment_analysis,
    general_sentiment_analysis,
    reviews_to_csv,
    summarize_reviews,
)
from utils.utils import get_analysis_stats
from cli.model import Order
import typer
from pathlib import Path
from rich import print


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
    if destination.suffix != ".csv":
        raise typer.BadParameter("`destination` must be CSV file.")
    print(
        f"[bold yellow]Scraping [italic][link={url}]reviews[/link][/italic][/bold yellow] :hourglass_not_done:"
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
        typer.Argument(dir_okay=False, exists=True, help="Source of the CSV file"),
    ],
    destination: Annotated[
        Path,
        typer.Argument(
            dir_okay=False,
            help="Destination of the CSV file for analysis results",
        ),
    ],
    aspects: Annotated[
        Optional[List[str]],
        typer.Option("--aspect", "-a", help="List of aspects to analyze"),
    ] = None,
):
    """
    Analyze sentiment from a CSV file.
    """
    if source.suffix != ".csv" or destination.suffix != ".csv":
        raise typer.BadParameter("Both `source` and `destination` must be CSV files.")

    with progress_bar("Analyzing..."):
        if aspects is None:
            print(
                "[bold yellow]No aspects provided. Performing general sentiment analysis.[/bold yellow] :hourglass_not_done:"
            )
            result = general_sentiment_analysis(source, destination)
            print(get_analysis_stats(result))
        else:
            print(
                f"[bold yellow]Analyzing sentiment for aspect(s): [italic]{', '.join(aspects)}[/italic][/bold yellow] :hourglass_not_done:"
            )
            result = aspect_based_sentiment_analysis(source, destination, aspects)
            for aspect, stats_dict in result.items():
                stats = get_analysis_stats(
                    **{
                        key: stats_dict[key]
                        for key in [
                            "positive_count",
                            "negative_count",
                            "neutral_count",
                            "most_positive_review",
                            "most_negative_review",
                        ]
                    }
                )
                print(f"Aspect {aspect}:")
                print(stats)
        print(
            f"[bold green]Analysis completed! Check out [italic]{destination}[/italic].[/bold green] :white_heavy_check_mark:\n"
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
    print(f"[dark_orange]{summary}[/dark_orange]")


@app.callback()
def cli():
    """
    CLI for scraping and analyzing reviews.
    """
    pass


if __name__ == "__main__":
    app()
