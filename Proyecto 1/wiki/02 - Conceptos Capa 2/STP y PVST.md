---
tags: [redes/concepto, capa2, stp, pvst, redundancia]
aliases: ["STP", "Spanning Tree", "PVST", "PVST+", "Root Bridge", "BPDU", "bucle de capa 2"]
---

# STP y PVST — evitar bucles con redundancia

Toda redundancia de Capa 2 (el triángulo de I+D, el enlace entre alas, los dos caminos al Core) crea **bucles**: una trama de broadcast circularía para siempre y tumbaría la red (*tormenta de broadcast*). **Spanning Tree** (IEEE 802.1D) mantiene la redundancia física pero **bloquea lógicamente** los puertos sobrantes hasta que un enlace falla.

## Cómo elige qué bloquear
1. Los switches intercambian **BPDU** (*Bridge Protocol Data Units*) cada **2 s** (*hello time*).
2. Se elige el **Root Bridge**: el de menor **Bridge ID**, compuesto por *"un valor de prioridad de 4 bits y un ID de sistema extendido de 12 bits igual al VLAN ID"* mas los 6 bytes de la **MAC**. La prioridad por defecto es **32768**. Empatadas las prioridades, *"el switch con la MAC mas baja de la VLAN se convierte en el switch raiz"* — a menudo el equipo mas viejo y peor ubicado. Por eso la rúbrica pide **elegir y justificar** el Root.
3. Cada switch calcula el **costo** acumulado al Root y deja un solo camino; los puertos alternativos quedan en **blocking**.

| Velocidad del enlace | Costo por defecto |
|---|---|
| 10 Mbps | 100 |
| 100 Mbps | 19 |
| 1 Gbps | 4 |

(La guía del 2960 tabula hasta 1 Gbps; los 10 Gbps valen 2 en la tabla ampliada de 802.1D-2004.)

## Estados y roles de puerto
Estados: **blocking** (no reenvía ni aprende), **listening** (primer estado transitorio), **learning** (aprende MAC, aún no reenvía), **forwarding** (reenvía y aprende) y **disabled**. Roles: **root port** (mejor camino al Root), **designated port** (menor costo en el segmento) y **alternate/backup** (bloqueados, la reserva).

Temporizadores por defecto: *"hello time 2 segundos, forward-delay 15 segundos, max-age 20 segundos"*, de donde sale la convergencia de **~50 s** (max-age + 2 × forward-delay).

## PVST+ (lo que me toca, carné par)
*Per-VLAN Spanning Tree*: **una instancia por VLAN**, así cada VLAN puede tener un Root distinto y repartir la carga entre enlaces. En Cisco IOS se selecciona con `spanning-tree mode pvst`; la implementación real es **PVST+**, *"basado en IEEE 802.1D"*. Rapid-PVST+ usa **802.1w** y converge en segundos —*"borra de inmediato las entradas MAC aprendidas dinamicamente, puerto por puerto, al recibir un cambio de topologia"*—, pero **no es el que me corresponde** (carné par → PVST).

## Elección del Root Bridge (borrador de justificación)
| VLAN | Root propuesto | Razón |
|---|---|---|
| 44 Servidores, 14 Gerencia, 34 Produccion, 54 Visitantes | **Core** | Es el centro de la jerarquía: todo el tráfico converge ahí; así ningún camino da rodeos |
| 24 Investigacion | ✍️ Core o distribuidor de I+D | Si el tráfico de I+D es mayormente interno, poner el Root en I+D acorta rutas dentro del anillo |

Comando: `spanning-tree vlan 14,34,44,54 root primary` en el Core y `root secondary` en un respaldo. El manual explica qué hace por dentro: *"el software revisa la prioridad de los switches raiz de cada VLAN [...] y fija su propia prioridad en **24576** si ese valor lo convierte en raiz"*. La forma explícita es `spanning-tree vlan 24 priority <valor>`, y **el valor debe ser múltiplo de 4096** (4096, 8192, 12288 ... 61440). Ver [[Comandos Cisco IOS del proyecto]].

## Evidencia
`show spanning-tree` (por VLAN: quién es Root, rol y estado de cada puerto, costo) es evidencia obligatoria. La captura de una **BPDU** en Modo Simulación (Root ID, Bridge ID, costo del camino) es el alcance opcional.

Relación con [[EtherChannel LACP]]: STP ve el *port-channel* como **un solo enlace**, así los dos cables no se bloquean entre sí. Ver también [[VLAN y enlaces troncales 802.1Q]].

> 📚 Fuente: Cisco, [*Configuring STP*](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst2960/software/release/12-2_53_se/configuration/guide/2960scg/swstp.html) (Catalyst 2960, IOS 12.2(53)SE), consultado el 2026-09-07 — enlace del enunciado §5; IEEE 802.1D. Cita de apertura: *"STP es un protocolo de gestion de enlaces de Capa 2 que provee redundancia de caminos evitando bucles en la red."*
