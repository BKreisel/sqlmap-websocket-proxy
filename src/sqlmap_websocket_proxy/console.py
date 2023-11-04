"""Console output functions."""
import sys
from datetime import datetime

import rich


def error(msg: str, depth: int = 0) -> None:
    """Print an error message."""
    print("")
    _rich_print("red", "⛔", msg, depth=depth)
    sys.exit(1)

def status(msg: str, depth: int = 0, symbol: str = "[*]") -> None:
    """Print a status message."""
    _rich_print("blue", symbol, msg, depth=depth)

def success(msg: str, depth: int = 0) -> None:
    """Print a success message."""
    _rich_print("green", "[+]", msg, depth=depth)

def warning(msg: str, depth: int = 0) -> None:
    """Print a success message."""
    _rich_print("yellow", "[!]", msg, depth=depth)

def _rich_print(color: str, symbol: str, msg: str, depth: int = 0) -> None:
    """Format and print messages with rich."""
    rich.print(f"{depth * '   '}[{color}]{symbol}[/{color}] {msg}")

def timestamp() -> str:
    """Get the current timestamp."""
    return datetime.now().strftime("%H:%M:%S")
