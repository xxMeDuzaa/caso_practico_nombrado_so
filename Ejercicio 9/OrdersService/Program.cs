var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

builder.Services.AddHttpClient("inventory", client =>
{
    client.Timeout = TimeSpan.FromSeconds(2);
    // Una conexión nueva por pedido: cada llamada vuelve a resolver el nombre en el DNS
    // de Docker. Así se ve el reparto entre réplicas (ejercicio 11) y el cambio de IP
    // al recrear contenedores (ejercicio 10). Sin esto, HttpClient reutiliza la conexión
    // abierta y siempre le pega a la misma instancia.
    client.DefaultRequestHeaders.ConnectionClose = true;
});

var app = builder.Build();

app.MapControllers();
app.MapGet("/health", () => new { status = "ok", instancia = Environment.MachineName });

Console.WriteLine($"OrdersService iniciando -> {builder.Configuration["INVENTORY_URL"] ?? "http://inventory-service:8080/api/inventory"}");
app.Run();
