# Ejercicio 9 – Docker Compose

| Servicio | Qué hace |
|---|---|
| `InventoryService` | Responde `GET /api/inventory`. Cada respuesta incluye el **hostname e IP de la instancia** que atendió. |
| `OrdersService` | Llama a `http://inventory-service:8080/api/inventory` (nombre lógico, **ninguna IP en el código**). |

Ambos están hechos en Python con solo la biblioteca estándar, así que no hay dependencias que instalar.

Endpoints de `OrdersService`, publicados en el host como `http://localhost:8081`:

| Endpoint | Para qué sirve |
|---|---|
| `/api/orders` | Consulta inventario e indica qué instancia respondió |
| `/debug/resolve` | Muestra a qué IP(s) resuelve hoy el nombre `inventory-service` |
| `/debug/balanceo?n=30` | Hace *n* llamadas y cuenta cuántas atendió cada instancia |

> Se usa `curl.exe` y no `curl` porque en Windows PowerShell `curl` es un alias de `Invoke-WebRequest`.

## Ejecutar

Desde esta carpeta:

```powershell
docker compose up --build        # deja los logs en primer plano; Ctrl+C para cortar
# o en segundo plano:
docker compose up -d --build

docker compose ps
```

## Nombres

```powershell
docker compose ps                # columna NAME (ejercicio-09-inventory-service-1) y SERVICE (inventory-service)
docker network ls                # ejercicio-09_ecommerce-network
```

## Direcciones

```powershell
docker network inspect ejercicio-09_ecommerce-network
docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" ejercicio-09-inventory-service-1
docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" ejercicio-09-orders-service-1
```

## Resolución

```powershell
# Desde dentro de orders-service, con el DNS embebido de Docker
docker compose exec orders-service getent hosts inventory-service
docker compose exec orders-service cat /etc/resolv.conf      # nameserver 127.0.0.11

# La llamada real, que usa el nombre y no la IP
curl.exe http://localhost:8081/api/orders
curl.exe http://localhost:8081/debug/resolve
```

Para comparar: el nombre **no** resuelve fuera de la red del proyecto.

```powershell
docker run --rm busybox nslookup inventory-service                                          # falla (red bridge por defecto)
docker run --rm --network ejercicio-09_ecommerce-network busybox nslookup inventory-service  # resuelve
```

## Limpieza

```powershell
docker compose down
```
