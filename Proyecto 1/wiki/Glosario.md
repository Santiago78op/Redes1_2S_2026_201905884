---
tags: [redes, glosario, referencia]
aliases: [términos, definiciones, vocabulario]
---

# Glosario de Redes 1

| Término | Definición en una línea | Nota relacionada |
|---|---|---|
| Dominio de colisión | Segmento donde dos tramas enviadas a la vez chocan; cada puerto de switch es uno, un hub entero es uno solo. | [[Dominios de colisión y broadcast]] |
| Dominio de broadcast | Alcance de una trama de difusión; lo delimita un router o una VLAN. | [[Dominios de colisión y broadcast]] |
| VLAN | Red local virtual: un dominio de broadcast lógico independiente del cableado físico. | [[VLAN y enlaces troncales 802.1Q]] |
| Trunk (troncal) | Enlace que transporta varias VLANs etiquetando cada trama con 802.1Q. | [[VLAN y enlaces troncales 802.1Q]] |
| VLAN nativa | La única VLAN que viaja sin etiqueta por un trunk; por seguridad se cambia de la 1. | [[VLAN y enlaces troncales 802.1Q]] |
| VTP | Protocolo Cisco que propaga la base de VLANs desde un switch Server a los Client. | [[VTP]] |
| Revision number | Contador de cambios de VTP; el más alto gana y sobrescribe a los demás. | [[VTP]] |
| STP / PVST | Protocolo que bloquea puertos redundantes para evitar bucles; PVST corre una instancia por VLAN. | [[STP y PVST]] |
| Root Bridge | Switch de referencia del árbol STP; todos los caminos se calculan hacia él. | [[STP y PVST]] |
| BPDU | Trama de control de STP que lleva Root ID, Bridge ID y costo. | [[STP y PVST]] |
| EtherChannel | Agrupación de varios enlaces físicos en uno lógico para sumar ancho de banda y tolerancia a fallos. | [[EtherChannel LACP]] |
| LACP / PAgP | Protocolos de negociación de EtherChannel: LACP es estándar IEEE, PAgP es propietario Cisco. | [[EtherChannel LACP]] |
| Legacy | Equipo o protocolo heredado que no se puede reemplazar de inmediato (el hub de la Planta). | [[Requerimientos por área]] |
| MOTD | *Message of the day*: banner que muestra el switch al iniciar sesión. | [[Comandos Cisco IOS del proyecto]] |
| DTP | Protocolo Cisco que negocia si un enlace se vuelve trunk; dos puertos en `dynamic auto` nunca lo forman. | [[VLAN y enlaces troncales 802.1Q]] |
| Bridge ID | Prioridad (4 bits) + ID de sistema extendido (12 bits, igual al VLAN ID) + MAC; decide quién es Root. | [[STP y PVST]] |
| Port-channel | Interfaz lógica que representa un EtherChannel; ahí se configura el trunk y los puertos físicos lo heredan. | [[EtherChannel LACP]] |
| PortFast | Salta los estados de STP en un puerto hacia un dispositivo final; nunca hacia otro switch. | [[STP y PVST]] |
| storm-control | Limita el porcentaje de broadcast que un puerto admite antes de descartarlo. | [[Dominios de colisión y broadcast]] |
| port-security | Restringe cuántas y cuáles direcciones MAC puede aprender un puerto. | [[Dominios de colisión y broadcast]] |

Volver al [[00 - 🌐 Cerebro Redes (MOC)|MOC]].
