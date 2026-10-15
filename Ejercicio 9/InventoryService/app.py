"""InventoryService: servicio mínimo de inventario.

Responde en /api/inventory e incluye en cada respuesta el hostname e IP
de la instancia que atendió, para poder observar la resolución de nombres
y el reparto de carga entre réplicas (ejercicio 11).
"""
import json
import os
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.getenv("PORT", "8080"))
HOSTNAME = socket.gethostname()

STOCK = [
    {"sku": "TEC-001", "producto": "Teclado mecánico", "stock": 25},
    {"sku": "MOU-002", "producto": "Mouse inalámbrico", "stock": 40},
    {"sku": "MON-003", "producto": "Monitor 24\"", "stock": 8},
]


def own_ip():
    try:
        return socket.gethostbyname(HOSTNAME)
    except OSError:
        return "desconocida"


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/")
        if path == "/api/inventory":
            self._send(200, {"instancia": HOSTNAME, "ip": own_ip(), "items": STOCK})
        elif path == "/health":
            self._send(200, {"status": "ok", "instancia": HOSTNAME})
        else:
            self._send(404, {"error": "ruta no encontrada", "path": self.path})

    def log_message(self, fmt, *args):
        print(f"[inventory {HOSTNAME} {own_ip()}] {self.address_string()} {fmt % args}", flush=True)


if __name__ == "__main__":
    print(f"InventoryService escuchando en :{PORT} (host={HOSTNAME}, ip={own_ip()})", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
