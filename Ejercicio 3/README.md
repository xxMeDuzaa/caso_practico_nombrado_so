# Ejercicio 3 – Crear un cliente

```powershell
docker run -it --name orders-service --network ecommerce-network alpine
```

Dentro del contenedor:

```sh
apk add --no-cache bind-tools curl
ping inventory-service
nslookup inventory-service
getent hosts inventory-service
```

Sin sesión interactiva: `python probar_cliente.py`.
