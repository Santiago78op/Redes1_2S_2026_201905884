---
tags: [redes/concepto, capa2, vtp, cisco]
aliases: ["VTP", "VLAN Trunking Protocol", "vtp server", "vtp client", "vtp transparent", "revision number"]
---

# VTP — VLAN Trunking Protocol

Protocolo **propietario de Cisco** que sincroniza la base de datos de VLANs (IDs y nombres) entre switches de un mismo **dominio**, a través de los trunks. Evita crear las 5 VLANs a mano en cada switch: se crean en el Server y se propagan.

## Los tres modos
| Modo | Crea/borra VLANs | Recibe y adopta anuncios | Reenvía anuncios | Rol en mi proyecto |
|---|---|---|---|---|
| **Server** | Sí | Sí | Sí | Core del Centro de Datos (administración centralizada) |
| **Client** | No | Sí | Sí | Distribución y acceso de I+D, Corporativo, Planta |
| **Transparent** | Sí, pero solo localmente | **No** adopta | Sí (v2) | Switch de Áreas Comunes: aísla la administración de VLANs del resto del campus |
| *Off* | Solo localmente | No | **No** reenvía | Igual que Transparent, pero ni siquiera propaga anuncios |

Textualmente: *"los switches VTP transparentes no participan en VTP"* y no se sincronizan con los anuncios, aunque *"si reenvian los anuncios VTP por sus puertos troncales en VTP version 2"*. Esa distincion —no adopta, pero reenvia— es justo lo que necesita el switch de Áreas Comunes: se aisla de la administracion sin romper la propagacion hacia el resto del campus.

## El número de revisión (la trampa clásica)
*"Cada vez que se hace un cambio de VLAN en un dispositivo VTP, la revision de configuracion se incrementa en uno."* Un switch **ignora** los anuncios cuya revision sea menor o igual a la propia; si la recibida es mayor, adopta esa base de datos. Consecuencia: **gana la revision mas alta**, aunque venga de un Client. Un switch reciclado con revision 30 puede **borrar** las VLANs de un campus que va en revision 5.

La advertencia de Cisco es literal: *"recuerde la revision de configuracion y como reiniciarla cada vez que inserte un switch nuevo en su red, para no tumbar la red entera"*. Se reinicia **cambiando el nombre de dominio y restaurandolo** (o pasando por Transparent), y se protege con la **contraseña** de dominio — la nuestra es `proyecto12S2026`.

## Requisitos para que funcione
1. Mismo **dominio** (`Smart_8`) — sensible a mayúsculas.
2. Misma **contraseña**.
3. Misma **versión** de VTP.
4. Enlace entre ellos en modo **trunk** (VTP viaja solo por trunks, en la VLAN nativa).

## Verificación y evidencia
`show vtp status` muestra modo, dominio, revisión y cantidad de VLANs; `show vlan brief` en un Client debe listar las VLANs 14/24/34/44/54 que nunca se escribieron ahí. Esa captura es la "justificación del switch servidor" que pide el Manual. En el alcance opcional, la PDU VTP capturada en Modo Simulación muestra el *Domain Name* y el *Revision Number*.

Comandos en [[Comandos Cisco IOS del proyecto]]; decisión sobre Transparent en [[Ambigüedades y riesgos del enunciado]]; las VLANs que propaga en [[Parámetros por carné 201905884]].

> 📚 Fuente: Cisco, [*Understanding VLAN Trunk Protocol (VTP)*](https://www.cisco.com/c/en/us/support/docs/lan-switching/vtp/10558-21.html), doc 10558, consultado el 2026-09-07 — enlace del enunciado §5.
