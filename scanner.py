
"""
scanner.py - Escáner básico de puertos
Autor: ManuelVzEs
GitHub: github.com/ManuelVzEs
"""

import socket
import argparse
from datetime import datetime


COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    631: "CUPS (Impresión)",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
}

DANGEROUS_PORTS = {
    21:   " PELIGRO: FTP transfiere datos sin cifrado, contraseñas visibles",
    23:   " MUY PELIGROSO: Telnet es acceso remoto sin cifrado, nunca debe estar abierto",
    25:   " PELIGRO: SMTP puede ser usado para enviar spam si está mal configurado",
    110:  " PELIGRO: POP3 transfiere correos sin cifrado",
    143:  " PELIGRO: IMAP transfiere correos sin cifrado",
    3306: "MUY PELIGROSO: Base de datos MySQL expuesta a la red",
    3389: " MUY PELIGROSO: RDP es uno de los puertos más atacados en internet",
    5432: " MUY PELIGROSO: Base de datos PostgreSQL expuesta a la red",
    6379: "MUY PELIGROSO: Redis sin autenticación por defecto, muy explotado",
}


def resolve_host(target: str) -> str:
    """Resuelve el hostname a dirección IP."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[!] No se pudo resolver el host: {target}")
        exit(1)


def scan_port(ip: str, port: int, timeout: float = 1.0) -> bool:
    """Intenta conectarse a un puerto. Retorna True si está abierto."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            return result == 0
    except socket.error:
        return False


def scan(target: str, start_port: int, end_port: int, timeout: float):
    """Escanea un rango de puertos en el objetivo."""
    ip = resolve_host(target)

    print("=" * 50)
    print(f"  Escáner de Puertos Básico")
    print("=" * 50)
    print(f"  Host     : {target}")
    print(f"  IP       : {ip}")
    print(f"  Puertos  : {start_port} - {end_port}")
    print(f"  Inicio   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    open_ports = []
    dangerous_found = []

    for port in range(start_port, end_port + 1):
        if scan_port(ip, port, timeout):
            service = COMMON_PORTS.get(port, "Desconocido")
            is_dangerous = port in DANGEROUS_PORTS
            flag = "🚨" if port in [23, 3306, 3389, 5432, 6379] else "⚠️ " if is_dangerous else "  "
            print(f"  [+] Puerto {port:<6} ABIERTO  ({service}) {flag if is_dangerous else ''}")
            if is_dangerous:
                dangerous_found.append(port)
            open_ports.append(port)

    print("=" * 50)
    print(f"  Escaneo completado: {len(open_ports)} puerto(s) abierto(s)")

    if dangerous_found:
        print(f"\n   PUERTOS PELIGROSOS DETECTADOS:")
        for port in dangerous_found:
            print(f"  {DANGEROUS_PORTS[port]}")

    print(f"\n  Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Escáner básico de puertos en Python",
        epilog="Ejemplo: python scanner.py 192.168.1.1 -p 1-1024"
    )
    parser.add_argument("target", help="IP o hostname objetivo")
    parser.add_argument(
        "-p", "--ports",
        default="1-1024",
        help="Rango de puertos (default: 1-1024). Ejemplo: 1-500"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=1.0,
        help="Timeout por puerto en segundos (default: 1.0)"
    )

    args = parser.parse_args()

    try:
        parts = args.ports.split("-")
        start_port = int(parts[0])
        end_port = int(parts[1]) if len(parts) > 1 else start_port
    except ValueError:
        print("[!] Formato de puertos inválido. Usa: 1-1024")
        exit(1)

    if not (1 <= start_port <= 65535) or not (1 <= end_port <= 65535):
        print("[!] Los puertos deben estar entre 1 y 65535")
        exit(1)

    scan(args.target, start_port, end_port, args.timeout)


if __name__ == "__main__":
    main()