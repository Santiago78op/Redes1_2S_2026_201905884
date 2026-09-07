---
tags: [redes/concepto, capa2, etherchannel, lacp, agregacion]
aliases: ["EtherChannel", "LACP", "PAgP", "port-channel", "agregación de enlaces", "802.3ad"]
---

# EtherChannel con LACP — agregación de enlaces

**EtherChannel** agrupa de 2 a 8 enlaces físicos en **un enlace lógico** (*port-channel*). Suma ancho de banda, y si un cable falla los demás siguen: exactamente lo que piden los servidores ("sin depender de una única conexión física") y el trunk de I+D ("mayor ancho de banda que el resto").

## LACP vs PAgP
| | **LACP** (mi caso, carné par) | PAgP |
|---|---|---|
| Estándar | IEEE 802.3ad, abierto | Propietario Cisco |
| Modos | `active` (inicia) / `passive` (espera) | `desirable` / `auto` |
| Combinación válida | active–active o active–passive | desirable–desirable o desirable–auto |
| Combinación inválida | passive–passive (nunca se forma) | auto–auto |

Regla práctica: **`active` en ambos extremos**, así no importa quién inicia.

## Condiciones para que el canal se forme
Todos los puertos miembros deben ser idénticos en: velocidad, dúplex, modo (access/trunk), VLAN nativa, VLANs permitidas. Un solo puerto distinto y el canal queda *suspended*. Por eso la configuración de trunk se hace en la **interfaz `port-channel`**, y los físicos la heredan.

## Interacción con STP
[[STP y PVST]] trata el port-channel como **un solo puerto**: sin EtherChannel, dos cables paralelos entre dos switches son un bucle y STP bloquea uno (ancho de banda desperdiciado); con EtherChannel, ambos reenvían.

## Evidencia
`show etherchannel summary`: la bandera debe ser **`SU`** (Layer 2, *in use*) en el canal y **`P`** (*bundled in port-channel*) en cada puerto. `D` = down, `s` = suspended, `I` = stand-alone (falló la negociación).

Comandos con mis valores en [[Comandos Cisco IOS del proyecto]]; dónde aplicarlo en [[Requerimientos por área]].

> 📚 Fuente: Cisco, *Configuring EtherChannels* (Catalyst 2960, 12.2(53)SE), enlace en el enunciado §5; IEEE 802.3ad.
