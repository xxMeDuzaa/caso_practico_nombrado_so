# Ejercicio 1 – Crear una red Docker

```powershell
docker network create ecommerce-network
docker network ls
docker network inspect ecommerce-network
```

Qué hay que observar en el `inspect`:
- `"Driver": "bridge"`
- `IPAM.Config` → `Subnet` y `Gateway`
- `"Containers": {}`: la red está vacía.

## Opcional: conectar un contenedor

Sirve para ver cómo se llena la sección `Containers`:

```powershell
docker run -d --name prueba --network ecommerce-network nginx:alpine
docker network inspect ecommerce-network      # ahora aparece "prueba" con su IP
docker rm -f prueba
```

## Limpieza

```powershell
docker network rm ecommerce-network
```

> Esta red es independiente de las que crean los ejercicios 9 y 11. Compose crea su propia red, con el nombre del proyecto como prefijo (`ejercicio-09_ecommerce-network`).
