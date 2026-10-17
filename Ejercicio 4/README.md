# Ejercicio 4 – Cambio de dirección

```powershell
docker stop inventory-service
docker rm inventory-service
docker run -d --name inventory-service --network ecommerce-network nginx
docker inspect inventory-service
docker exec orders-service nslookup inventory-service
```

Automatizado (compara IP antes/después): `python cambio_direccion.py`.
