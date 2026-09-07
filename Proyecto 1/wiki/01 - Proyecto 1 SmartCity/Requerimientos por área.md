---
tags: [redes/proyecto, proyecto1, diseño, topologia]
aliases: ["áreas", "edificios", "requerimientos de diseño", "topología por área"]
---

# Requerimientos por área y cómo pienso resolverlos

Cuatro áreas, un switch central y una regla transversal: **todo lo que no sea obligatorio queda a mi criterio, pero debe justificarse en el Manual**. Este es el borrador de decisiones; lo que tenga ✍️ todavía no está decidido.

## 1. Centro de Datos (Core)
| Exige el enunciado | Idea de solución |
|---|---|
| Administración centralizada del dominio VTP | Switch Core en **VTP Server** ([[VTP]]) |
| Trunks hacia los 3 edificios, modelo jerárquico | Core ↔ distribución de cada edificio, trunk 802.1Q, nativa 94 |
| Granja de ≥ 4 servidores con enlace de alto tráfico **sin depender de una sola conexión física** | Switch de servidores → Core por **EtherChannel LACP de 2+ enlaces** ([[EtherChannel LACP]]); servidores en VLAN 44 |
| Cantidad de switches intermedios a criterio | ✍️ 1 switch de acceso para servidores, o conectar servidores al Core y justificar |

## 2. Centro de I+D
| Exige | Idea |
|---|---|
| ≥ 3 switches interconectados: la caída de uno no aísla a los demás | **Triángulo/anillo** de 3 switches: cada uno tiene dos caminos; [[STP y PVST]] bloquea uno |
| Trunk hacia el Core con **más ancho de banda** que los demás | **EtherChannel** de 2 Gigabit (o fibra Gigabit vs cobre en el resto) — el "enlace gordo" del campus |
| ≥ 8 estaciones de trabajo | 8+ PCs/laptops en VLAN 24 repartidas en los 3 switches |
| Alta disponibilidad | ✍️ Root Bridge de la VLAN 24: ¿el Core o el distribuidor de I+D? Justificar |

## 3. Edificio Corporativo
| Exige | Idea |
|---|---|
| Dos alas, cada una con su switch de acceso | Distribución + 2 acceso (Ala A, Ala B) |
| Conectividad entre alas aunque caiga la ruta al distribuidor | **Enlace directo Ala A ↔ Ala B** (triángulo con el distribuidor); STP lo bloquea en normal y lo activa si falla el uplink |
| Áreas Comunes para visitantes con **aislamiento total de tráfico y administración de VLANs** | VLAN 54 Visitantes; el switch de Áreas Comunes en **VTP Transparent** para que no administre ni reciba la base del dominio ✍️ justificar |
| Servicio inalámbrico a laptops de invitados | **Access Point** en puerto access VLAN 54 + laptops con tarjeta inalámbrica |
| Gerencia | VLAN 14 en puertos access del personal administrativo |
| Banner MOTD | En el switch de distribución (y en todos los de distribución del campus) |

## 4. Planta de Producción (Legacy)
| Exige | Idea |
|---|---|
| Dominio de colisión compartido en Capa 1, evidente | **Hub** con las máquinas industriales, conectado a **un puerto** del switch de acceso |
| Integrado a la red | Switch de acceso en VLAN 34, trunk al Core (o a un distribuidor) |
| Documentar impacto y **medidas de contención a nivel de switch de acceso** | Impacto: half-duplex, CSMA/CD, colisiones, retransmisiones, latencia. Contención: `storm-control broadcast`, `port-security` con máximo de MACs, confinar el hub a la VLAN 34, un solo puerto de acceso para el hub. → [[Dominios de colisión y broadcast]] |

## Medio de transmisión (decisión transversal)
Regla general que voy a justificar: **fibra** en troncales entre edificios (distancia > 100 m, mayor ancho de banda, inmunidad electromagnética — la Planta es industrial), **cobre UTP Cat 6/6A** dentro de cada edificio. En Packet Tracer los puertos de fibra requieren módulos SFP (p. ej. `GLC-LH-SMD` en un 3560/3650) o el módulo de fibra del switch genérico; verificarlo al armar. Etiquetar cada medio en el `.pkt`.

## Diagrama borrador
```mermaid
flowchart TD
    CORE[Core - VTP Server<br/>Centro de Datos]
    SRV[Sw Servidores<br/>VLAN 44]
    DID[Dist I+D]
    A1[Sw I+D 1] --- A2[Sw I+D 2] --- A3[Sw I+D 3] --- A1
    DCO[Dist Corporativo<br/>banner MOTD]
    ALA[Ala A - VLAN 14] --- ALB[Ala B]
    AC[Areas Comunes<br/>VTP Transparent - VLAN 54] --> AP((AP))
    DPR[Sw Acceso Planta<br/>VLAN 34] --> HUB{{Hub Legacy}}
    SRV ==LACP== CORE
    CORE ==LACP / fibra== DID
    CORE --fibra--> DCO
    CORE --fibra--> DPR
    DID --- A1
    DCO --- ALA
    DCO --- ALB
    DCO --- AC
```

Volver a [[Proyecto 1 - SmartCity Tech Park]] · Ver [[Ambigüedades y riesgos del enunciado]].

> 📚 Fuente: enunciado §4.2 "Requerimientos de Diseño Topológico" y §4.3.
