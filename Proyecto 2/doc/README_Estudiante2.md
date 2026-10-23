## 8.1 Sede Occidente (Agencia Regional Comercial)

**Dominio de enrutamiento:** EIGRP 100, con un único punto de redistribución hacia OSPF en CORE2.
**Red base:** 10.5.10.0/24.

### Topología

![Topología Occidente](img/10_topologia_occidente.png)

Es una estrella de dos niveles: R-Occidente está sobre el switch de distribución SW-OCC-A0, y de este cuelgan dos switches de acceso, SW-OCC-A1 y SW-OCC-A2, con 8 PCs en total.

### Mapeo lógico

| Rol | Equipo | Detalle |
|-----|--------|---------|
| Router de borde / inter-VLAN | R-Occidente (2911) | Gi0/0 hacia CORE2 (10.5.0.22/30). Gi0/1 es el troncal con las subinterfaces .12, .22, .32 y .42 |
| Switch principal / distribución | SW-OCC-A0 (2960-24TT) | Servidor VTP `bantech05` |
| Switches de acceso | SW-OCC-A1, SW-OCC-A2 (2960-24TT) | Clientes VTP |

| Enlace | Tipo |
|--------|------|
| R-Occidente Gi0/1 ↔ SW-OCC-A0 Gi0/1 | Troncal 802.1Q (straight) |
| SW-OCC-A0 Fa0/1 ↔ SW-OCC-A1 Fa0/1 | Troncal 802.1Q (cross-over) |
| SW-OCC-A0 Fa0/2 ↔ SW-OCC-A2 Fa0/2 | Troncal 802.1Q (cross-over) |
| SW-OCC-A1 Fa0/11-12 / Fa0/13-14 | Acceso VLAN 12 Cajas / VLAN 32 Gerencia |
| SW-OCC-A2 Fa0/11-12 / Fa0/13-14 | Acceso VLAN 22 Asesores / VLAN 42 Seguridad |

### VLANs y direccionamiento (VLSM)

| VLAN | Nombre | Hosts req. | Red | Máscara | Gateway (subinterfaz) | Rango útil | Broadcast |
|------|--------|-----------|-----|---------|------------------------|------------|-----------|
| 12 | Cajas | 45 | 10.5.10.0/26 | 255.255.255.192 | 10.5.10.1 (Gi0/1.12) | .2 – .62 | 10.5.10.63 |
| 22 | Asesores | 30 | 10.5.10.64/26 | 255.255.255.192 | 10.5.10.65 (Gi0/1.22) | .66 – .126 | 10.5.10.127 |
| 42 | Seguridad | 12 | 10.5.10.128/28 | 255.255.255.240 | 10.5.10.129 (Gi0/1.42) | .130 – .142 | 10.5.10.143 |
| 32 | Gerencia | 10 | 10.5.10.144/28 | 255.255.255.240 | 10.5.10.145 (Gi0/1.32) | .146 – .158 | 10.5.10.159 |

Asesores va en un /26: 30 hosts más el gateway suman 31, y un /27 solo da 30 direcciones útiles. Queda libre 10.5.10.160 – 10.5.10.255 para crecer.

| Equipo | Puerto | IP | Gateway |
|--------|--------|----|---------|
| PC-CAJA1, PC-CAJA2 | A1 Fa0/11-12 | 10.5.10.2, .3 /26 | 10.5.10.1 |
| PC-GER1, PC-GER2 | A1 Fa0/13-14 | 10.5.10.146, .147 /28 | 10.5.10.145 |
| PC-ASE1, PC-ASE2 | A2 Fa0/11-12 | 10.5.10.66, .67 /26 | 10.5.10.65 |
| PC-SEG1, PC-SEG2 | A2 Fa0/13-14 | 10.5.10.130, .131 /28 | 10.5.10.129 |

### Justificación

Elegimos una estrella con un switch de distribución porque una agencia comercial necesita, ante todo, una administración sencilla. Las cuatro VLANs se crean una sola vez en SW-OCC-A0, como servidor VTP, y A1 y A2 las aprenden como clientes. Agregar un switch de acceso nuevo es solo un troncal y `vtp mode client`.

La segmentación responde a la necesidad operativa de la sede. Cajas (A1) y Asesores (A2) quedan en switches físicos distintos y en VLANs distintas, así que un bucle, una tormenta de broadcast o una falla de hardware en el área de asesores no llega al dominio de broadcast ni al switch de las cajas. El tráfico entre áreas solo cruza por R-Occidente, que es el punto donde después se pueden aplicar ACLs.

Usamos Router-on-a-Stick porque lo exige el enunciado y porque alcanza para el volumen inter-VLAN de una agencia: la mayor parte del tráfico de Cajas sale hacia el Data Center, no hacia las otras VLANs.

En tolerancia a fallos, perder un switch de acceso afecta solo a sus áreas y no a las de la otra rama. Esta sede prioriza la segmentación sobre la redundancia física, que el enunciado pide para Norte y Oriente.

