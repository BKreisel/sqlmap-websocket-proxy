"""HTTP Payload Handler."""
import contextlib
import json
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler
from json import JSONDecodeError
from socketserver import TCPServer
from typing import Any, Self
from urllib.parse import parse_qsl, unquote

import rich
import websocket

from sqlmap_websocket_proxy.console import error, status, timestamp

# Don't proxy these headers
SKIPPED_HEADERS = [
    "connection",
    "accept-encoding",
    "accept",
]

class HTTPHandler(SimpleHTTPRequestHandler):
    """HTTP Endpoint that Proxies to the  weboscket."""

    def __init__(
        self: Self,
        url: str,
        data: str,
        *args: Any,  # noqa: ANN401
        **kwargs: dict[Any],
    ) -> None:
        """Init."""
        self.url = url
        self.data = data

        self.json_encode = False
        with contextlib.suppress(JSONDecodeError):
            json.loads(data)
            self.json_encode = True
            status("Detected JSON input. Auto-escaping.")

        # Suppress default logging
        self.log_message = lambda *_args: None

        super().__init__(*args, **kwargs)

    def do_GET(self: Self) -> None:  # noqa: N802
        """Handle GET requests."""
        self.send_response(200)
        self.end_headers()
        resp = send_inject(
            self.url,
            self.path,
            self.data,
            self.headers,
            self.json_encode,
        )
        self.wfile.write(resp)

def send_inject(
    url: str,
    path: str,
    data: str,
    headers: dict,
    json_encode: bool,  # noqa: FBT001
) -> bytes:
    """Send sqlmap inject acrossthe websocket."""
    params = [x for _, x in parse_qsl(path)]

    if json_encode:
        params = [unquote(x).replace('"',"'") for x in params]

    for x in params:
        data = data.replace("%param%", x, 1)

    try:
        ws = websocket.create_connection(
            url,
            header=[
                f"{k}: {v}"
                for k, v in headers.items()
                if k.lower() not in SKIPPED_HEADERS
            ],
        )
    except Exception as e:  # noqa: BLE001
        error(f"Websocket Connection Failed: {e}")

    try:
        ws.send(data)
        rich.print(f"[{timestamp()}] Proxied: {data}")
        data = ws.recv()
        return data.encode("utf-8") if data else b""
    except Exception as err:  # noqa: BLE001
        rich.print(f"[yellow]Request Failed: {err!s}[/yellow]")
    finally:
        ws.close()


def run_server(port: int, url: str, data: str) -> None:
    """Run the Proxy Server."""
    try:
        handler = partial(HTTPHandler, url, data)
        with TCPServer(("", port), handler) as httpd:
            status("Server Started (Ctrl+c to stop)\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        status("Quitting...")
        sys.exit(0)
    except Exception as err:  # noqa: BLE001
        error(f"Exception: {err}")
