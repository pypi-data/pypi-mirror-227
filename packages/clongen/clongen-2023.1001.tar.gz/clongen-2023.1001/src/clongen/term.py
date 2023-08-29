import sys
from typing import Any

from rich.console import Console


class Term:
    prefix = "[b]clongen[yellow]|[blue]|[red]|[reset]"

    def __init__(self) -> None:
        self.console = Console(file=sys.stderr)

    def echo(self, *args: Any, **kwargs: Any) -> None:
        self.console.print(self.prefix, *args, **kwargs)

    def error(self, *args: Any, kind: str = "", code: int = 1, **kwargs: Any) -> None:
        self.console.print(self.prefix, f"[red]\[{kind}Error][/red]", *args)
        sys.exit(code)


term = Term()
