# Ejercicio 6 – InventoryService en C#

Web API en ASP.NET Core (.NET 8) con el controlador del enunciado: `GET /api/inventory/{productId}`.

Proyecto creado con:

```powershell
dotnet new webapi -n InventoryService --use-controllers -f net8.0
```

(se quitó el `WeatherForecastController` de ejemplo y se agregó `Controllers/InventoryController.cs`).

## Ejecutar

```powershell
cd InventoryService
dotnet run                                         # escucha en http://localhost:8080 (Properties/launchSettings.json)
curl.exe http://localhost:8080/api/inventory/P001
```

Respuesta:

```json
{"productId":"P001","stock":25,"server":"<nombre de la máquina>"}
```

`server` es `Environment.MachineName`: en Windows, el nombre de la PC; dentro de Docker, el id del contenedor.
