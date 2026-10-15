"""OrdersService: cliente de InventoryService.

No conoce ninguna IP: usa el nombre lógico definido en INVENTORY_URL
(por defecto http://inventory-service:8080/api/inventory) y deja que el
DNS embebido de Docker lo resuelva en cada petición.

Endpoints:
  GET /api/orders              -> consulta inventario y muestra qué instancia respondió
  GET /debug/resolve           -> IPs a las que resuelve hoy el nombre del servicio
  GET /debug/balanceo?n=10     -> hace n llamadas y cuenta cuántas atendió cada instancia
  GET /health
"""
import json
import os
import socket
import urllib.error
import urllib.request
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

PORT = int(os.getenv("PORT", "8080"))
INVENTORY_URL = os.getenv("INVENTORY_URL", "http://inventory-service:8080/api/inventory")
TIMEOUT = float(os.getenv("INVENTORY_TIMEOUT", "2"))
HOSTNAME = socket.gethostname()


def resolve(host):
    """Devuelve todas las IPs que el DNS asocia al nombre (sin duplicados, en orden)."""
    try:
        infos = socket.getaddrinfo(host, None, socket.AF_INET, socket.SOCK_STREAM)
        return list(dict.fromkeys(info[4][0] for info in infos))
    except socket.gaierror as e:
        return {"error": f"no se pudo resolver '{host}': {e}"}


def call_inventory():
    with urllib.request.urlopen(INVENTORY_URL, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        path = url.path.rstrip("/")
        inv_host = urlparse(INVENTORY_URL).hostname

        if path == "/api/orders":
            try:
                inv = call_inventory()
                self._send(200, {
                    "orders_service": HOSTNAME,
                    "inventory_url": INVENTORY_URL,
                    "respondio_instancia": inv.get("instancia"),
                    "respondio_ip": inv.get("ip"),
                    "items": inv.get("items"),
                })
            except (urllib.error.URLError, OSError) as e:
                self._send(502, {"error": "no se pudo contactar a inventory-service",
                                 "inventory_url": INVENTORY_URL, "detalle": str(e)})

        elif path == "/debug/resolve":
            self._send(200, {"nombre": inv_host, "resuelve_a": resolve(inv_host)})

        elif path == "/debug/balanceo":
            n = int(parse_qs(url.query).get("n", ["10"])[0])
            n = max(1, min(n, 200))
            conteo, errores = Counter(), []
            for _ in range(n):
                try:
                    inv = call_inventory()
                    conteo[f"{inv.get('instancia')} ({inv.get('ip')})"] += 1
                except (urllib.error.URLError, OSError) as e:
                    errores.append(str(e))
            self._send(200, {
                "llamadas": n,
                "ips_resueltas": resolve(inv_host),
                "atendidas_por_instancia": dict(conteo),
                "errores": len(errores),
                "detalle_errores": errores[:5],
            })

        elif path == "/health":
            self._send(200, {"status": "ok", "instancia": HOSTNAME})

        else:
            self._send(404, {"error": "ruta no encontrada", "path": self.path})

    def log_message(self, fmt, *args):
        print(f"[orders {HOSTNAME}] {self.address_string()} {fmt % args}", flush=True)


if __name__ == "__main__":
    print(f"OrdersService escuchando en :{PORT} -> {INVENTORY_URL}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
