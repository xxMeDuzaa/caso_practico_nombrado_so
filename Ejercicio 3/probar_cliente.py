"""Ejecuta los comandos del ejercicio 3 dentro de un contenedor alpine temporal
conectado a ecommerce-network, sin sesión interactiva.

Requiere que inventory-service ya esté corriendo (ejercicio 2).
"""
import subprocess

RED = "ecommerce-network"
COMANDOS = (
    "apk add --no-cache bind-tools curl >/dev/null && "
    "echo '--- /etc/resolv.conf' && cat /etc/resolv.conf && "
    "echo '--- ping' && ping -c 3 inventory-service && "
    "echo '--- nslookup' && nslookup inventory-service && "
    "echo '--- getent' && getent hosts inventory-service"
)

if __name__ == "__main__":
    subprocess.run(
        ["docker", "run", "--rm", "--network", RED, "alpine", "sh", "-c", COMANDOS]
    )
