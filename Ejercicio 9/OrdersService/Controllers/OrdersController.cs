using System.Net;
using System.Net.Sockets;
using Microsoft.AspNetCore.Mvc;

namespace OrdersService.Controllers
{
    /// <summary>
    /// Cliente de InventoryService. No conoce ninguna IP: usa el nombre lógico de
    /// INVENTORY_URL (por defecto http://inventory-service:8080/api/inventory) y deja
    /// que el DNS embebido de Docker lo resuelva.
    /// </summary>
    [ApiController]
    public class OrdersController : ControllerBase
    {
        private readonly IHttpClientFactory _factory;
        private readonly string _inventoryUrl;

        public OrdersController(IHttpClientFactory factory, IConfiguration config)
        {
            _factory = factory;
            _inventoryUrl = (config["INVENTORY_URL"] ?? "http://inventory-service:8080/api/inventory").TrimEnd('/');
        }

        private string InventoryHost => new Uri(_inventoryUrl).Host;

        // GET /api/orders -> consulta inventario e indica qué instancia respondió
        [HttpGet("api/orders")]
        public async Task<IActionResult> GetOrders()
        {
            try
            {
                var inv = await ConsultarInventario();
                return Ok(new
                {
                    OrdersService = Environment.MachineName,
                    InventoryUrl = _inventoryUrl,
                    RespondioInstancia = inv.Instancia,
                    RespondioIp = inv.Ip,
                    inv.Items
                });
            }
            catch (Exception e) when (e is HttpRequestException or TaskCanceledException)
            {
                return StatusCode(502, new
                {
                    Error = "no se pudo contactar a inventory-service",
                    InventoryUrl = _inventoryUrl,
                    Detalle = e.Message
                });
            }
        }

        // GET /api/orders/{productId} -> la llamada del enunciado (ejercicio 7)
        [HttpGet("api/orders/{productId}")]
        public async Task<IActionResult> GetProducto(string productId)
        {
            var client = _factory.CreateClient("inventory");
            var response = await client.GetAsync($"{_inventoryUrl}/{productId}");
            var content = await response.Content.ReadAsStringAsync();
            Console.WriteLine(content);
            return Content(content, "application/json");
        }

        // GET /debug/resolve -> a qué IP(s) resuelve hoy el nombre del servicio
        [HttpGet("debug/resolve")]
        public async Task<IActionResult> Resolve()
        {
            return Ok(new { Nombre = InventoryHost, ResuelveA = await Resolver(InventoryHost) });
        }

        // GET /debug/balanceo?n=30 -> hace n llamadas y cuenta cuántas atendió cada instancia
        [HttpGet("debug/balanceo")]
        public async Task<IActionResult> Balanceo([FromQuery] int n = 10)
        {
            n = Math.Clamp(n, 1, 200);
            var conteo = new Dictionary<string, int>();
            var errores = new List<string>();

            for (var i = 0; i < n; i++)
            {
                try
                {
                    var inv = await ConsultarInventario();
                    var clave = $"{inv.Instancia} ({inv.Ip})";
                    conteo[clave] = conteo.GetValueOrDefault(clave) + 1;
                }
                catch (Exception e) when (e is HttpRequestException or TaskCanceledException)
                {
                    errores.Add(e.Message);
                }
            }

            return Ok(new
            {
                Llamadas = n,
                IpsResueltas = await Resolver(InventoryHost),
                AtendidasPorInstancia = conteo,
                Errores = errores.Count,
                DetalleErrores = errores.Take(5)
            });
        }

        private async Task<InventarioRespuesta> ConsultarInventario()
        {
            var client = _factory.CreateClient("inventory");
            var inv = await client.GetFromJsonAsync<InventarioRespuesta>(_inventoryUrl);
            return inv ?? throw new HttpRequestException("respuesta vacía de inventory-service");
        }

        private static async Task<object> Resolver(string host)
        {
            try
            {
                var ips = await Dns.GetHostAddressesAsync(host, AddressFamily.InterNetwork);
                return ips.Select(ip => ip.ToString()).Distinct().ToArray();
            }
            catch (SocketException e)
            {
                return new { Error = $"no se pudo resolver '{host}': {e.Message}" };
            }
        }
    }

    public record InventarioRespuesta(string? Instancia, string? Ip, List<ItemStock>? Items);

    public record ItemStock(string Sku, string Producto, int Stock);
}
