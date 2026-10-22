# Sede Norte y Sede Oriente

## Sede Norte, Centro de Autorización de Créditos

### Topología

![Topología Norte](img/18_topologia_norte.png)

Dominio de enrutamiento: OSPF área 0.

Equipos de la sede:

| Equipo    | Modelo             | Función                                            |
| --------- | ------------------ | -------------------------------------------------- |
| R-Norte   | ISR 2911           | Router de borde e inter-VLAN con Router-on-a-Stick |
| SW-NOR-A0 | Catalyst 2960-24TT | Switch principal y Root Bridge                     |
| SW-NOR-A1 | Catalyst 2960-24TT | Acceso y raíz secundaria                           |
| SW-NOR-A2 | Catalyst 2960-24TT | Acceso                                             |
| 8 PCs     | PC-PT              | Dispositivos finales                               |

### Tabla de VLANs

| ID  | Nombre    | Área funcional      | Hosts requeridos |
| --- | --------- | ------------------- | ---------------- |
| 52  | Analisis  | Analistas de Riesgo | 50               |
| 62  | Auditoria | Revisión de cuentas | 25               |
| 72  | Legal     | Contratos           | 14               |

### Subnetting VLSM sobre el bloque 10.5.20.0/24

Criterio: a los hosts requeridos se les suma una IP para el gateway. Los bloques se asignan de mayor a menor.

| VLAN         | Necesarias | Prefijo                      | Red        | Gateway    | Rango de hosts           | Broadcast   |
| ------------ | ---------- | ---------------------------- | ---------- | ---------- | ------------------------ | ----------- |
| 52 Analisis  | 51         | /26, máscara 255.255.255.192 | 10.5.20.0  | 10.5.20.1  | 10.5.20.2 a 10.5.20.62   | 10.5.20.63  |
| 62 Auditoria | 26         | /27, máscara 255.255.255.224 | 10.5.20.64 | 10.5.20.65 | 10.5.20.66 a 10.5.20.94  | 10.5.20.95  |
| 72 Legal     | 15         | /27, máscara 255.255.255.224 | 10.5.20.96 | 10.5.20.97 | 10.5.20.98 a 10.5.20.126 | 10.5.20.127 |

### Enlaces punto a punto hacia el backbone

| Enlace                         | Red          | Extremo A       | Extremo B         | Dominio |
| ------------------------------ | ------------ | --------------- | ----------------- | ------- |
| CORE1 g1/0/10 con R-Norte g0/0 | 10.5.0.12/30 | CORE1 10.5.0.13 | R-Norte 10.5.0.14 | OSPF    |
| CORE2 g1/0/10 con R-Norte g0/1 | 10.5.0.16/30 | CORE2 10.5.0.17 | R-Norte 10.5.0.18 | OSPF    |

### Dispositivos finales

| PC                | Switch y puerto           | VLAN | IP                      | Máscara         | Gateway    |
| ----------------- | ------------------------- | ---- | ----------------------- | --------------- | ---------- |
| PC-ANA1 y PC-ANA2 | SW-NOR-A1 Fa0/11 y Fa0/12 | 52   | 10.5.20.2 y 10.5.20.3   | 255.255.255.192 | 10.5.20.1  |
| PC-AUD1 y PC-AUD2 | SW-NOR-A1 Fa0/13 y Fa0/14 | 62   | 10.5.20.66 y 10.5.20.67 | 255.255.255.224 | 10.5.20.65 |
| PC-ANA3 y PC-ANA4 | SW-NOR-A2 Fa0/11 y Fa0/12 | 52   | 10.5.20.4 y 10.5.20.5   | 255.255.255.192 | 10.5.20.1  |
| PC-LEG1 y PC-LEG2 | SW-NOR-A2 Fa0/13 y Fa0/14 | 72   | 10.5.20.98 y 10.5.20.99 | 255.255.255.224 | 10.5.20.97 |

### Mapeo lógico

Switch principal: SW-NOR-A0, configurado como Root Bridge.

Enlaces troncales 802.1Q:

| Enlace                  | Puertos                                         |
| ----------------------- | ----------------------------------------------- |
| R-Norte con SW-NOR-A0   | g0/2 con Gi0/1                                  |
| SW-NOR-A0 con SW-NOR-A1 | Fa0/1 con Fa0/1                                 |
| SW-NOR-A0 con SW-NOR-A2 | Fa0/2 con Fa0/2                                 |
| SW-NOR-A1 con SW-NOR-A2 | Fa0/3 con Fa0/3, enlace que cierra el triángulo |

