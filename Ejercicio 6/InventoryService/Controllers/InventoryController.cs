using Microsoft.AspNetCore.Mvc;

namespace InventoryService.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class InventoryController : ControllerBase
    {
        // GET /api/inventory/{productId}
        [HttpGet("{productId}")]
        public IActionResult Get(string productId)
        {
            return Ok(new
            {
                ProductId = productId,
                Stock = 25,
                Server = Environment.MachineName
            });
        }
    }
}
