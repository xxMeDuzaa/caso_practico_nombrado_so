"""InventoryService (equivalente en Python del Web API en C# del enunciado).

GET /api/inventory/{productId} -> {"ProductId": ..., "Stock": 25, "Server": <hostname>}
Solo biblioteca estándar.
"""
import json
import os
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.getenv("PORT", "8080"))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        partes = self.path.split("?")[0].strip("/").split("/")
        if len(partes) == 3 and partes[:2] == ["api", "inventory"]:
            code = 200
            payload = {"ProductId": partes[2], "Stock": 25, "Server": socket.gethostname()}
        else:
            code, payload = 404, {"error": "ruta no encontrada", "path": self.path}
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[inventory {socket.gethostname()}] {self.address_string()} {fmt % args}", flush=True)


if __name__ == "__main__":
    print(f"InventoryService escuchando en :{PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
