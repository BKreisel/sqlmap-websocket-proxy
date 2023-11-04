# sqlmap Websocket Proxy
💉Tool to enable blind sql injection attacks against websockets using sqlmap

Heavily based on an excellent writeup from Rayhan Ahmed: [Automating Blind SQL injection over WebSocket](https://rayhan0x01.github.io/ctf/2021/04/02/blind-sqli-over-websocket-automation.html)

## Example
```
sqlmap-websocket-proxy -u ws://sketcy.lol:1337 -p '{"id": "%param%"}'
python3 sqlmap.py -u  http://localhost:8080/?param1=1
```
## Usage
```bash
usage: sqlmap-websocket-proxy [-h] -u URL -d DATA [-p PORT]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to the websocket (example: ws://vuln_server:1337/ws)
  -d DATA, --data DATA  Paylod with injectable fields encoded as '%param%' (example: {"id": "%param%"})
  -p PORT, --port PORT  Proxy Port (default: 8080)
```

## Installation

### PyPI
```bash
python3 -m pip install sqlmap-websocket-proxy
```

### Manual 
```bash
python3 -m pip install sqlmap_websocket_proxy-1.1.0-py3-none-any.whl
```

### Git 
```bash
python3 -m pip install .
```

[Download Latest Release](https://github.com/BKreisel/sqlmap-websocket-proxy/releases/download/1.1.0/sqlmap_websocket_proxy-1.1.0-py3-none-any.whl)

## Demo
[![demo](https://asciinema.org/a/550190.svg)](https://asciinema.org/a/550190?autoplay=1)
