# port-scanner

This project allows you to check if there are any open ports on your computer so you can stay vigilant.
I built this project to learn cybersecurity basics, understand how networks work, and practice Python at the same time.
I learned about ports, sockets, and how certain open ports can be very dangerous for the user.
It's a simple project, but not an easy one. Features such as reports and anomaly detection could be added in the future.

Technologies
- Python 3.x
- `socket` (standard library)
- `argparse` (standard library)

No external dependencies required.

Installation


git clone https://github.com/tuusuario/port-scanner.git
cd port-scanner


Usage

# Basic scan (ports 1-1024)
python scanner.py localhost

# Custom range
python scanner.py <0.0.0.0> -p 1-500

# Custom timeout
python scanner.py <> -p 1-1024 -t 0.5


Flags

| Flag | Description | Default |
|------|-------------|---------|
| `-p` | Port range | `1-1024` |
| `-t` | Timeout per port (seconds) | `1.0` |


## Example Output


==================================================
  Escáner de Puertos Básico
==================================================
  Host     : localhost
  IP       : 127.0.0.1
  Puertos  : 1 - 1024
  Inicio   : 2026-03-14 11:12:24
==================================================
  [+] Puerto 22     ABIERTO  (SSH)
  [+] Puerto 80     ABIERTO  (HTTP)   
  [+] Puerto 23     ABIERTO  (Telnet) 

  UERTOS PELIGROSOS DETECTADOS:
  MUY PELIGROSO: Telnet es acceso remoto sin cifrado
==================================================
  Escaneo completado: 3 puerto(s) abierto(s
==================================================

Future Improvements

- [ ] Banner grabbing to detect service versions
- [ ] Export results to JSON
- [ ] Faster scanning with threading
- [ ] Host discovery on local network


Author

JOSE MANUEL VAZQUEZ ESPINOIZA (SISU)
