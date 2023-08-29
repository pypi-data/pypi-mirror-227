from pathlib import Path

import rich_click as click

from ._version import __version__
from .core import generate


@click.command()
@click.option(
    "-l",
    "--lineages",
    "lineages_path",
    required=True,
    type=Path,
    help="csv file of lineages",
)
@click.option(
    "-p",
    "--prefix",
    show_default=True,
    help="optional default prefix",
    default="lin-",
)
@click.option(
    "-o",
    "--output",
    type=Path,
    show_default=True,
    help="directory to write fasta/gtf files",
    default="references",
)
@click.version_option(__version__)
def cli(lineages_path: Path, prefix: str, output: Path) -> None:
    """ClonMapper reference genome generator for use with cellranger mkref"""

    generate(lineages_path, prefix, output)