Puertos de acceso: Fa0/11 a Fa0/14 en SW-NOR-A1 y en SW-NOR-A2.

Enrutamiento inter-VLAN: Router-on-a-Stick en R-Norte, con las subinterfaces g0/2.52, g0/2.62 y g0/2.72.

### Justificación de la arquitectura

La sede Norte concentra a los analistas de riesgo, y de su disponibilidad depende que los créditos de todo el país puedan aprobarse. Por eso se eligió un triángulo de tres switches, que introduce bucles físicos de forma intencional. Cada switch de acceso tiene dos caminos hacia SW-NOR-A0, uno directo y otro a través del switch vecino, de modo que ningún cable ni ningún switch de acceso es un punto único de falla. Rapid PVST+ mantiene bloqueado un solo puerto, SW-NOR-A2 Fa0/3, para evitar tormentas de broadcast, y lo habilita en segundos si falla un enlace activo. SW-NOR-A0 se forzó como Root Bridge con prioridad 24576 porque es el switch al que se conecta R-Norte, así el tráfico hacia el gateway sigue siempre el camino más corto. SW-NOR-A1 quedó como raíz secundaria con prioridad 28672, de modo que si A0 falla el reemplazo es predecible y no queda al azar de las direcciones MAC.

Se usó Router-on-a-Stick porque los switches son de capa 2 y un único enlace troncal es suficiente para el tráfico entre las tres VLANs de una sede de este tamaño. La sede se asignó al dominio OSPF porque es la más crítica del corporativo. Al estar en el mismo dominio que el núcleo no depende de redistribución, y sus dos salidas hacia CORE1 y CORE2 convergen con rapidez gracias al enrutamiento por estado de enlace.

### Configuraciones clave

Los archivos completos de cada equipo están en la carpeta `configs`.

Las VLANs se crean en SW-NOR-A0, SW-NOR-A1 y SW-NOR-A2. No aparecen en la salida de `show running-config` porque Packet Tracer las guarda en el archivo `vlan.dat`.

```
vlan 52
 name Analisis
vlan 62
 name Auditoria
vlan 72
 name Legal
```

SW-NOR-A0, Root Bridge:

```
hostname SW-NOR-A0
spanning-tree mode rapid-pvst
spanning-tree vlan 52,62,72 priority 24576
interface FastEthernet0/1
 description Troncal hacia SW-NOR-A1
 switchport mode trunk
interface FastEthernet0/2
 description Troncal hacia SW-NOR-A2
 switchport mode trunk
interface GigabitEthernet0/1
 description Troncal hacia R-Norte
 switchport mode trunk
```

El comando aplicado fue `spanning-tree vlan 52,62,72 root primary`, que IOS guarda como prioridad 24576.

SW-NOR-A1, raíz secundaria:

```
hostname SW-NOR-A1
spanning-tree mode rapid-pvst
spanning-tree vlan 52,62,72 priority 28672
interface FastEthernet0/1
 description Troncal hacia SW-NOR-A0
 switchport mode trunk
interface FastEthernet0/3
 description Troncal hacia SW-NOR-A2
 switchport mode trunk
interface range FastEthernet0/11-12
 switchport mode access
 switchport access vlan 52
 spanning-tree portfast
interface range FastEthernet0/13-14
 switchport mode access
 switchport access vlan 62
 spanning-tree portfast
```

El comando aplicado fue `spanning-tree vlan 52,62,72 root secondary`, que IOS guarda como prioridad 28672.

SW-NOR-A2, acceso:

```
hostname SW-NOR-A2
spanning-tree mode rapid-pvst
interface FastEthernet0/2
 description Troncal hacia SW-NOR-A0
 switchport mode trunk
interface FastEthernet0/3
 description Troncal hacia SW-NOR-A1
 switchport mode trunk
interface range FastEthernet0/11-12
 switchport mode access
 switchport access vlan 52
 spanning-tree portfast
interface range FastEthernet0/13-14
 switchport mode access
 switchport access vlan 72
 spanning-tree portfast
```

R-Norte, Router-on-a-Stick y OSPF:

