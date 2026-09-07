---
tags: [redes/concepto, capa2, etherchannel, lacp, agregacion]
aliases: ["EtherChannel", "LACP", "PAgP", "port-channel", "agregación de enlaces", "802.3ad"]
---

# EtherChannel con LACP — agregación de enlaces

**EtherChannel** agrupa hasta **8 puertos** en **un enlace logico** (*port-channel*); en el Catalyst 2960 el limite es de **6 EtherChannel por switch**. Cisco lo define asi: *"EtherChannel provee enlaces de alta velocidad tolerantes a fallos entre switches, routers y servidores"* y *"provee recuperacion automatica ante la perdida de un enlace, redistribuyendo la carga entre los enlaces restantes"*. Es exactamente lo que piden los servidores ("sin depender de una unica conexion fisica") y el trunk de I+D ("mayor ancho de banda que el resto").

## LACP vs PAgP
| | **LACP** (mi caso, carné par) | PAgP |
|---|---|---|
| Estándar | IEEE 802.3ad, abierto | Propietario Cisco |
| Modos | `active` (inicia) / `passive` (espera) | `desirable` / `auto` |
| Combinación válida | active–active o active–passive | desirable–desirable o desirable–auto |
| Combinación inválida | passive–passive (nunca se forma) | auto–auto |

Regla practica: **`active` en ambos extremos**, asi no importa quien inicia. Existe ademas el modo `on`, que *"fuerza al puerto a unirse a un EtherChannel sin negociacion"*, pero exige `on` en los dos extremos y pierde la verificacion del protocolo.

### Balanceo de carga
El canal reparte el trafico por **flujo**, no por trama suelta: `src-mac` (por defecto), `dst-mac`, `src-dst-mac`, `src-ip`, `dst-ip`, `src-dst-ip`. Consecuencia practica: un solo par origen-destino **no** alcanza la suma de los enlaces; el beneficio aparece con trafico de muchos hosts, que es el caso de la granja de servidores.

## Condiciones para que el canal se forme
Todos los puertos miembros deben coincidir en: **velocidad y duplex, VLAN nativa, lista de VLANs permitidas y modo de trunk** (ISL vs 802.1Q). *"Los puertos que no son compatibles quedan suspendidos, incluso si se configuran en modo `on`."* Por eso la configuracion de trunk se hace en la **interfaz `port-channel`** y los fisicos la heredan: evita que una diferencia tipeada a mano suspenda un miembro.

## Interacción con STP
[[STP y PVST]] trata el port-channel como **un solo puerto**: sin EtherChannel, dos cables paralelos entre dos switches son un bucle y STP bloquea uno (ancho de banda desperdiciado); con EtherChannel, ambos reenvían.

## Evidencia
`show etherchannel summary`: la bandera debe ser **`SU`** (`S` = Layer 2, `U` = *in use*) en el canal y **`P`** (*bundled in port-channel*) en cada puerto miembro. Otras banderas: `D` = down, `s` = suspended, `I` = stand-alone (no negocio), `H` = *hot-standby*, que la guia documenta para LACP cuando hay mas de 8 puertos configurados.

Comandos con mis valores en [[Comandos Cisco IOS del proyecto]]; dónde aplicarlo en [[Requerimientos por área]].

> 📚 Fuente: Cisco, [*Configuring EtherChannels*](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst2960/software/release/12-2_53_se/configuration/guide/2960scg/swethchl.html) (Catalyst 2960, IOS 12.2(53)SE), consultado el 2026-09-07 — enlace del enunciado §5; IEEE 802.3ad. Nota: la tabla completa de banderas de `show etherchannel summary` no está en esa página; se lee en la leyenda que imprime el propio comando.
