using Microsoft.AspNetCore.Mvc;

namespace InventoryService.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class InventoryController : ControllerBase
    {
        private static readonly object[] Items =
        {
            new { Sku = "P001", Producto = "Teclado mecánico", Stock = 25 },
            new { Sku = "P002", Producto = "Mouse inalámbrico", Stock = 40 },
            new { Sku = "P003", Producto = "Monitor 24\"", Stock = 8 },
        };

        // GET /api/inventory -> todo el stock + qué instancia respondió (hostname e IP)
        [HttpGet]
        public IActionResult GetAll()
        {
            return Ok(new { Instancia = Instancia.Nombre, Ip = Instancia.Ip, Items });
        }

        // GET /api/inventory/{productId} -> el endpoint del enunciado (ejercicio 6)
        [HttpGet("{productId}")]
        public IActionResult Get(string productId)
        {
            return Ok(new
            {
                ProductId = productId,
                Stock = 25,
                Server = Environment.MachineName,
                Ip = Instancia.Ip
            });
        }
    }
}
