# Diagramas — Proyecto 1, SmartCity Tech Park

Figuras del Manual Técnico que **no** salen de Packet Tracer (las capturas del simulador están en
`../capturas/`). Son diagramas propios en **SVG**, que es vectorial: se ven nítidos en GitHub y al
imprimir.

**Convención de nombre:** `NN-nombre-en-kebab-case.svg`, donde `NN` es el orden dentro de esta
carpeta. El número de **Figura** del Manual es otra serie y está en la columna «Fig.».

## Índice

### Marco Teórico

| Archivo | Fig. | § | Qué muestra |
| --- | --- | --- | --- |
| `01-red-plana-problema.svg` | F1 | 2 | La red plana actual con sus cuatro síntomas |
| `02-dominios-colision.svg` | F2 | 3.1 | Hub (1 dominio compartido) vs. switch (1 por puerto) |
| `03-dominios-broadcast.svg` | F3 | 3.2 | Red plana = 1 dominio · con VLANs = 1 por VLAN |
| `04-access-vs-trunk.svg` | F4 | 4.2 | Puerto access y puerto trunk lado a lado |
| `05-trama-8021q.svg` | F5 | 4.3 | Trama Ethernet con el tag de 4 bytes desglosado |
| `06-vtp-modos.svg` | F6 | 5.2 | Anuncios entre Server, Client y Transparent |
| `07-bucle-capa2.svg` | F7 | 6.1 | Tormenta de broadcast en un triángulo de switches |
| `08-eleccion-root-bridge.svg` | F8 | 6.2 | Bridge ID, costos y el puerto que queda bloqueado |
| `09-etherchannel-lacp.svg` | F9 | 7.1 | Enlaces físicos agrupados en un port-channel |
| `10-medios-transmision.svg` | F10 | 8 | Alcance y ancho de banda de UTP vs. fibra |
| `11-seguridad-capa2.svg` | F11 | 9.1 | VLAN hopping por doble etiquetado y MAC flooding |

### Marco Práctico

| Archivo | Fig. | § | Qué muestra |
| --- | --- | --- | --- |
| `12-topologia-logica.svg` | F13 | 11 | Jerarquía Core → distribución → acceso, VLANs, canales y medios |
| `13-dominios-broadcast-campus.svg` | F18 | 16 | Las 5 VLANs como dominios independientes sobre la planta física |
| `14-arbol-stp.svg` | F19 | 18 | Root Bridge por VLAN y puertos bloqueados |

F13, F18 y F19 describen la red implementada y se contrastaron con la captura de la topología (F12),
la tabla de §16 y las salidas de `show spanning-tree` (E3 y E4).

## Estilo

| Elemento | Convención |
| --- | --- |
| Fibra óptica | Línea naranja gruesa |
| Cobre UTP | Línea azul delgada |
| Enlace bloqueado por STP | Línea punteada roja con candado |
| Problema / ataque | Rojo |
| Solución / estado correcto | Verde |
| VLANs | Un color fijo por VLAN, el mismo en todas las figuras (tabla abajo) |

Los colores de **medio** (naranja fibra, azul cobre) se usan sólo como **línea**; los de **VLAN**,
sólo como **relleno** de nodos y nubes. Así el azul del cobre y el de una VLAN nunca se confunden
aunque aparezcan en la misma figura.

### Paleta de VLANs

| VLAN | Nombre | Color | Hex |
| --- | --- | --- | --- |
| 14 | GERENCIA | violeta | `#7048e8` |
| 24 | INVESTIGACION | turquesa | `#0c8599` |
| 34 | PRODUCCION | ámbar | `#f08c00` |
| 44 | SERVIDORES | grafito | `#343a40` |
| 54 | VISITANTES | rosa | `#d6336c` |
| 94 | nativa (control) | gris punteado | `#adb5bd` |

Ninguno es rojo ni verde puros, que están reservados para *problema* y *estado correcto*.
