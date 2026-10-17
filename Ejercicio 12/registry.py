"""Registro de servicios mínimo: register / heartbeat / discover con expiración (TTL).

Ejecutar sin argumentos para una demostración.
"""
import random
import time


class ServiceRegistry:
    def __init__(self, ttl=3.0):
        self.ttl = ttl
        self._instancias = {}  # nombre -> {direccion: ultimo_heartbeat}

    def register(self, nombre, direccion):
        self._instancias.setdefault(nombre, {})[direccion] = time.monotonic()

    heartbeat = register  # renovar el registro es registrar de nuevo

    def deregister(self, nombre, direccion):
        self._instancias.get(nombre, {}).pop(direccion, None)

    def discover(self, nombre):
        """Devuelve las direcciones vigentes (descarta las que no enviaron heartbeat)."""
        ahora = time.monotonic()
        vivas = {d: t for d, t in self._instancias.get(nombre, {}).items()
                 if ahora - t <= self.ttl}
        self._instancias[nombre] = vivas
        return sorted(vivas)


if __name__ == "__main__":
    reg = ServiceRegistry(ttl=1.0)
    for ip in ("172.18.0.5:8080", "172.18.0.6:8080", "172.18.0.7:8080"):
        reg.register("inventory-service", ip)
    print("Instancias:", reg.discover("inventory-service"))

    print("Cliente elige:", random.choice(reg.discover("inventory-service")))

    print("... pasa el tiempo; solo 2 instancias envían heartbeat ...")
    time.sleep(0.8)
    reg.heartbeat("inventory-service", "172.18.0.5:8080")
    reg.heartbeat("inventory-service", "172.18.0.7:8080")
    time.sleep(0.4)
    print("Instancias:", reg.discover("inventory-service"), "(la .6 expiró)")

    reg.register("inventory-service", "172.18.0.9:8080")
    print("Nueva instancia:", reg.discover("inventory-service"))
    print("El cliente siempre pregunta por 'inventory-service'; nunca configura IP.")
