using InventoryService;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

var app = builder.Build();

// Registra cada petición con la instancia que la atendió (se ve con "docker compose logs")
app.Use(async (context, next) =>
{
    await next();
    Console.WriteLine($"[inventory {Instancia.Nombre} {Instancia.Ip}] {context.Connection.RemoteIpAddress} " +
                      $"{context.Request.Method} {context.Request.Path} {context.Response.StatusCode}");
});

app.MapControllers();
app.MapGet("/health", () => new { status = "ok", instancia = Instancia.Nombre });

Console.WriteLine($"InventoryService iniciando (host={Instancia.Nombre}, ip={Instancia.Ip})");
app.Run();
