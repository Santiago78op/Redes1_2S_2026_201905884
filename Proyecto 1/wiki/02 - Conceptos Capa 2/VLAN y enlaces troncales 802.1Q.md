---
tags: [redes/concepto, capa2, vlan, trunk, 802.1q]
aliases: ["VLAN", "trunk", "troncal", "802.1Q", "VLAN nativa", "access vs trunk"]
---

# VLAN y enlaces troncales 802.1Q

Una **VLAN** es un dominio de broadcast lógico: agrupa puertos como si fueran un switch aparte, aunque compartan hardware. Es la herramienta que convierte la red plana del Tech Park en 5 redes independientes ([[Dominios de colisión y broadcast]]).

## Dos tipos de puerto
| Puerto | Qué transporta | Etiqueta 802.1Q | Dónde va |
|---|---|---|---|
| **Access** | Una sola VLAN | No (trama normal) | Hacia PCs, servidores, AP, hub |
| **Trunk** | Varias VLANs | Sí: 4 bytes con el VLAN ID en cada trama | Entre switches |

## VLAN nativa
En un trunk, la VLAN nativa viaja **sin etiqueta**. Por defecto es la 1, y eso es un riesgo (ataques de *VLAN hopping* por doble etiqueta, y la VLAN 1 lleva el control). Por eso el enunciado exige cambiarla a la **94** en todos los trunks, y **debe coincidir en ambos extremos** o CDP/STP se quejan de *native VLAN mismatch*.

## Antipatrón → idiomático
- ❌ Dejar el trunk en `dynamic auto` a ambos lados (nunca negocia trunk) → ✅ `switchport mode trunk` explícito en ambos extremos → *evita depender de DTP*.
- ❌ Permitir todas las VLANs en el trunk → ✅ `switchport trunk allowed vlan 14,24,34,44,54,94` → *reduce broadcast innecesario y documenta la intención*.
- ❌ Nativa distinta en cada extremo → ✅ misma nativa 94 en todos los trunks del campus.

## Verificación
`show vlan brief` (qué puertos están en qué VLAN) y `show interfaces trunk` (modo, encapsulación, nativa, VLANs permitidas) — el segundo es evidencia obligatoria del Manual.

Las VLANs se crean en el Server y viajan por [[VTP]]; los comandos exactos están en [[Comandos Cisco IOS del proyecto]].

> 📚 Fuente: Cisco, *Configure VLAN Trunks* (Catalyst 9000) — enlace en el enunciado §5; IEEE 802.1Q.
