"""Demuestra que el nombre se mantiene aunque cambie la IP del contenedor.

1. Crea la red y un cliente (orders-service) si no existen.
2. Levanta inventory-service y registra su IP.
3. Lo elimina, ocupa su IP con otro contenedor y lo vuelve a crear con el mismo nombre.
4. Resuelve el nombre desde el cliente y compara.
"""
import json
import subprocess

RED = "ecommerce-network"
SERVICIO = "inventory-service"
CLIENTE = "orders-service"


def docker(*args, check=True):
    return subprocess.run(["docker", *args], capture_output=True, text=True, check=check)


def ip_de(nombre):
    info = json.loads(docker("inspect", nombre).stdout)[0]
    return info["NetworkSettings"]["Networks"][RED]["IPAddress"]


def resolver_desde_cliente():
    return docker("exec", CLIENTE, "getent", "hosts", SERVICIO).stdout.strip()


def levantar_servicio():
    docker("run", "-d", "--name", SERVICIO, "--network", RED, "nginx")


if __name__ == "__main__":
    docker("network", "create", RED, check=False)
    docker("rm", "-f", CLIENTE, SERVICIO, "relleno", check=False)
    docker("run", "-d", "--name", CLIENTE, "--network", RED, "alpine", "sleep", "infinity")

    levantar_servicio()
    antes = ip_de(SERVICIO)
    print(f"ANTES   : {SERVICIO} -> {antes}")
    print(f"  cliente resuelve: {resolver_desde_cliente()}")

    docker("rm", "-f", SERVICIO)
    # Un contenedor extra toma la IP liberada para que el nuevo servicio reciba otra
    docker("run", "-d", "--name", "relleno", "--network", RED, "nginx")
    levantar_servicio()
    despues = ip_de(SERVICIO)
    print(f"DESPUES : {SERVICIO} -> {despues}")
    print(f"  cliente resuelve: {resolver_desde_cliente()}")

    print()
    print(f"¿Cambió la IP?      {'Sí' if antes != despues else 'No'}")
    print(f"¿Cambió el nombre?  No ({SERVICIO})")
    print("¿Se modificó el cliente?  No: solo volvió a resolver el nombre")

    docker("rm", "-f", "relleno", check=False)