EIGRP encaja en el papel de "dominio de expansión regional": DUAL converge casi de inmediato y anunciar una agencia nueva es una sola sentencia `network`.

### Extractos de configuración

**R-Occidente**: subinterfaces 802.1Q y EIGRP.
```
interface g0/1.12
 description Cajas
 encapsulation dot1Q 12
 ip address 10.5.10.1 255.255.255.192
interface g0/1.22
 description Asesores
 encapsulation dot1Q 22
 ip address 10.5.10.65 255.255.255.192
! (.32 Gerencia 10.5.10.145/28, .42 Seguridad 10.5.10.129/28)
router eigrp 100
 no auto-summary
 network 10.5.0.20 0.0.0.3
 network 10.5.10.0 0.0.0.255
 passive-interface g0/1.12
 passive-interface g0/1.22
 passive-interface g0/1.32
 passive-interface g0/1.42
```
Los `passive-interface` hacen que EIGRP anuncie las redes de usuario sin enviar hellos hacia las PCs.

**SW-OCC-A0**: servidor VTP y VLANs con nombre.
```
vtp domain bantech05
vtp password cisco
vtp mode server
vlan 12
 name Cajas
vlan 22
 name Asesores
vlan 32
 name Gerencia
vlan 42
 name Seguridad
interface g0/1
 switchport mode trunk
interface fa0/1
 switchport mode trunk
interface fa0/2
 switchport mode trunk
```

**SW-OCC-A1**: cliente VTP y puertos de acceso. SW-OCC-A2 es análogo, con las VLANs 22 y 42.
```
vtp domain bantech05
vtp password cisco
vtp mode client
interface fa0/1
 switchport mode trunk
interface range fa0/11-12
 switchport mode access
 switchport access vlan 12
 spanning-tree portfast
interface range fa0/13-14
 switchport mode access
 switchport access vlan 32
 spanning-tree portfast
```

### Pruebas

**VTP:** A0 está en modo Server y A1 en modo Client, en el mismo dominio `bantech05`, con la misma revisión (8) y el mismo MD5 digest.

![show vtp status](img/11_vtp_status.png)

**VLANs propagadas:** en el cliente SW-OCC-A1 aparecen las 4 VLANs con su nombre sin haberlas creado localmente.

![show vlan brief](img/12_vlan_brief_occ.png)

**Router-on-a-Stick:** las 4 subinterfaces están up/up y cada una es una red conectada.

![R-Occidente subinterfaces](img/10b_roas_roccidente.png)

**Inter-VLAN:** PC-CAJA1 (VLAN 12) hace ping a PC-ASE1 (VLAN 22) y a PC-SEG1 (VLAN 42) con 0 % de pérdida. El TTL=127 confirma que el paquete pasó por R-Occidente.

![Ping Cajas a Asesores](img/14_intervlan_occ.png)

**Redistribución:** la captura `img/13_route_roccidente.png` (`show ip route` con las redes de las otras sedes como `D EX`) se toma con el archivo integrado.

---

## 8.4 Data Center y Sede Central (Alta Seguridad)

**Dominio de enrutamiento:** rutas estáticas. SW-DC-A0 → R-Central2 → R-Central1, y R-Central1 redistribuye a OSPF.
**Red base:** 10.5.40.0/24.

### Topología

![Topología Data Center](img/15_topologia_dc.png)

Es una topología de distribución y acceso: el switch multicapa SW-DC-A0 se enlaza a R-Central2 por un puerto ruteado y a cada switch de acceso por un EtherChannel de 2 cables.

### Mapeo lógico

| Rol | Equipo | Detalle |
|-----|--------|---------|
| Switch principal / distribución (L3) | SW-DC-A0 (3560-24PS) | `ip routing`, SVIs de las VLANs 13, 23 y 33, Gi0/1 ruteado hacia R-Central2 (10.5.0.46/30) |
| Acceso a servidores | SW-DC-A1 (2960-24TT) | Core_BD y Web_Apps |
| Acceso NOC | SW-DC-A2 (2960-24TT) | NOC |

| Enlace | Tipo |
|--------|------|
| SW-DC-A0 Gi0/1 ↔ R-Central2 Gi0/0 | Puerto ruteado (`no switchport`), 10.5.0.44/30 |
| SW-DC-A0 Fa0/1-2 ↔ SW-DC-A1 Fa0/1-2 | Po1: troncal 802.1Q, EtherChannel LACP |
| SW-DC-A0 Fa0/3-4 ↔ SW-DC-A2 Fa0/3-4 | Po2: troncal 802.1Q, EtherChannel LACP |
| SW-DC-A1 Fa0/11-12 / Fa0/13-15 | Acceso VLAN 13 Core_BD / VLAN 23 Web_Apps |
| SW-DC-A2 Fa0/11-13 | Acceso VLAN 33 NOC |

