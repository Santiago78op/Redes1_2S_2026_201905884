---
tags: [redes/concepto, capa1, capa2, dominios]
aliases: ["dominio de colisión", "dominio de broadcast", "collision domain", "broadcast domain", "contar dominios"]
---

# Dominios de colisión y de broadcast

Son las dos "fronteras" que el proyecto pide tabular. Se cuentan con reglas distintas porque viven en capas distintas.

## Dominio de colisión (Capa 1)
Conjunto de dispositivos que **comparten el medio**: si dos transmiten a la vez, las tramas chocan y CSMA/CD obliga a reintentar.
- **Hub**: repite eléctricamente todo por todos los puertos → **un solo** dominio de colisión para todo lo que cuelga de él (half-duplex).
- **Switch**: cada puerto es su propio segmento → **un dominio de colisión por puerto activo**. Con full-duplex, en la práctica no hay colisiones, pero el dominio "existe" y así lo cuenta la rúbrica.
- **Router**: también separa dominios de colisión (y de broadcast).

Regla para la tabla del Manual: `dominios de colisión de un switch = número de puertos con cable conectado`. El puerto que va al hub cuenta como **uno**, y ese es el dominio compartido de la Planta (hub + todas las máquinas + ese puerto).

## Dominio de broadcast (Capa 2)
Alcance de una trama con destino `FF:FF:FF:FF:FF:FF`. Un switch la **inunda** por todos los puertos de la misma VLAN; solo la frenan un **router** o el límite de una **VLAN**.
- Red plana con N switches = **1** dominio de broadcast (el problema del Tech Park).
- Con VLANs = **un dominio de broadcast por VLAN activa**, sin importar cuántos switches la transporten. Para mí: VLANs 14, 24, 34, 44, 54 → 5 dominios (más la 94 nativa si lleva tráfico).

## Impacto del hub Legacy (para la sección de la Planta)
- Half-duplex y colisiones → retransmisiones, latencia variable, ancho de banda efectivo muy por debajo del nominal.
- Toda trama de una máquina la ven todas las demás (sin privacidad).
- Una tormenta o una NIC dañada afecta a todo el segmento.

**Contención desde el switch de acceso** (sin quitar el hub): confinar el hub a la **VLAN 34** (limita el broadcast), `storm-control broadcast level` en ese puerto, `switchport port-security maximum N` con las MAC de las máquinas, y un único puerto access para el hub, de modo que el dominio de colisión sea uno y no se propague.

Ver [[VLAN y enlaces troncales 802.1Q]] para cómo las VLANs parten el broadcast, y [[Requerimientos por área]] para dónde va cada cosa.

> 📚 Fuente: Cisco Networking Academy, *Switching, Routing and Wireless Essentials*, cap. 1–2; enunciado §4.1 y §4.5.
