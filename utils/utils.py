import re
import pandas as pd


def extract_walmart_product_id(url: str) -> str:
    """
    Extracts the Walmart product ID from a given URL.

    Args:
        url (str): The URL to extract the product ID from.

    Returns:
        str: The extracted product ID.
    """
    pattern = r"((?<=^)|(?<=\/))\d{9,14}"
    match = re.search(pattern, url)
    product_id = match.group()
    return product_id


def get_analysis_stats(
    positive_count: int,
    negative_count: int,
    most_positive_review: str,
    most_negative_review: str,
    neutral_count: int = None,
) -> str:
    """
    Format the analysis result for display.

    Args:
        positive_count (int): Number of positive reviews.
        negative_count (int): Number of negative reviews.
        most_positive_review (str): The most positive review.
        most_negative_review (str): The most negative review.
        neutral_count (int, optional): Number of neutral reviews. Applicable for aspect-based sentiment analysis.

    Returns:
        str: Formatted string with the analysis results.
    """
    positive = "[bold green]positive[/bold green]"
    neutral = "[bold grey78]neutral[/bold grey78]"
    negative = "[bold red]negative[/bold red]"

    neutral_stat = (
        f"[bold blue]# of {neutral} reviews:[/bold blue] [bold grey78]{neutral_count}[/bold grey78]\n"
        if neutral_count is not None
        else ""
    )
    positve_review_stat = (
        f"[bold blue]Most {positive} review:[/bold blue] [dark_orange]{most_positive_review}[/dark_orange]\n"
        if not pd.isna(most_positive_review)
        else ""
    )
    negative_review_stat = (
        f"[bold blue]Most {negative} review:[/bold blue] [dark_orange]{most_negative_review}[/dark_orange]"
        if not pd.isna(most_negative_review)
        else ""
    )

    stats = (
        f"[bold blue]# of {positive} reviews:[/bold blue] [bold green]{positive_count}[/bold green]\n"
        f"{neutral_stat}"
        f"[bold blue]# of {negative} reviews:[/bold blue] [bold red]{negative_count}[/bold red]\n"
        f"{positve_review_stat}{negative_review_stat}"
    )

    return stats
