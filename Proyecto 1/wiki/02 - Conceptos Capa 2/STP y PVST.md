---
tags: [redes/concepto, capa2, stp, pvst, redundancia]
aliases: ["STP", "Spanning Tree", "PVST", "PVST+", "Root Bridge", "BPDU", "bucle de capa 2"]
---

# STP y PVST — evitar bucles con redundancia

Toda redundancia de Capa 2 (el triángulo de I+D, el enlace entre alas, los dos caminos al Core) crea **bucles**: una trama de broadcast circularía para siempre y tumbaría la red (*tormenta de broadcast*). **Spanning Tree** (IEEE 802.1D) mantiene la redundancia física pero **bloquea lógicamente** los puertos sobrantes hasta que un enlace falla.

## Cómo elige qué bloquear
1. Los switches intercambian **BPDU** (*Bridge Protocol Data Units*) cada 2 s.
2. Se elige el **Root Bridge**: el de menor **Bridge ID** = prioridad (por defecto 32768 + VLAN ID) + MAC. Si nadie interviene, gana la MAC más baja, a menudo el switch más viejo y peor ubicado. Por eso la rúbrica pide **elegir y justificar** el Root.
3. Cada switch calcula el **costo** al Root (FastEthernet 19, Gigabit 4, 10 G 2 en costos clásicos) y deja un solo camino; los puertos alternativos quedan en **blocking**.

## PVST+ (lo que me toca, carné par)
*Per-VLAN Spanning Tree*: **una instancia por VLAN**, así cada VLAN puede tener un Root distinto y repartir la carga entre enlaces. En Cisco IOS es el modo por defecto y se llama `pvst` (la implementación real es PVST+, compatible con 802.1Q). Los estados por puerto son *blocking → listening → learning → forwarding*, con **30–50 s** de convergencia; Rapid-PVST (802.1w) baja eso a segundos, pero **no es el que me corresponde**.

## Elección del Root Bridge (borrador de justificación)
| VLAN | Root propuesto | Razón |
|---|---|---|
| 44 Servidores, 14 Gerencia, 34 Produccion, 54 Visitantes | **Core** | Es el centro de la jerarquía: todo el tráfico converge ahí; así ningún camino da rodeos |
| 24 Investigacion | ✍️ Core o distribuidor de I+D | Si el tráfico de I+D es mayormente interno, poner el Root en I+D acorta rutas dentro del anillo |

Comando: `spanning-tree vlan 14,34,44,54 root primary` en el Core (baja la prioridad a 24576) y `root secondary` en un respaldo. Ver [[Comandos Cisco IOS del proyecto]].

## Evidencia
`show spanning-tree` (por VLAN: quién es Root, rol y estado de cada puerto, costo) es evidencia obligatoria. La captura de una **BPDU** en Modo Simulación (Root ID, Bridge ID, costo del camino) es el alcance opcional.

Relación con [[EtherChannel LACP]]: STP ve el *port-channel* como **un solo enlace**, así los dos cables no se bloquean entre sí. Ver también [[VLAN y enlaces troncales 802.1Q]].

> 📚 Fuente: Cisco, *Configuring STP* (Catalyst 2960, 12.2(53)SE), enlace en el enunciado §5; IEEE 802.1D.
