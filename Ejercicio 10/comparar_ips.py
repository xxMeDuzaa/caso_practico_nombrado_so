"""Recrea la infraestructura del ejercicio 9 y compara las IP antes y después.

Ejecutar desde cualquier carpeta: python comparar_ips.py
"""
import json
import subprocess
import time
import urllib.request
from pathlib import Path

PROYECTO = Path(__file__).resolve().parent.parent / "Ejercicio 9"
CONTENEDORES = ["ejercicio-09-inventory-service-1", "ejercicio-09-orders-service-1"]
URL = "http://localhost:8081/api/orders"


def compose(*args):
    subprocess.run(["docker", "compose", *args], cwd=PROYECTO, check=True)


def ips():
    resultado = {}
    for nombre in CONTENEDORES:
        info = json.loads(subprocess.run(["docker", "inspect", nombre],
                                         capture_output=True, text=True, check=True).stdout)[0]
        resultado[nombre] = next(iter(info["NetworkSettings"]["Networks"].values()))["IPAddress"]
    return resultado


def probar():
    for _ in range(15):  # esperar a que el servicio arranque
        try:
            with urllib.request.urlopen(URL, timeout=3) as r:
                return json.loads(r.read())["respondio_ip"]
        except OSError:
            time.sleep(1)
    return "sin respuesta"


if __name__ == "__main__":
    compose("up", "-d", "--build")
    antes = ips(); resp_antes = probar()
    compose("down")
    compose("up", "-d")
    despues = ips(); resp_despues = probar()
    for nombre in CONTENEDORES:
        cambio = "cambió" if antes[nombre] != despues[nombre] else "igual"
        print(f"{nombre}: {antes[nombre]} -> {despues[nombre]} ({cambio})")
    print(f"orders-service llegó a inventory en {resp_antes} y luego en {resp_despues}, sin tocar su código")
