var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

// Cliente HTTP hacia InventoryService: se configura con el NOMBRE lógico, nunca con una IP.
// En Docker se usa el valor por defecto; fuera de Docker se puede pisar con la
// configuración "InventoryUrl" (appsettings.Development.json o variable de entorno).
builder.Services.AddHttpClient("inventory", client =>
{
    client.BaseAddress = new Uri(builder.Configuration["InventoryUrl"] ?? "http://inventory-service:8080/");
    client.Timeout = TimeSpan.FromSeconds(5);
});

var app = builder.Build();

app.MapControllers();

app.Run();