```
hostname R-Norte
interface GigabitEthernet0/0
 description Hacia CORE1 g1/0/10
 ip address 10.5.0.14 255.255.255.252
interface GigabitEthernet0/1
 description Hacia CORE2 g1/0/10
 ip address 10.5.0.18 255.255.255.252
interface GigabitEthernet0/2
 description Troncal hacia SW-NOR-A0
interface GigabitEthernet0/2.52
 description Analisis
 encapsulation dot1Q 52
 ip address 10.5.20.1 255.255.255.192
interface GigabitEthernet0/2.62
 description Auditoria
 encapsulation dot1Q 62
 ip address 10.5.20.65 255.255.255.224
interface GigabitEthernet0/2.72
 description Legal
 encapsulation dot1Q 72
 ip address 10.5.20.97 255.255.255.224
router ospf 1
 router-id 4.4.4.4
 passive-interface GigabitEthernet0/2.52
 passive-interface GigabitEthernet0/2.62
 passive-interface GigabitEthernet0/2.72
 network 10.5.0.12 0.0.0.3 area 0
 network 10.5.0.16 0.0.0.3 area 0
 network 10.5.20.0 0.0.0.255 area 0
```

### Pruebas

Enrutamiento inter-VLAN. Los pings entre VLANs distintas responden con TTL 127, lo que confirma que el tráfico atraviesa R-Norte. El primer paquete se pierde mientras se resuelve el ARP y los siguientes responden sin pérdida.

Root Bridge. SW-NOR-A0 es la raíz de la VLAN 52 con prioridad 24628, que resulta de sumar 24576 y el número de VLAN.

![Root Bridge en SW-NOR-A0](img/19_stp_root.png)

Puerto bloqueado. En SW-NOR-A2 el puerto Fa0/2 es el puerto raíz y Fa0/3 queda en estado Altn BLK, que corresponde al enlace entre SW-NOR-A1 y SW-NOR-A2.

![Puerto bloqueado en SW-NOR-A2](img/20_stp_bloqueado.png)

Conmutación por error de STP. Con un ping continuo desde PC-ANA1 hacia el gateway 10.5.20.1 se apagó la interfaz Fa0/1 de SW-NOR-A0. El puerto bloqueado pasó a reenviar tráfico y el ping se recuperó después de 2 tiempos de espera agotados.

![Failover de STP](img/21_failover_stp.png)

## Sede Oriente, Centro Financiero Legado

### Topología

![Topología Oriente](img/22_topologia_oriente.png)

Dominio de enrutamiento: RIPv2.

Equipos de la sede:

| Equipo    | Modelo             | Función                                            |
| --------- | ------------------ | -------------------------------------------------- |
| MS1       | Catalyst 3560-24PS | Switch multicapa, HSRP activo y Root Bridge        |
| MS2       | Catalyst 3560-24PS | Switch multicapa, HSRP en espera y raíz secundaria |
| SW-ORI-A1 | Catalyst 2960-24TT | Acceso de la VLAN Boveda                           |
| SW-ORI-A2 | Catalyst 2960-24TT | Acceso de la VLAN Plataforma                       |
| 8 PCs     | PC-PT              | Dispositivos finales                               |

### Tabla de VLANs

| ID  | Nombre     | Área funcional         | Hosts requeridos |
| --- | ---------- | ---------------------- | ---------------- |
| 82  | Boveda     | Operaciones de valores | 40               |
| 92  | Plataforma | Atención VIP           | 60               |

### Subnetting VLSM sobre el bloque 10.5.30.0/24

Criterio: a los hosts requeridos se les suman tres IPs de HSRP, que son la virtual, la de MS1 y la de MS2.

| VLAN          | Necesarias | Prefijo                      | Red         | IP virtual  | MS1         | MS2         | Rango de hosts            | Broadcast   |
| ------------- | ---------- | ---------------------------- | ----------- | ----------- | ----------- | ----------- | ------------------------- | ----------- |
| 92 Plataforma | 63         | /25, máscara 255.255.255.128 | 10.5.30.0   | 10.5.30.1   | 10.5.30.2   | 10.5.30.3   | 10.5.30.4 a 10.5.30.126   | 10.5.30.127 |
| 82 Boveda     | 43         | /26, máscara 255.255.255.192 | 10.5.30.128 | 10.5.30.129 | 10.5.30.130 | 10.5.30.131 | 10.5.30.132 a 10.5.30.190 | 10.5.30.191 |

