# Diagramas — Práctica 2, Red de Cayalá

Figuras del Manual Técnico que no salen de Packet Tracer (las capturas del simulador están en
`../capturas/`). Son diagramas propios en SVG.

| Archivo | Fig. | § | Qué muestra |
| --- | --- | --- | --- |
| `01-dominios-colision.svg` | F1 | 1 | Hub (un dominio compartido) frente a switch (uno por puerto) |
| `02-dominios-broadcast.svg` | F2 | 1 | Un dominio de broadcast sin VLANs; uno por VLAN con ellas |
| `03-access-vs-trunk.svg` | F3 | 2 | Puerto de acceso y puerto troncal |
| `04-trama-8021q.svg` | F4 | 2 | Trama Ethernet con el tag 802.1Q |
| `05-bucle-capa2.svg` | F5 | 4 | Tormenta de broadcast sin Spanning Tree |
| `06-eleccion-root-bridge.svg` | F6 | 4 | Elección de la raíz y puerto bloqueado |
| `07-etherchannel-lacp.svg` | F7 | 5 | Enlaces físicos agrupados en un canal |
| `08-vtp-multiservidor.svg` | F8 | 15 | Un servidor VTP por zona |
| `09-topologia-logica.svg` | F9 | 10 | Zonas, VLANs y enlaces |
| `10-topologia-hibrida.svg` | F10 | 10 | Malla, anillo y estrella sobre la misma red |
| `11-vlsm.svg` | F11 | 12 | Reparto de 192.168.4.0/24 |
| `12-arbol-stp.svg` | F12 | 16 | Raíz y puertos alternos por VLAN |
| `13-pruebas-de-falla.svg` | F13 | 22 | Cuatro fallas inducidas y su resultado |
| `14-enrutamiento-svi.svg` | F14 | 18 | Camino de un paquete entre dos zonas |

F1 a F7 son diagramas de teoría reutilizados del Proyecto 1, con la VLAN nativa actualizada a 99.
F8 a F14 describen la red implementada; F12 y F13 se dibujaron a partir de las salidas de
`show spanning-tree` y de los pings medidos.

## Paleta de VLANs

| VLAN | Zona | Color | Hex |
| --- | --- | --- | --- |
| 14 | Paseo Cayalá | violeta | `#7048e8` |
| 24 | Distrito Empresarial | turquesa | `#0c8599` |
| 34 | Décimo de Cayalá | ámbar | `#f08c00` |
| 44 | Distrito Moda | grafito | `#343a40` |
| 54 | Encinos de Cayalá | rosa | `#d6336c` |

Rojo y verde quedan reservados para *falla* y *camino activo*.
