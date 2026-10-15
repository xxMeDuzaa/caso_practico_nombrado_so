# Ejercicio 11 – Múltiples instancias

Usa el mismo código del [ejercicio 9](../Ejercicio%209). El `docker-compose.yml` de esta carpeta levanta **tres réplicas** de `inventory-service` (`deploy.replicas: 3`). `OrdersService` sigue apuntando a un único nombre: `http://inventory-service:8080/api/inventory`.

`OrdersService` queda publicado en `http://localhost:8082`. Es un puerto distinto al del ejercicio 9, así que no choca si ese sigue levantado.

## 1. Levantar las tres réplicas

Desde esta carpeta:

```powershell
docker compose up -d --build
docker compose ps                # ejercicio-11-inventory-service-1, -2 y -3
```

> Equivale a `docker compose up -d --scale inventory-service=3`.

## 2. Ver las tres direcciones detrás de un solo nombre

```powershell
docker network inspect ejercicio-11_ecommerce-network                    # 3 IPs distintas
docker compose exec orders-service getent ahostsv4 inventory-service     # el nombre devuelve las 3
curl.exe http://localhost:8082/debug/resolve
```

## 3. Ver el reparto de carga por DNS round-robin

```powershell
curl.exe "http://localhost:8082/debug/balanceo?n=30"
docker compose logs inventory-service          # cada réplica registra las peticiones que atendió
```

Docker devuelve los registros A en orden variable, así que el reparto es aproximado: no es exactamente equitativo.

## 4. Simular la falla de una instancia

```powershell
docker stop ejercicio-11-inventory-service-2
curl.exe http://localhost:8082/debug/resolve                   # ya no aparece su IP
curl.exe "http://localhost:8082/debug/balanceo?n=30"           # solo responden 1 y 3, errores = 0
```

## 5. Recuperar la instancia

```powershell
docker start ejercicio-11-inventory-service-2
curl.exe "http://localhost:8082/debug/balanceo?n=30"           # vuelven a responder las 3
```

En ningún momento se modificó ni reinició `OrdersService`.

## Limpieza

```powershell
docker compose down
```