La VLAN Plataforma necesita un /25 porque 60 hosts más 3 IPs de HSRP suman 63, que supera los 62 utilizables de un /26.

### Enlaces punto a punto hacia el backbone

| Enlace                     | Red          | Extremo A       | Extremo B     | Dominio |
| -------------------------- | ------------ | --------------- | ------------- | ------- |
| CORE3 g1/0/12 con MS1 g0/1 | 10.5.0.24/30 | CORE3 10.5.0.25 | MS1 10.5.0.26 | RIPv2   |
| CORE3 g1/0/13 con MS2 g0/1 | 10.5.0.28/30 | CORE3 10.5.0.29 | MS2 10.5.0.30 | RIPv2   |

### Dispositivos finales

El gateway de todas las PCs es la IP virtual de HSRP.

| PC                | Switch y puerto           | VLAN | IP                        | Máscara         | Gateway     |
| ----------------- | ------------------------- | ---- | ------------------------- | --------------- | ----------- |
| PC-BOV1 a PC-BOV4 | SW-ORI-A1 Fa0/11 a Fa0/14 | 82   | 10.5.30.132 a 10.5.30.135 | 255.255.255.192 | 10.5.30.129 |
| PC-PLA1 a PC-PLA4 | SW-ORI-A2 Fa0/11 a Fa0/14 | 92   | 10.5.30.4 a 10.5.30.7     | 255.255.255.128 | 10.5.30.1   |

### Mapeo lógico

Switches principales: MS1 como activo y MS2 como respaldo.

Enlaces troncales 802.1Q:

| Enlace               | Puertos         |
| -------------------- | --------------- |
| MS1 con MS2, cascada | Gi0/2 con Gi0/2 |
| MS1 con SW-ORI-A1    | Fa0/1 con Fa0/1 |
| MS2 con SW-ORI-A1    | Fa0/2 con Fa0/2 |
| MS1 con SW-ORI-A2    | Fa0/3 con Fa0/3 |
| MS2 con SW-ORI-A2    | Fa0/4 con Fa0/4 |

Enlaces ruteados: MS1 Gi0/1 y MS2 Gi0/1 hacia CORE3.

Puertos de acceso: Fa0/11 a Fa0/14 en SW-ORI-A1 y en SW-ORI-A2.

Enrutamiento inter-VLAN: interfaces virtuales Vlan82 y Vlan92 en MS1 y MS2, que cuentan con `ip routing` habilitado.

### Justificación de la arquitectura

El Centro Financiero Legado es una sede crítica cuyos usuarios no pueden perder conectividad hacia el núcleo, incluso si MS1 sufre un corte de energía. Para cumplirlo, cada switch de acceso se conecta de forma simultánea a MS1 y a MS2, de manera que ni la capa 2 ni la capa 3 dependen de un solo equipo. MS1 y MS2 también se conectan entre sí por un enlace troncal en cascada, y cada uno tiene su propio enlace ruteado hacia CORE3, lo que da dos salidas independientes hacia el backbone.

Se eligió HSRP porque es el protocolo nativo de Cisco, está soportado por Packet Tracer y es el que pide la rúbrica. Cada VLAN tiene una IP virtual que las PCs usan como gateway, por lo que si MS1 falla, MS2 asume el rol activo sin que haya que cambiar nada en los equipos finales. MS1 tiene prioridad 110 y preempt, así recupera el rol cuando regresa. Además, MS1 es el Root Bridge de Rapid PVST+ con prioridad 24576, alineado con su rol de gateway activo, y así el camino de capa 2 coincide con el de capa 3 y se evitan rutas subóptimas. MS2 es la raíz secundaria con prioridad 28672.

La sede se asignó al dominio RIPv2 por ser la red legada del banco adquirido. De esa forma se integra al corporativo sin migrarla de inmediato, y queda aislada detrás del punto de redistribución del backbone.

### Configuraciones clave

Los archivos completos de cada equipo están en la carpeta `configs`.

Las VLANs se crean en MS1, MS2, SW-ORI-A1 y SW-ORI-A2. No aparecen en la salida de `show running-config` porque Packet Tracer las guarda en el archivo `vlan.dat`.

```
vlan 82
 name Boveda
vlan 92
 name Plataforma
```

MS1, HSRP activo y Root Bridge:

