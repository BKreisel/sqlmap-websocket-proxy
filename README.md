# sqlmap Websocket Proxy
💉Tool to enable blind sql injection attacks against websockets using sqlmap

Heavily based on an excellent writeup from Rayhan Ahmed: [Automating Blind SQL injection over WebSocket](https://rayhan0x01.github.io/ctf/2021/04/02/blind-sqli-over-websocket-automation.html)

## Example
```
sqlmap-websocket-proxy -u ws://sketchyurl.htb:8081 -p '{"uid_of_some_sort": "%param%"}' --json
python3 sqlmap.py -u  http://localhost:8080/?param1=1
```
## Usage
```bash
usage: sqlmap-websocket-proxy [-h] -u URL -p PAYLOAD [-o PORT] [--json]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to the websocket
  -p PAYLOAD, --payload PAYLOAD
                        String with params for the playload encoded as %param% (example: {"uid_of_some_sort": "%param%"})
  -o PORT, --port PORT  Proxy Port (default: 8080)
  --json                Escape text for JSON payloads
```

## Installation

### PyPI
```bash
python3 -m pip install sqlmap-websocket-proxy
```

### Manual 
```bash
python3 -m pip install sqlmap_websocket_proxy-1.0.0-py3-none-any.whl
```
[Download Latest Release](https://github.com/BKreisel/sqlmap-websocket-proxy/releases/download/1.0.0/sqlmap_websocket_proxy-1.0.0-py3-none-any.whl)

## Demo
[![demo](https://asciinema.org/a/550190.svg)](https://asciinema.org/a/550190?autoplay=1)
