# Ejercicio 2 – Crear el servicio de inventario

Requiere la red del [ejercicio 1](../Ejercicio%201).

```powershell
docker run -d --name inventory-service --network ecommerce-network nginx
docker ps
docker inspect inventory-service
python registrar.py inventory-service     # tabla con nombre, estado, red e IP
```
