Lab mac-flooding-lab

Eunice Y. Francisca Fleming 2024-1185

Enlace de video: (https://youtu.be/ejYp6q1sgTk?si=j4a7qyuvuRRH6d4M)

Enlace de Playlist: https://www.youtube.com/playlist?list=PLedgCpC2B7oUOUOG7D6VLYsRR7i7bySIM

**Matrícula:** 2024-1185

---

## Descripción

Script Python que realiza un ataque **MAC Flooding**, enviando masivamente frames Ethernet con MACs origen aleatorias para saturar la tabla CAM del switch. Al llenarse, el switch hace broadcast de todo el tráfico permitiendo al atacante ver comunicaciones ajenas.

---

## Requisitos

| Requisito | Detalle |
|-----------|---------|
| Sistema Operativo | Linux (probado en Linux2024 / Debian) |
| Python | 3.x |
| Librería | Scapy (`pip3 install scapy`) |
| Privilegios | root (sudo) |
| Simulador | GNS3 con IOU Cisco |

---

## Instalación

```bash
pip3 install scapy
```

---

## Uso

```bash
sudo python3 mac_flooding.py [opciones]
```

### Parámetros

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `-i` / `--iface` | Interfaz de red | `-i eth0` |
| `-c` / `--count` | Número de frames (0=infinito) | `-c 5000` |
| `-d` / `--delay` | Delay entre frames (seg) | `-d 0.0` |
| `-v` / `--verbose` | Mostrar cada frame | `--verbose` |

### Ejemplo

```bash
sudo python3 mac_flooding.py -i eth0 -c 5000 -v
```

---

## Topología

```
```
<img width="668" height="603" alt="image" src="https://github.com/user-attachments/assets/2b9b70eb-3da5-46d8-b2b0-82f27bcb7325" />


### Tabla de Direccionamiento

| Dispositivo | IP | Máscara | Rol |
|-------------|-----|---------|-----|
| IOU1 | 10.11.85.1 | /24 | Gateway |
| PC1 (VPCS) | 10.11.85.10 | /24 | Víctima 1 |
| PC2 (VPCS) | 10.11.85.20 | /24 | Víctima 2 |
| PC3 (VPCS) | 10.11.85.40 | /24 | Víctima 3 |
| Linux2024 | 10.11.85.30 | /24 | Atacante |

---

## Verificación

```bash
# En IOU2 — tabla CAM llena
show mac address-table count
show mac address-table
```
Antes del ataque
<img width="896" height="620" alt="image" src="https://github.com/user-attachments/assets/ee3d56a6-618c-426c-ab5b-9098223affa1" />

<img width="615" height="159" alt="image" src="https://github.com/user-attachments/assets/aaf1e3d3-2e89-408a-bb7b-17999c7288cd" />

---
Durante el ataque, innundación de MACs

<img width="651" height="1119" alt="image" src="https://github.com/user-attachments/assets/8efb6ddc-21c2-418c-a284-01e2e9786fbe" />

<img width="504" height="553" alt="image" src="https://github.com/user-attachments/assets/e8783a4a-c043-4ae2-a5fc-f4fb01631b18" />

<img width="573" height="231" alt="image" src="https://github.com/user-attachments/assets/85c8cfb5-0e76-4500-b7e2-c803d3339be5" />

```
# Verificacion del tráfico ajeno tcpdump -i eth0 -n
```
<img width="975" height="402" alt="image" src="https://github.com/user-attachments/assets/15349fe2-f840-48ae-8ec8-0a42e196213c" />


## Contramedida

```bash
# En IOU2 — Port Security
conf t
interface Ethernet1/0
 switchport mode access
 switchport port-security
 switchport port-security maximum 5
 switchport port-security violation restrict
end
wr

# Verificar
show port-security
show port-security interface Ethernet1/0
```
<img width="853" height="751" alt="image" src="https://github.com/user-attachments/assets/392910d8-99d4-4ab0-b849-367dfdc98aeb" />

<img width="680" height="379" alt="image" src="https://github.com/user-attachments/assets/e5cc8c33-2c64-4eab-91ad-9d85a0a87013" />

---

`````
# Resultado esperado
•	Cada puerto acepta máximo 5 MACs diferentes.
•	El exceso de MACs del atacante es descartado automáticamente.
•	La tabla CAM no puede ser desbordada.
•	El tráfico entre PCs deja de ser visible en el atacante.

`````
<img width="975" height="263" alt="image" src="https://github.com/user-attachments/assets/5d85b13d-724e-4c16-89cc-f2c05b838a75" />

<img width="511" height="216" alt="image" src="https://github.com/user-attachments/assets/378bc454-6616-4503-8e8b-0ad573c471ab" />

<img width="571" height="288" alt="image" src="https://github.com/user-attachments/assets/4456f9b0-0daf-40d1-9bbf-6dcfa68545b5" />



## Video

> Enlace al video de demostración: https://youtu.be/ejYp6q1sgTk?si=j4a7qyuvuRRH6d4M

---

## Documentación

Ver archivo incluido en este repositorio.
