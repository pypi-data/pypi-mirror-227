import csv
from pathlib import Path
from typing import List, Tuple

from .sequences import Lineage
from .term import term


def read_lineages(file: Path, prefix: str) -> List[Lineage]:
    lineages = []
    with file.open("r") as f:
        first_line = next(f)
        if "," in first_line:
            fields = first_line.strip().split(",")
            if not set(fields) == {"id", "lineage"}:
                term.error(
                    'two columns csv\'s must have headers for "id" and "lineages"',
                    kind="Input",
                )
            reader = csv.DictReader(f, delimiter=",", fieldnames=fields)
            for row in reader:
                lineages.append(Lineage(**row))
        else:
            if not first_line == "lineage":
                f.seek(0)
            for lineage in f:
                lineages.append(
                    Lineage(id=f"{prefix}{lineage.strip()}", lineage=lineage.strip())
                )

    return lineages


def check_paths(lineages_path: Path, output: Path) -> Tuple[Path, Path]:
    if not lineages_path.is_file():
        term.error(f"failed to find {lineages_path}...exiting", kind="Input")
    output.mkdir(exist_ok=True, parents=True)
    gtf_file, fa_file = (output / f"clonmapper.{ext}" for ext in ("gtf", "fa"))
    if gtf_file.is_file():
        term.error(f"gtf file already exists: {gtf_file}...exiting.", kind="Ouput")
    if fa_file.is_file():
        term.error(f"fasta file already exists: {fa_file}...exiting.", kind="Output")
    return (gtf_file, fa_file)


def generate(lineages_path: Path, prefix: str, output: Path) -> None:
    gtf_file, fa_file = check_paths(lineages_path, output)

    term.echo(f"reading lineages from [yellow]{lineages_path}")
    lineages = read_lineages(lineages_path, prefix)
    term.echo(f"generating fasta/gtf for {len(lineages)} lineages")

    with fa_file.open("w") as f:
        for lineage in lineages:
            f.write(lineage.fasta())

    with gtf_file.open("w") as f:
        for lineage in lineages:
            f.write(lineage.gtf())

    term.echo(f"generation complete see [bold]{output}")
