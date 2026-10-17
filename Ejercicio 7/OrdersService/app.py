"""OrdersService: cliente de InventoryService que usa el NOMBRE lógico.

Equivalente en Python del HttpClient del enunciado:
    GET http://inventory-service:8080/api/inventory/P001

Uso:
    python app.py                 # pide P001 a INVENTORY_URL e imprime la respuesta
    python app.py --ip 172.18.0.5 # variante con IP directa, para comparar
Fuera de Docker puede apuntarse a localhost con INVENTORY_URL=http://localhost:8080/api/inventory
"""
import os
import sys
import urllib.error
import urllib.request

INVENTORY_URL = os.getenv("INVENTORY_URL", "http://inventory-service:8080/api/inventory")


def consultar(base_url, product_id="P001"):
    with urllib.request.urlopen(f"{base_url}/{product_id}", timeout=3) as resp:
        return resp.read().decode("utf-8")


if __name__ == "__main__":
    url = INVENTORY_URL
    if len(sys.argv) == 3 and sys.argv[1] == "--ip":
        url = f"http://{sys.argv[2]}:8080/api/inventory"
    print(f"Consultando {url}/P001")
    try:
        print(consultar(url))
    except (urllib.error.URLError, OSError) as e:
        sys.exit(f"Error: {e}")
