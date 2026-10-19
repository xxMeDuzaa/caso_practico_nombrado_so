# Ejercicio 7 – OrdersService en C#

Web API en ASP.NET Core (.NET 8). `GET /api/orders/{productId}` consulta a InventoryService usando el **nombre lógico**:

```
http://inventory-service:8080/api/inventory/{productId}
```

La URL base no está escrita en el controlador: se registra un `HttpClient` con nombre en `Program.cs` (vía `IHttpClientFactory`) y se toma de la configuración `InventoryUrl`, con `http://inventory-service:8080/` por defecto.

## Prueba local (sin Docker)

Con el InventoryService del [ejercicio 6](../Ejercicio%206) corriendo en el puerto 8080:

```powershell
cd OrdersService
dotnet run                                       # escucha en http://localhost:8081
curl.exe http://localhost:8081/api/orders/P001
```

Fuera de Docker el nombre `inventory-service` no existe (Windows no lo puede resolver), por eso `appsettings.Development.json` apunta a `http://localhost:8080/`. Dentro de Docker se usa el valor por defecto, con el nombre.

## Comparar con una IP directa

```powershell
$env:InventoryUrl = "http://172.18.0.5:8080/"     # IP fija
dotnet run
curl.exe http://localhost:8081/api/orders/P001     # falla: esa IP no existe o ya cambió
Remove-Item Env:InventoryUrl
```

Con el nombre, el cliente funciona aunque el contenedor de inventario se recree con otra IP; con la IP, la referencia queda obsoleta.
