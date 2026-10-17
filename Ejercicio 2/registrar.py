"""Registra nombre, IP, red y estado de un contenedor usando `docker inspect`.

Uso: python registrar.py [nombre-del-contenedor]
"""
import json
import subprocess
import sys


def inspeccionar(nombre):
    salida = subprocess.run(
        ["docker", "inspect", nombre], capture_output=True, text=True, check=True
    ).stdout
    return json.loads(salida)[0]


def resumen(info):
    redes = info["NetworkSettings"]["Networks"]
    return {
        "Nombre": info["Name"].lstrip("/"),
        "Estado": info["State"]["Status"],
        "Redes": {red: datos["IPAddress"] for red, datos in redes.items()},
    }


if __name__ == "__main__":
    nombre = sys.argv[1] if len(sys.argv) > 1 else "inventory-service"
    try:
        datos = resumen(inspeccionar(nombre))
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        sys.exit(f"No se pudo inspeccionar '{nombre}': {e}")
    print(f"Nombre : {datos['Nombre']}")
    print(f"Estado : {datos['Estado']}")
    for red, ip in datos["Redes"].items():
        print(f"Red    : {red}  ->  IP {ip}")
