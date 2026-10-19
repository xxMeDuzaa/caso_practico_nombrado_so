# Ejercicio 8 – Dockerizar los servicios

Dockerfiles *multi-stage*: la etapa `build` compila con el SDK de .NET 8 y la imagen final solo lleva el runtime de ASP.NET y lo publicado. Las imágenes `aspnet:8.0` escuchan en el puerto **8080**, por eso la URL del caso es `http://inventory-service:8080`.

- `Dockerfile.inventory` → InventoryService del [ejercicio 6](../Ejercicio%206) (el del enunciado).
- `Dockerfile.orders` → equivalente para OrdersService del [ejercicio 7](../Ejercicio%207); solo cambia la DLL del `ENTRYPOINT`.

El contexto de cada build es la carpeta del proyecto, que tiene un `.dockerignore` con `bin/` y `obj/`.

```powershell
docker build -f Dockerfile.inventory -t inventory-service "../Ejercicio 6/InventoryService"
docker build -f Dockerfile.orders    -t orders-service    "../Ejercicio 7/OrdersService"

docker rm -f inventory-service orders-service       # por si quedaron los de los ejercicios 2 a 4
docker network create ecommerce-network             # si no existe (ejercicio 1)

docker run -d --name inventory-service --network ecommerce-network inventory-service
docker run -d --name orders-service    --network ecommerce-network -p 8081:8080 orders-service

curl.exe http://localhost:8081/api/orders/P001
docker logs orders-service                          # muestra la URL consultada, con el nombre
```

El `-p 8081:8080` solo hace falta para probar desde Windows; entre contenedores no se publican puertos.

## Limpieza

```powershell
docker rm -f inventory-service orders-service
```