### VLANs y direccionamiento (VLSM)

| VLAN | Nombre | Hosts req. | Red | Máscara | Gateway (SVI) | Rango útil | Broadcast |
|------|--------|-----------|-----|---------|---------------|------------|-----------|
| 23 | Web_Apps | 28 | 10.5.40.0/27 | 255.255.255.224 | 10.5.40.1 | .2 – .30 | 10.5.40.31 |
| 13 | Core_BD | 14 | 10.5.40.32/27 | 255.255.255.224 | 10.5.40.33 | .34 – .62 | 10.5.40.63 |
| 33 | NOC | 10 | 10.5.40.64/28 | 255.255.255.240 | 10.5.40.65 | .66 – .78 | 10.5.40.79 |

Core_BD necesita un /27: 14 hosts más el gateway suman 15, y un /28 solo da 14 direcciones útiles.

| Equipo | Puerto | IP | Gateway |
|--------|--------|----|---------|
| SRV-BD1, SRV-BD2 | A1 Fa0/11-12 | 10.5.40.34, .35 /27 | 10.5.40.33 |
| SRV-WEB1, SRV-WEB2, SRV-WEB3 | A1 Fa0/13-15 | 10.5.40.2, .3, .4 /27 | 10.5.40.1 |
| PC-NOC1, PC-NOC2, PC-NOC3 | A2 Fa0/11-13 | 10.5.40.66, .67, .68 /28 | 10.5.40.65 |

### Justificación

La capa de distribución multicapa saca el enrutamiento inter-VLAN del router: SW-DC-A0 enruta entre Core_BD, Web_Apps y NOC por hardware, con sus SVIs, sin el cuello de botella de un único troncal hacia un router. El tráfico servidor-servidor, como Web_Apps consultando Core_BD, nunca sale del switch.

La necesidad operativa es absorber ráfagas masivas de tráfico, y por eso cada switch de acceso se conecta con un EtherChannel LACP (IEEE 802.3ad) de 2 enlaces. Así se suma el ancho de banda y el balanceo reparte los flujos entre los miembros.

En tolerancia a fallos, si un cable del canal cae, el Port-channel sigue arriba con el otro miembro: no hay reconvergencia de STP ni pérdida de servicio. Elegimos LACP en lugar de PAgP porque es un estándar abierto.

La seguridad se resuelve con enrutamiento estático. SW-DC-A0 solo tiene una ruta por defecto hacia R-Central2, y ningún protocolo dinámico anuncia ni aprende rutas dentro del segmento. Lo que el resto de la red conoce del Data Center son exactamente las 3 redes que R-Central1 redistribuye a OSPF.

### Extractos de configuración

**SW-DC-A0**: SVIs, EtherChannel y ruta por defecto.
```
ip routing
vlan 13
 name Core_BD
vlan 23
 name Web_Apps
vlan 33
 name NOC
interface g0/1
 no switchport
 ip address 10.5.0.46 255.255.255.252
interface range fa0/1-2
 switchport trunk encapsulation dot1q
 switchport mode trunk
 channel-group 1 mode active
interface range fa0/3-4
 switchport trunk encapsulation dot1q
 switchport mode trunk
 channel-group 2 mode active
interface vlan 13
 ip address 10.5.40.33 255.255.255.224
interface vlan 23
 ip address 10.5.40.1 255.255.255.224
interface vlan 33
 ip address 10.5.40.65 255.255.255.240
ip route 0.0.0.0 0.0.0.0 10.5.0.45
```

**SW-DC-A1**: extremo LACP de Po1 y accesos. SW-DC-A2 es análogo, con Po2 en Fa0/3-4 y la VLAN 33.
```
interface range fa0/1-2
 switchport mode trunk
 channel-group 1 mode active
interface range fa0/11-12
 switchport mode access
 switchport access vlan 13
 spanning-tree portfast
interface range fa0/13-15
 switchport mode access
 switchport access vlan 23
 spanning-tree portfast
```

### Pruebas

**EtherChannel:** Po1 y Po2 están en `(SU)` (capa 2, en uso), con protocolo LACP y ambos miembros en `(P)`.

![show etherchannel summary](img/16_etherchannel_dc.png)

**Troncales e inter-VLAN:** los Port-channel están trunking con las VLANs 13, 23 y 33 activas, y las tres SVIs son redes conectadas.

![Troncales y SVIs](img/15b_svi_trunk_dc.png)

**Failover del EtherChannel:** con `shutdown` en SW-DC-A0 Fa0/1, el miembro queda en `(D)` pero Po1 sigue `(SU)` con Fa0/2. A la izquierda se ve el estado del canal, y a la derecha PC-NOC1 (VLAN 33) llegando a SRV-BD1 (VLAN 13) con 0 % de pérdida por el miembro que queda.

![Failover EtherChannel](img/17_failover_etherchannel_dc.png)
