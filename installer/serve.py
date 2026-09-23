"""Serve this installer only on this computer; Python 3, no dependencies."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser

if __name__ == "__main__":
    handler = partial(SimpleHTTPRequestHandler, directory=str(Path(__file__).resolve().parent))
    server = ThreadingHTTPServer(("127.0.0.1", 8000), handler)
    print("HA Wind Sensor: http://localhost:8000 — stop with Ctrl+C", flush=True)
    webbrowser.open("http://localhost:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
