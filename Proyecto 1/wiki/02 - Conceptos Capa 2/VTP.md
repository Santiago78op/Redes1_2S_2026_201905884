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

## El número de revisión (la trampa clásica)
Cada cambio en el Server incrementa el **configuration revision number**. Cuando dos switches del mismo dominio se conectan, **gana el de revisión más alta**, aunque sea un Client. Un switch reciclado con revisión 30 puede **borrar** las VLANs del campus con revisión 5. Mitigación: antes de conectar un switch, ponerlo en Transparent y luego en Client (eso resetea la revisión a 0), y usar **contraseña** de dominio — la nuestra es `proyecto12S2026`.

## Requisitos para que funcione
1. Mismo **dominio** (`Smart_8`) — sensible a mayúsculas.
2. Misma **contraseña**.
3. Misma **versión** de VTP.
4. Enlace entre ellos en modo **trunk** (VTP viaja solo por trunks, en la VLAN nativa).

## Verificación y evidencia
`show vtp status` muestra modo, dominio, revisión y cantidad de VLANs; `show vlan brief` en un Client debe listar las VLANs 14/24/34/44/54 que nunca se escribieron ahí. Esa captura es la "justificación del switch servidor" que pide el Manual. En el alcance opcional, la PDU VTP capturada en Modo Simulación muestra el *Domain Name* y el *Revision Number*.

Comandos en [[Comandos Cisco IOS del proyecto]]; decisión sobre Transparent en [[Ambigüedades y riesgos del enunciado]]; las VLANs que propaga en [[Parámetros por carné 201905884]].

> 📚 Fuente: Cisco, *Understanding VLAN Trunk Protocol (VTP)*, doc 10558 — enlace en el enunciado §5.
