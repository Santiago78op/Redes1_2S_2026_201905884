# Configuraciones por dispositivo — Proyecto 1

Un archivo por switch con su configuración **completa** (`show running-config`), nombrado igual que su
`hostname`: `SW-CORE.txt`, `SW-DIST-ID.txt`, `SW-ID-1.txt`, … El manual (§23) cita solo los comandos
relevantes; aquí queda la evidencia íntegra.

Cabecera obligatoria al inicio de cada archivo (misma convención que `APT_3/configs/`):

```
! ==========================================================
! SW-CORE  -  Core / VTP Server   (carne 201905884)
! Modelo: <modelo PT>   |   MAC (Bridge ID): <xxxx.xxxx.xxxx>
! Gi0/1-2 -> SW-SRV (Po1)  |  Gi0/3-4 -> SW-DIST-ID (Po2)
! ==========================================================
```

## Parámetros que deben aparecer en todos

| Parámetro | Valor | Dónde |
|---|---|---|
| Dominio / contraseña VTP | `Smart_8` / `proyecto12S2026` | todos |
| Modo VTP | Server (Core), Client (resto), Transparent (SW-COMUNES) | según rol |
| VLANs | 14, 24, 34, 44, 54, 94 | Server (y Transparent localmente) |
| Nativa de trunks | `switchport trunk native vlan 94` | todo trunk |
| STP | `spanning-tree mode pvst` | todos |
| EtherChannel | `channel-group N mode active` (LACP) | Core, SW-SRV, SW-DIST-ID |
| Banner | `Acceso Restringido - TechPark_201905884` | distribución (y Core) |

## Inventario

| Archivo | Rol | Estado |
|---|---|---|
| `SW-CORE.txt` | Core / VTP Server | pendiente |
| `SW-SRV.txt` | Acceso servidores | pendiente |
| `SW-DIST-ID.txt` | Distribución I+D | pendiente |
| `SW-ID-1.txt` / `SW-ID-2.txt` / `SW-ID-3.txt` | Acceso I+D (anillo) | pendiente |
| `SW-DIST-CORP.txt` | Distribución Corporativo | pendiente |
| `SW-ALA-A.txt` / `SW-ALA-B.txt` | Acceso Corporativo | pendiente |
| `SW-COMUNES.txt` | Acceso visitantes (Transparent) | pendiente |
| `SW-PLANTA.txt` | Acceso Planta | pendiente |
