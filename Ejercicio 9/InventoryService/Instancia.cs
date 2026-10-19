using System.Net;
using System.Net.Sockets;

namespace InventoryService
{
    /// <summary>Datos de la instancia (contenedor) que está atendiendo.</summary>
    public static class Instancia
    {
        public static string Nombre => Environment.MachineName;

        public static string Ip
        {
            get
            {
                try
                {
                    return Dns.GetHostAddresses(Dns.GetHostName())
                        .FirstOrDefault(a => a.AddressFamily == AddressFamily.InterNetwork)?
                        .ToString() ?? "desconocida";
                }
                catch (SocketException)
                {
                    return "desconocida";
                }
            }
        }
    }
}
