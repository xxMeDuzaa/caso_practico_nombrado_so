# Ejercicio 5 – DNS tradicional

```powershell
nslookup www.google.com
dig www.google.com                  # opcional
python dns_lookup.py www.google.com
docker exec orders-service nslookup inventory-service   # DNS interno de Docker, para comparar
```
