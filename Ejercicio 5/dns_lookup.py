"""Resuelve un nombre de dominio y muestra sus direcciones (equivalente a nslookup)."""
import socket
import sys


def resolver(nombre):
    infos = socket.getaddrinfo(nombre, None, proto=socket.IPPROTO_TCP)
    ipv4, ipv6 = [], []
    for familia, _, _, canonico, sockaddr in infos:
        destino = ipv4 if familia == socket.AF_INET else ipv6
        if sockaddr[0] not in destino:
            destino.append(sockaddr[0])
    return ipv4, ipv6


if __name__ == "__main__":
    nombre = sys.argv[1] if len(sys.argv) > 1 else "www.google.com"
    try:
        ipv4, ipv6 = resolver(nombre)
    except socket.gaierror as e:
        sys.exit(f"No se pudo resolver '{nombre}': {e}")
    print(f"Nombre: {nombre}")
    print(f"Direcciones IPv4: {', '.join(ipv4) or '-'}")
    print(f"Direcciones IPv6: {', '.join(ipv6) or '-'}")
