using Microsoft.AspNetCore.Mvc;

namespace OrdersService.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class OrdersController : ControllerBase
    {
        private readonly IHttpClientFactory _factory;

        public OrdersController(IHttpClientFactory factory) => _factory = factory;

        // GET /api/orders/{productId}
        // Consulta a InventoryService por su nombre: http://inventory-service:8080/api/inventory/{productId}
        [HttpGet("{productId}")]
        public async Task<IActionResult> Get(string productId)
        {
            var client = _factory.CreateClient("inventory");
            Console.WriteLine($"Consultando {client.BaseAddress}api/inventory/{productId}");

            var response = await client.GetAsync($"api/inventory/{productId}");
            var content = await response.Content.ReadAsStringAsync();
            Console.WriteLine(content);

            return Content(content, "application/json");
        }
    }
}
