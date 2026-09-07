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
En un trunk, la VLAN nativa viaja **sin etiqueta**. La regla exacta de Cisco: *"si un paquete tiene un VLAN ID igual al de la VLAN nativa del puerto de salida, el paquete se envia sin etiqueta; de lo contrario, el dispositivo lo envia etiquetado"*. Por defecto es la **VLAN 1**, y eso es un riesgo: la VLAN 1 transporta trafico de control y habilita ataques de *VLAN hopping* por doble etiqueta. Por eso el enunciado exige cambiarla a la **94**.

> [!warning] Debe coincidir en ambos extremos
> La documentacion es categorica: *"si la VLAN nativa de un extremo del trunk es distinta de la del otro extremo, **pueden producirse bucles de spanning tree**"*. No es un aviso cosmetico de CDP: es una causa real de bucle.

## DTP: por que se declara el trunk a mano
El *Dynamic Trunking Protocol* negocia el modo del enlace. Modos y con quien forman trunk:

| Modo local | Forma trunk con |
|---|---|
| `trunk` (permanente) | `trunk`, `dynamic desirable`, `dynamic auto` |
| `dynamic desirable` | `trunk`, `dynamic desirable`, `dynamic auto` |
| `dynamic auto` | **solo** `trunk` o `dynamic desirable` |
| `access` | con ninguno |
| `nonegotiate` | no emite tramas DTP: hay que declarar el trunk en ambos extremos |

De ahi el antipatron clasico: `dynamic auto` en los dos lados **nunca** negocia trunk. Y hay una razon de seguridad para no depender de DTP: *"DTP puede representar un riesgo de seguridad [...] un atacante puede conectar un dispositivo a ese puerto y, enviando tramas DTP, forzarlo a modo troncal"*.

## Antipatrón → idiomático
- ❌ Dejar el trunk en `dynamic auto` a ambos lados (nunca negocia trunk) → ✅ `switchport mode trunk` explícito en ambos extremos → *evita depender de DTP*.
- ❌ Permitir todas las VLANs en el trunk (por defecto viajan **todas, de la 1 a la 4094**) → ✅ `switchport trunk allowed vlan 14,24,34,44,54,94` → *reduce broadcast innecesario, saca la VLAN 1 del trunk y documenta la intención*.
- ❌ Nativa distinta en cada extremo → ✅ misma nativa 94 en todos los trunks del campus.

## Verificación
`show vlan brief` (qué puertos están en qué VLAN) y `show interfaces trunk` (modo, encapsulación, nativa, VLANs permitidas) — el segundo es evidencia obligatoria del Manual.

Las VLANs se crean en el Server y viajan por [[VTP]]; los comandos exactos están en [[Comandos Cisco IOS del proyecto]].

> 📚 Fuente: Cisco, [*Configure VLAN Trunks*](https://www.cisco.com/c/en/us/td/docs/switches/lan/c9000/lyr2-fwd/vlan/vlan-configuration-guide/configure-vlan-trunks.html) (Catalyst 9000), consultado el 2026-09-07 — enlace del enunciado §5; IEEE 802.1Q.
