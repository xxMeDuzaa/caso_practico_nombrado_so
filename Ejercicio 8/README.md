# Ejercicio 8 – Dockerizar los servicios

```powershell
docker build -f Dockerfile.inventory -t inventory-service "../Ejercicio 6/InventoryService"
docker build -f Dockerfile.orders    -t orders-service    "../Ejercicio 7/OrdersService"

docker network create ecommerce-network
docker run -d --name inventory-service --network ecommerce-network inventory-service
docker run --rm --network ecommerce-network orders-service
```
