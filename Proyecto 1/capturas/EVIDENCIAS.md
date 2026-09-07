# Evidencias del Proyecto 1 — SmartCity Tech Park

**Carné:** 201905884 · **X = 4, # = 8** · **Archivo:** `Proyecto1_201905884.pkt`
**Parámetros:** VLANs 14/24/34/44/54 · nativa 94 · VTP `Smart_8` · LACP · PVST+

Todas las capturas se toman sobre la simulación corriendo en Packet Tracer, a resolución completa
de la ventana del dispositivo, de modo que en la barra de título se vea **de qué equipo salió cada
salida**. Nombre de archivo: `NN-<dispositivo>-<comando>.png`, en minúsculas y con guiones.

## Carpetas

| Carpeta | Contenido | Sección del manual |
|---|---|---|
| `topologia/` | Topología completa con medios etiquetados | §11 |
| `areas/` | Una captura por área (Core, I+D, Corporativo, Planta) | §12 |
| `evidencias/` | Salidas de `show`, pings, pruebas de falla, PDUs | §17–§24, §27 |
| `laboratorio/` | Fotos y salidas de los switches reales (parte física) | §25 |

---

## Índice de capturas

| # | Archivo | Dispositivo | Comando / acción | Qué evidencia | § |
|---|---------|-------------|------------------|---------------|---|
| 0 | `topologia/00-topologia-completa.png` | — | — | Jerarquía Core → distribución → acceso, medios etiquetados | 11 |
| 1 | `areas/01-centro-de-datos.png` | — | — | Core VTP Server + granja de servidores por EtherChannel | 12.1 |
| 2 | `areas/02-centro-id.png` | — | — | Anillo de 3 switches, ≥ 8 estaciones, trunk de mayor capacidad | 12.2 |
| 3 | `areas/03-edificio-corporativo.png` | — | — | Dos alas con enlace directo, Áreas Comunes con AP | 12.3 |
| 4 | `areas/04-planta-produccion.png` | — | — | Hub Legacy colgado de un puerto del switch de acceso | 12.4 |
| 5 | `evidencias/01-sw-core-show-vtp-status.png` | SW-CORE | `show vtp status` | Modo Server, dominio `Smart_8`, revisión, 5 VLANs | 17 |
| 6 | `evidencias/02-<client>-show-vlan-brief.png` | (un Client) | `show vlan brief` | VLANs 14/24/34/44/54 propagadas sin crearse localmente | 17 |
| 7 | `evidencias/03-sw-core-show-spanning-tree.png` | SW-CORE | `show spanning-tree` | **`This bridge is the root`** en las VLANs asignadas | 18 |
| 8 | `evidencias/04-<switch>-puerto-bloqueado.png` | (I+D o ala) | `show spanning-tree vlan NN` | Puerto `Altn BLK`: el que rompe el bucle | 18 |
| 9 | `evidencias/05-sw-core-show-etherchannel-summary.png` | SW-CORE | `show etherchannel summary` | Po1/Po2 en `SU`, miembros en `P` | 19 |
| 10 | `evidencias/06-<switch>-show-interfaces-trunk.png` | (distribución) | `show interfaces trunk` | Nativa 94, VLANs permitidas | 20, 22 |
| 11 | `evidencias/07-banner-motd.png` | (distribución) | inicio de sesión | `Acceso Restringido - TechPark_201905884` | 22 |
| 12 | `evidencias/08-ping-intra-vlan.png` | PC | `ping` | 0 % loss dentro de la misma VLAN | 24 |
| 13 | `evidencias/09-ping-inter-vlan.png` | PC | `ping` | 100 % loss entre VLANs distintas | 24 |
| 14 | `evidencias/10-falla-switch-id.png` | — | apagar un switch de I+D | Los otros dos siguen conectados | 24 |
| 15 | `evidencias/11-falla-uplink-ala.png` | — | apagar uplink de un ala | Ala A ↔ Ala B sigue activo | 24 |
| 16 | `evidencias/12-bpdu.png` (opcional) | — | Modo Simulación, STP | Root ID, Bridge ID, costo en la BPDU | 27 |
| 17 | `evidencias/13-pdu-vtp.png` (opcional) | — | Modo Simulación, VTP | Domain Name y Configuration Revision Number | 27 |

<!-- Al agregar una captura: nombrarla según la convención, subirla a su carpeta y completar la fila. -->

---

## Lo que hay que saber leer de cada captura

<!-- Modelo: capturas/EVIDENCIAS.md de la APT 3. Por cada evidencia clave, pegar el fragmento de la salida y señalar la línea que demuestra el punto (ej. "This bridge is the root", "Gi0/2 Altn BLK", "Po1(SU)", "Native vlan 94"). -->