```
hostname MS1
ip routing
spanning-tree mode rapid-pvst
spanning-tree vlan 82,92 priority 24576
interface GigabitEthernet0/1
 description Enlace ruteado hacia CORE3 g1/0/12
 no switchport
 ip address 10.5.0.26 255.255.255.252
interface GigabitEthernet0/2
 description Cascada hacia MS2
 switchport trunk encapsulation dot1q
 switchport mode trunk
interface FastEthernet0/1
 description Troncal hacia SW-ORI-A1
 switchport trunk encapsulation dot1q
 switchport mode trunk
interface FastEthernet0/3
 description Troncal hacia SW-ORI-A2
 switchport trunk encapsulation dot1q
 switchport mode trunk
interface Vlan82
 ip address 10.5.30.130 255.255.255.192
 standby 82 ip 10.5.30.129
 standby 82 priority 110
 standby 82 preempt
interface Vlan92
 ip address 10.5.30.2 255.255.255.128
 standby 92 ip 10.5.30.1
 standby 92 priority 110
 standby 92 preempt
router rip
 version 2
 network 10.0.0.0
 no auto-summary
```

MS2, HSRP en espera y raíz secundaria:

```
hostname MS2
ip routing
spanning-tree mode rapid-pvst
spanning-tree vlan 82,92 priority 28672
interface GigabitEthernet0/1
 description Enlace ruteado hacia CORE3 g1/0/13
 no switchport
 ip address 10.5.0.30 255.255.255.252
interface GigabitEthernet0/2
 description Cascada hacia MS1
 switchport trunk encapsulation dot1q
 switchport mode trunk
interface FastEthernet0/2
 description Troncal hacia SW-ORI-A1
 switchport trunk encapsulation dot1q
 switchport mode trunk
interface FastEthernet0/4
 description Troncal hacia SW-ORI-A2
 switchport trunk encapsulation dot1q
 switchport mode trunk
interface Vlan82
 ip address 10.5.30.131 255.255.255.192
 standby 82 ip 10.5.30.129
 standby 82 preempt
interface Vlan92
 ip address 10.5.30.3 255.255.255.128
 standby 92 ip 10.5.30.1
 standby 92 preempt
router rip
 version 2
 network 10.0.0.0
 no auto-summary
```

En MS2 no aparece la línea de prioridad de HSRP porque su valor es 100, que es el predeterminado.

SW-ORI-A1, acceso de Boveda:

```
hostname SW-ORI-A1
spanning-tree mode rapid-pvst
interface FastEthernet0/1
 description Uplink hacia MS1
 switchport mode trunk
interface FastEthernet0/2
 description Uplink hacia MS2
 switchport mode trunk
interface range FastEthernet0/11-14
 switchport mode access
 switchport access vlan 82
 spanning-tree portfast
```

SW-ORI-A2, acceso de Plataforma:

```
hostname SW-ORI-A2
spanning-tree mode rapid-pvst
interface FastEthernet0/3
 description Uplink hacia MS1
 switchport mode trunk
interface FastEthernet0/4
 description Uplink hacia MS2
 switchport mode trunk
interface range FastEthernet0/11-14
 switchport mode access
 switchport access vlan 92
 spanning-tree portfast
```

### Pruebas

Estado de HSRP antes de la falla. MS1 está en estado Active con prioridad 110 y MS2 en estado Standby con prioridad 100, en las VLANs 82 y 92. La IP virtual es 10.5.30.129 para Boveda y 10.5.30.1 para Plataforma.

![Estado de HSRP antes de la falla](img/23_hsrp_antes.png)

Enrutamiento inter-VLAN y gateways virtuales. El ping de una PC de Boveda hacia una de Plataforma responde con TTL 127, y los pings a las IPs virtuales 10.5.30.129 y 10.5.30.1 responden con TTL 255 y sin pérdida.

Conmutación por error de HSRP. Con un ping continuo desde PC-PLA1 hacia PC-BOV1 en 10.5.30.132, que cruza el gateway, se simuló el corte de MS1 apagando sus interfaces Fa0/1, Fa0/3 y Gi0/2. El ping se recuperó después de 4 tiempos de espera agotados y MS2 asumió el rol Active. Al restaurar los enlaces, MS1 recuperó el rol Active gracias a preempt, como lo muestran los mensajes de cambio de estado de HSRP en las VLANs 82 y 92.

![Failover de HSRP](img/24_failover_hsrp.png)
