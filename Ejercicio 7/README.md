# Ejercicio 7 – OrdersService

Cliente Python que usa el nombre `http://inventory-service:8080/api/inventory`.

Prueba local (sin Docker), con el inventario del ejercicio 6 corriendo:

```powershell
$env:INVENTORY_URL = "http://localhost:8080/api/inventory"
python OrdersService/app.py
python OrdersService/app.py --ip 172.18.0.5     # variante con IP directa
```
