# Ejercicio 10 – Recrear la infraestructura

Usa el proyecto del [ejercicio 9](../Ejercicio%209).

```powershell
cd "..\Ejercicio 9"
docker compose up -d --build
docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" ejercicio-09-inventory-service-1
docker compose down
docker compose up -d
docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" ejercicio-09-inventory-service-1
```

Automatizado: `python comparar_ips.py`.
