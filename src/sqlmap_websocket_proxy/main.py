"""sqlmap websocket proxy main."""
import re
from argparse import ArgumentParser, Namespace
from typing import cast

from sqlmap_websocket_proxy.console import error, status, success, warning
from sqlmap_websocket_proxy.handler import run_server


class Args(Namespace):
    """Add type hints for CLI args."""

    url: str
    port: int
    data: str


def parse_args() -> Args:
    """Read and parse CLI args."""
    parser = ArgumentParser()
    parser.add_argument(
        "-u",
        "--url",
        required=True,
        help="URL to the websocket (example: ws://vuln_server:1337/ws)",
    )
    parser.add_argument(
        "-d",
        "--data",
        required=True,
        help=
            "Paylod with injectable fields encoded as '%%param%%'"
            ' (example: {"id": "%%param%%"})',
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8080,
        help="Proxy Port (default: 8080)",
    )
    args = parser.parse_args()

    if not args.url.startswith("ws"):
        warning("Input URL doesn't appear to be a websocket.")

    return cast(Args, args)

def main() -> None:
    """CLI main."""
    args = parse_args()
    status("Sqlmap Websocket Proxy", symbol="💉")

    status(f"{'Proxy Port':10} : {args.port}", depth=1, symbol="-")
    status(f"{'URL':10} : {args.url}", depth=1, symbol="-")
    status(f"{'Payload':10} : {args.data}", depth=1, symbol="-")

    params = [match.start() for match in re.finditer(r"%param%", args.data)]
    if not len(params):
        error("No Injectable Parameters Found :(")

    status(f"Targeting {len(params)} injectable parameter(s)")
    param_str = "&".join([f"param{x}=1" for x in range(1,len(params)+1)])
    success(f"sqlmap url flag: -u http://localhost:{args.port}/?{param_str}")

    run_server(args.port, args.url, args.data)

if __name__ == "__main__":
    main()
