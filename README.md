# Caso práctico – Nombrado en Sistemas Distribuidos

Plataforma de e-commerce reducida a los dos servicios que intervienen en el problema de nombrado: `orders-service` necesita encontrar a `inventory-service` aunque cambie su IP.

| Carpeta | Ejercicio | Contenido |
|---|---|---|
| [`Ejercicio 1`](./Ejercicio%201) | Red Docker | Comandos |
| [`Ejercicio 2`](./Ejercicio%202) | Servicio de inventario | Comandos + `registrar.py` |
| [`Ejercicio 3`](./Ejercicio%203) | Cliente | Comandos + `probar_cliente.py` |
| [`Ejercicio 4`](./Ejercicio%204) | Cambio de dirección | Comandos + `cambio_direccion.py` |
| [`Ejercicio 5`](./Ejercicio%205) | DNS tradicional | Comandos + `dns_lookup.py` |
| [`Ejercicio 6`](./Ejercicio%206) | InventoryService | C# (ASP.NET Core) |
| [`Ejercicio 7`](./Ejercicio%207) | OrdersService | C# (ASP.NET Core) |
| [`Ejercicio 8`](./Ejercicio%208) | Dockerizar | Dockerfiles multi-stage (.NET 8) |
| [`Ejercicio 9`](./Ejercicio%209) | Docker Compose | `docker-compose.yml` + servicios en C# |
| [`Ejercicio 10`](./Ejercicio%2010) | Recrear infraestructura | Comandos + `comparar_ips.py` |
| [`Ejercicio 11`](./Ejercicio%2011) | Múltiples instancias | `docker-compose.yml` con 3 réplicas |
| [`Ejercicio 12`](./Ejercicio%2012) | Service Discovery | `registry.py` |
| [`Ejercicio 13`](./Ejercicio%2013) | Kubernetes | Manifiestos YAML |

Los ejercicios 14 y 15 (comparación y conclusión) son teóricos y están fuera de este repositorio.

**Requisitos:** Docker Desktop. Para correr los servicios fuera de Docker (ejercicios 6 y 7), el SDK de .NET 8. Los scripts auxiliares de los ejercicios 2 a 5, 10 y 12 usan Python 3. Los comandos están escritos para PowerShell.
