---
tags: [redes/comandos, cisco, ios, cheatsheet, proyecto1]
aliases: ["comandos", "cheat sheet", "IOS", "configuración de switches", "show commands"]
---

# Comandos Cisco IOS del Proyecto 1 (valores ya sustituidos)

Todos los valores vienen de [[Parámetros por carné 201905884]]. Copiá cada bloque al README bajo el dispositivo donde lo ejecutaste.

## 1. Identidad y seguridad básica (todos los switches)
```
enable
configure terminal
hostname SW-CORE
banner motd #Acceso Restringido - TechPark_201905884#
```
El `hostname` sigue el rol: `SW-CORE`, `SW-DIST-ID`, `SW-ACC-ALA-A`, etc. El banner es obligatorio en los de distribución.

## 2. VTP
Core (Centro de Datos):
```
vtp mode server
vtp domain Smart_8
vtp password proyecto12S2026
vtp version 2
```
Distribución y acceso del resto del campus:
```
vtp mode client
vtp domain Smart_8
vtp password proyecto12S2026
vtp version 2
```
Switch de Áreas Comunes (aislamiento de administración):
```
vtp mode transparent
vtp domain Smart_8
vtp password proyecto12S2026
```
Antes de conectar un switch nuevo al dominio: `vtp mode transparent` y luego `vtp mode client`, para dejar la revisión en 0 ([[VTP]]).

## 3. VLANs (solo en el Server; el Transparent las crea localmente)
```
vlan 14
 name Gerencia
vlan 24
 name Investigacion
vlan 34
 name Produccion
vlan 44
 name Servidores
vlan 54
 name Visitantes
vlan 94
 name Nativa
```
Mayúsculas del nombre: pendiente en [[Ambigüedades y riesgos del enunciado]].

## 4. Trunks (entre switches), nativa 94 obligatoria
```
interface GigabitEthernet0/1
 description Trunk hacia SW-DIST-ID (fibra)
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 94
 switchport trunk allowed vlan 14,24,34,44,54,94
```
La línea `encapsulation dot1q` solo la aceptan modelos multicapa (3560/3650); en un 2960 se omite.

## 5. Puertos de acceso (PCs, servidores, AP, hub)
```
interface range FastEthernet0/1 - 8
 switchport mode access
 switchport access vlan 24
 spanning-tree portfast
```
`portfast` solo hacia dispositivos finales, nunca hacia otro switch. Puerto hacia el **hub Legacy**, con contención (ver [[Dominios de colisión y broadcast]]):
```
interface FastEthernet0/24
 switchport mode access
 switchport access vlan 34
 storm-control broadcast level 20
 switchport port-security
 switchport port-security maximum 4
 switchport port-security violation restrict
```

## 6. EtherChannel LACP (mismos parámetros en ambos extremos)
```
interface range GigabitEthernet0/1 - 2
 channel-group 1 mode active
 no shutdown
interface Port-channel 1
 switchport mode trunk
 switchport trunk native vlan 94
 switchport trunk allowed vlan 14,24,34,44,54,94
```
Ver [[EtherChannel LACP]].

## 7. STP en modo PVST con Root Bridge elegido
En el Core:
```
spanning-tree mode pvst
spanning-tree vlan 14,34,44,54 root primary
spanning-tree vlan 24 root secondary
```
En el distribuidor de I+D, si decido que sea Root de la 24:
```
spanning-tree vlan 24 root primary
```
Alternativa explícita: `spanning-tree vlan 24 priority 4096`. Ver [[STP y PVST]].

## 8. Verificación (evidencia obligatoria del Manual)
| Comando | Qué demuestra |
|---|---|
| `show vlan brief` | VLANs presentes y puertos asignados (en un Client prueba la propagación VTP) |
| `show vtp status` | Modo, dominio `Smart_8`, revisión, número de VLANs |
| `show interfaces trunk` | Trunks activos, nativa 94, VLANs permitidas |
| `show spanning-tree` | Root Bridge por VLAN, rol/estado de puertos, costos |
| `show etherchannel summary` | Canal `SU`, puertos `P` |
| `show running-config` | Respaldo completo para el README |
| `copy running-config startup-config` | Guardar la configuración |

Volver al [[00 - 🌐 Cerebro Redes (MOC)|MOC]].

> 📚 Fuente: guías Cisco enlazadas en el enunciado §5 (VLAN/Trunks, VTP, STP, EtherChannel) y valores propios del carné.
