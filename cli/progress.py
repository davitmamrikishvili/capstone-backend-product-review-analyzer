from contextlib import contextmanager
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn


@contextmanager
def progress_bar(description: str):
    """
    Context manager for displaying a progress bar with spinner and elapsed time.

    Args:
        description: The description to show in the progress bar
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        progress.add_task(description=description, total=None)
        yield progress
