# Guía Maestra – Proyecto 2: Infraestructura Financiera y Alta Disponibilidad BanTech GT

Redes de Computadoras 1 – Segundo Semestre 2026 – Grupo 2

---

## 0. Parámetros del grupo

- Coordinador: Fabio Hernández, carnet 201801005 → **XX = 05**
- Número de grupo: 2 → **Y = 2**
- VTP (solo Occidente): dominio `bantech05`, password `cisco`
- Red base: **10.5.0.0/16** con VLSM (un bloque /24 por sede, /30 para enlaces punto a punto)
- Dispositivos finales: mínimo 7 **por sede** (el diseño usa 8 por sede)
- Fecha límite de elaboración: viernes 23/10/2026. Calificación: sábado 24/10/2026

### Tabla de VLANs

| ID | Nombre | Sede | Hosts requeridos |
|----|--------|------|------------------|
| 12 | Cajas | Occidente | 45 |
| 22 | Asesores | Occidente | 30 |
| 32 | Gerencia | Occidente | 10 |
| 42 | Seguridad | Occidente | 12 |
| 52 | Analisis | Norte | 50 |
| 62 | Auditoria | Norte | 25 |
| 72 | Legal | Norte | 14 |
| 82 | Boveda | Oriente | 40 |
| 92 | Plataforma | Oriente | 60 |
| 13 | Core_BD | Data Center | 14 |
| 23 | Web_Apps | Data Center | 28 |
| 33 | NOC | Data Center | 10 |

Los nombres van sin tildes para evitar problemas en IOS.

---

## 1. Reparto de labores y cronograma

Modelo de trabajo: cada integrante construye su bloque en su propio archivo .pkt, con **todas las IPs de esta guía** (incluidas las interfaces que miran al backbone). Al final, Fabio copia y pega cada bloque en el archivo maestro y solo conecta los cables de integración.

### Estudiante 1 – Fabio (coordinador): Backbone + integración

- Crear el repositorio y su estructura (ver sección 11).
- **Primera tarea (domingo o lunes temprano):** verificar que el 3650-24PS acepta el módulo de fibra GLC-LH-SMD (ver sección 10). Todo el núcleo depende de eso.
- Construir el archivo maestro con:
  - CORE1, CORE2 y CORE3, con los 3 EtherChannel L3 (Po1 en fibra) y OSPF área 0.
  - Puntos de redistribución en CORE2 (OSPF↔EIGRP) y CORE3 (OSPF↔RIPv2).
  - R-Central1 y R-Central2: enlace serial, rutas estáticas y redistribución de estáticas a OSPF.
- Integrar los bloques de los estudiantes 2 y 3, y colocar las etiquetas de dominio en la topología.
- Capturas de `show ip route` de los routers frontera y pings extremo a extremo.
- Consolidar el README final y hacer la entrega.

### Estudiante 2: Sede Occidente + Data Center

- **Occidente:** R-Occidente con Router-on-a-Stick y EIGRP, 3 switches, VTP, VLANs con nombre y 8 PCs.
- **Data Center:** SW-DC-A0 (3560, inter-VLAN y ruta estática por defecto), SW-DC-A1 y SW-DC-A2 con EtherChannel LACP, y 8 dispositivos finales.
- Capturas de VTP, EtherChannel, inter-VLAN y redacción de sus secciones del README.

### Estudiante 3: Sede Norte + Sede Oriente

- **Norte:** R-Norte con Router-on-a-Stick y OSPF, triángulo de 3 switches, Rapid PVST+, Root Bridge forzado y 8 PCs.
- **Oriente:** MS1 y MS2 (SVIs, HSRP, RIPv2, Rapid PVST+), 2 switches de acceso conectados a ambos y 8 PCs.
- Capturas de STP, HSRP, failover y redacción de sus secciones del README.

### Cronograma

- **Dom 18 (noche) – Mar 20:** construcción en paralelo. Cada quien su .pkt, más un .txt con la configuración de cada equipo en `configs/`.
- **Mar 20 (noche):** todos hacen `wr` en cada equipo y suben su .pkt y sus .txt al repo.
- **Mié 21:** Fabio integra en el archivo maestro. Los demás quedan disponibles para depurar su bloque.
- **Jue 22:** pruebas de convergencia y failover, y capturas (cada quien las de su bloque).
- **Vie 23:** cada quien sube su sección del README con commits propios. Fabio consolida, revisa y entrega.

Regla de oro: los tres deben usar **exactamente la misma versión de Packet Tracer**.

---

## 2. Arquitectura general

```
                            [R-Norte]  (OSPF área 0)
                             g0/0   g0/1
                              |       |
                      g1/0/10 |       | g1/0/10
 [R-Central1]g0/0---g1/0/14[CORE1]==Po1 FIBRA==[CORE2]g1/0/11---g0/0[R-Occidente]
   |    g0/1                  \\               //                  (EIGRP 100)
   |      \                Po2 \\             // Po3
 Se0/0/0   \------------g1/0/14[    CORE3    ]
 (serial)                     g1/0/12   g1/0/13
   |                             |         |
 Se0/0/0                       g0/1      g0/1
 [R-Central2]                  [MS1]=====[MS2]   (RIPv2 + HSRP)
   | g0/0                        \\       //
   | g0/1                      SW-ORI-A1  SW-ORI-A2
 [SW-DC-A0] (estáticas)
   ||Po1  ||Po2
 SW-DC-A1  SW-DC-A2
```

### Dominios de enrutamiento

- **OSPF área 0:** CORE1, CORE2, CORE3, R-Norte y R-Central1. Es el dominio principal del núcleo transaccional.
- **EIGRP 100:** R-Occidente y la interfaz de CORE2 hacia él (expansión regional).
- **RIPv2:** MS1, MS2 y las interfaces de CORE3 hacia ellos (red legada).
- **Rutas estáticas:** R-Central2 y SW-DC-A0. Es el segmento de alta seguridad, sin protocolos dinámicos.

### Puntos de redistribución (3; el enunciado pide al menos 2)

1. **CORE2:** OSPF ↔ EIGRP (mutua)
2. **CORE3:** OSPF ↔ RIPv2 (mutua)
3. **R-Central1:** estáticas → OSPF

Cada dominio externo tiene **un solo** punto de redistribución. Así se evitan bucles de enrutamiento por redistribución mutua en varios puntos.

### Medios físicos

- **Fibra óptica:** Po1 CORE1↔CORE2 (2 enlaces con GLC-LH-SMD)
- **Ethernet:** el resto de enlaces del núcleo y de las sedes
- **Serial:** R-Central1↔R-Central2 (enlace WAN hacia el segmento de alta seguridad)

---

## 3. Inventario de equipos

| Hostname | Modelo PT | Módulos / notas | Responsable |
|----------|-----------|-----------------|-------------|
| CORE1, CORE2 | Catalyst 3650-24PS | AC-POWER-SUPPLY + 2x GLC-LH-SMD (Gi1/1/1-2) | Fabio |
| CORE3 | Catalyst 3650-24PS | AC-POWER-SUPPLY | Fabio |
| R-Central1, R-Central2 | ISR 2911 | HWIC-2T (serial) | Fabio |
| R-Occidente | ISR 2911 | – | Estudiante 2 |
| SW-OCC-A0, A1, A2 | Catalyst 2960-24TT | – | Estudiante 2 |
| SW-DC-A0 | Catalyst 3560-24PS | – | Estudiante 2 |
| SW-DC-A1, A2 | Catalyst 2960-24TT | – | Estudiante 2 |
| R-Norte | ISR 2911 | – | Estudiante 3 |
| SW-NOR-A0, A1, A2 | Catalyst 2960-24TT | – | Estudiante 3 |
| MS1, MS2 | Catalyst 3560-24PS | – | Estudiante 3 |
| SW-ORI-A1, A2 | Catalyst 2960-24TT | – | Estudiante 3 |

Dispositivos finales: 8 PCs en Occidente, 8 en Norte y 8 en Oriente. En el Data Center, 5 Server-PT más 3 PCs del NOC.

Convención de nombres: el switch principal de cada sede termina en -A0 y los de acceso en -A1, -A2. En Oriente los principales son MS1 y MS2.

Convención de cableado: dentro de cada sede, todo enlace entre switches usa el mismo número de puerto en ambos extremos.

---

## 4. Plan de direccionamiento (VLSM)

Criterio: a los hosts requeridos se les suma el gateway (y en Oriente las 3 IPs de HSRP: virtual, MS1 y MS2). Se ordena de mayor a menor dentro del bloque de cada sede.

### Asignación de bloques

| Bloque | Uso |
|--------|-----|
| 10.5.0.0/24 | Enlaces punto a punto (/30) |
| 10.5.10.0/24 | Sede Occidente |
| 10.5.20.0/24 | Sede Norte |
| 10.5.30.0/24 | Sede Oriente |
| 10.5.40.0/24 | Data Center y Sede Central |

### Occidente – 10.5.10.0/24

| VLAN | Nombre | Req. | Necesarias | Prefijo | Red | Gateway | Rango hosts | Broadcast |
|------|--------|------|-----------|---------|-----|---------|-------------|-----------|
| 12 | Cajas | 45 | 46 | /26 (255.255.255.192) | 10.5.10.0 | 10.5.10.1 | .2 – .62 | 10.5.10.63 |
| 22 | Asesores | 30 | 31 | /26 (255.255.255.192) | 10.5.10.64 | 10.5.10.65 | .66 – .126 | 10.5.10.127 |
| 42 | Seguridad | 12 | 13 | /28 (255.255.255.240) | 10.5.10.128 | 10.5.10.129 | .130 – .142 | 10.5.10.143 |
| 32 | Gerencia | 10 | 11 | /28 (255.255.255.240) | 10.5.10.144 | 10.5.10.145 | .146 – .158 | 10.5.10.159 |

Asesores necesita /26 porque 30 hosts más el gateway (31) no caben en un /27 (30 utilizables). Libre para crecimiento: 10.5.10.160 – 10.5.10.255.

### Norte – 10.5.20.0/24

| VLAN | Nombre | Req. | Necesarias | Prefijo | Red | Gateway | Rango hosts | Broadcast |
|------|--------|------|-----------|---------|-----|---------|-------------|-----------|
| 52 | Analisis | 50 | 51 | /26 (255.255.255.192) | 10.5.20.0 | 10.5.20.1 | .2 – .62 | 10.5.20.63 |
| 62 | Auditoria | 25 | 26 | /27 (255.255.255.224) | 10.5.20.64 | 10.5.20.65 | .66 – .94 | 10.5.20.95 |
| 72 | Legal | 14 | 15 | /27 (255.255.255.224) | 10.5.20.96 | 10.5.20.97 | .98 – .126 | 10.5.20.127 |

### Oriente – 10.5.30.0/24

| VLAN | Nombre | Req. | Necesarias | Prefijo | Red | IP virtual (gateway) | MS1 | MS2 | Rango hosts | Broadcast |
|------|--------|------|-----------|---------|-----|---------------------|-----|-----|-------------|-----------|
| 92 | Plataforma | 60 | 63 | /25 (255.255.255.128) | 10.5.30.0 | 10.5.30.1 | .2 | .3 | .4 – .126 | 10.5.30.127 |
| 82 | Boveda | 40 | 43 | /26 (255.255.255.192) | 10.5.30.128 | 10.5.30.129 | .130 | .131 | .132 – .190 | 10.5.30.191 |

Plataforma necesita /25 porque 60 hosts más 3 IPs de HSRP (63) superan los 62 utilizables de un /26.

### Data Center – 10.5.40.0/24

| VLAN | Nombre | Req. | Necesarias | Prefijo | Red | Gateway | Rango hosts | Broadcast |
|------|--------|------|-----------|---------|-----|---------|-------------|-----------|
| 23 | Web_Apps | 28 | 29 | /27 (255.255.255.224) | 10.5.40.0 | 10.5.40.1 | .2 – .30 | 10.5.40.31 |
| 13 | Core_BD | 14 | 15 | /27 (255.255.255.224) | 10.5.40.32 | 10.5.40.33 | .34 – .62 | 10.5.40.63 |
| 33 | NOC | 10 | 11 | /28 (255.255.255.240) | 10.5.40.64 | 10.5.40.65 | .66 – .78 | 10.5.40.79 |

### Enlaces punto a punto – 10.5.0.0/24 (/30, máscara 255.255.255.252)

| # | Enlace | Red | Extremo A | Extremo B | Dominio |
|---|--------|-----|-----------|-----------|---------|
| 1 | CORE1 Po1 – CORE2 Po1 (fibra) | 10.5.0.0/30 | CORE1 .1 | CORE2 .2 | OSPF |
| 2 | CORE1 Po2 – CORE3 Po2 | 10.5.0.4/30 | CORE1 .5 | CORE3 .6 | OSPF |
| 3 | CORE2 Po3 – CORE3 Po3 | 10.5.0.8/30 | CORE2 .9 | CORE3 .10 | OSPF |
| 4 | CORE1 g1/0/10 – R-Norte g0/0 | 10.5.0.12/30 | CORE1 .13 | R-Norte .14 | OSPF |
| 5 | CORE2 g1/0/10 – R-Norte g0/1 | 10.5.0.16/30 | CORE2 .17 | R-Norte .18 | OSPF |
| 6 | CORE2 g1/0/11 – R-Occidente g0/0 | 10.5.0.20/30 | CORE2 .21 | R-Occidente .22 | EIGRP |
| 7 | CORE3 g1/0/12 – MS1 g0/1 | 10.5.0.24/30 | CORE3 .25 | MS1 .26 | RIPv2 |
| 8 | CORE3 g1/0/13 – MS2 g0/1 | 10.5.0.28/30 | CORE3 .29 | MS2 .30 | RIPv2 |
| 9 | CORE1 g1/0/14 – R-Central1 g0/0 | 10.5.0.32/30 | CORE1 .33 | R-Central1 .34 | OSPF |
| 10 | CORE3 g1/0/14 – R-Central1 g0/1 | 10.5.0.36/30 | CORE3 .37 | R-Central1 .38 | OSPF |
| 11 | R-Central1 Se0/0/0 – R-Central2 Se0/0/0 | 10.5.0.40/30 | R-Central1 .41 (DCE) | R-Central2 .42 | Estático |
| 12 | R-Central2 g0/0 – SW-DC-A0 g0/1 | 10.5.0.44/30 | R-Central2 .45 | SW-DC-A0 .46 | Estático |

Router-ID de OSPF: CORE1 1.1.1.1, CORE2 2.2.2.2, CORE3 3.3.3.3, R-Norte 4.4.4.4, R-Central1 5.5.5.5.

---

## 5. Tabla de cableado

Tipos de cable:
- **Straight-Through:** switch↔router y switch↔PC/servidor.
- **Cross-Over:** switch↔switch, aunque el puerto sea ruteado.
- **Fiber:** entre puertos con GLC-LH-SMD.
- **Serial DCE:** se hace clic primero en R-Central1 para que ese extremo quede como DCE.

### Backbone (Fabio)

| Origen | Destino | Cable |
|--------|---------|-------|
| CORE1 Gi1/1/1 | CORE2 Gi1/1/1 | Fibra |
| CORE1 Gi1/1/2 | CORE2 Gi1/1/2 | Fibra |
| CORE1 Gi1/0/1 | CORE3 Gi1/0/1 | Cross-Over |
| CORE1 Gi1/0/2 | CORE3 Gi1/0/2 | Cross-Over |
| CORE2 Gi1/0/3 | CORE3 Gi1/0/3 | Cross-Over |
| CORE2 Gi1/0/4 | CORE3 Gi1/0/4 | Cross-Over |
| CORE1 Gi1/0/14 | R-Central1 Gi0/0 | Straight |
| CORE3 Gi1/0/14 | R-Central1 Gi0/1 | Straight |
| R-Central1 Se0/0/0 | R-Central2 Se0/0/0 | Serial DCE |

### Occidente (Estudiante 2)

| Origen | Destino | Cable | Tipo de puerto |
|--------|---------|-------|----------------|
| R-Occidente Gi0/1 | SW-OCC-A0 Gi0/1 | Straight | Troncal 802.1Q |
| SW-OCC-A0 Fa0/1 | SW-OCC-A1 Fa0/1 | Cross-Over | Troncal |
| SW-OCC-A0 Fa0/2 | SW-OCC-A2 Fa0/2 | Cross-Over | Troncal |
| SW-OCC-A1 Fa0/11-12 | 2 PCs Cajas | Straight | Acceso VLAN 12 |
| SW-OCC-A1 Fa0/13-14 | 2 PCs Gerencia | Straight | Acceso VLAN 32 |
| SW-OCC-A2 Fa0/11-12 | 2 PCs Asesores | Straight | Acceso VLAN 22 |
| SW-OCC-A2 Fa0/13-14 | 2 PCs Seguridad | Straight | Acceso VLAN 42 |

### Data Center (Estudiante 2)

| Origen | Destino | Cable | Tipo de puerto |
|--------|---------|-------|----------------|
| SW-DC-A0 Fa0/1-2 | SW-DC-A1 Fa0/1-2 | Cross-Over x2 | Po1 troncal LACP |
| SW-DC-A0 Fa0/3-4 | SW-DC-A2 Fa0/3-4 | Cross-Over x2 | Po2 troncal LACP |
| SW-DC-A1 Fa0/11-12 | 2 servidores Core_BD | Straight | Acceso VLAN 13 |
| SW-DC-A1 Fa0/13-15 | 3 servidores Web_Apps | Straight | Acceso VLAN 23 |
| SW-DC-A2 Fa0/11-13 | 3 PCs NOC | Straight | Acceso VLAN 33 |

### Norte (Estudiante 3)

| Origen | Destino | Cable | Tipo de puerto |
|--------|---------|-------|----------------|
| R-Norte Gi0/2 | SW-NOR-A0 Gi0/1 | Straight | Troncal 802.1Q |
| SW-NOR-A0 Fa0/1 | SW-NOR-A1 Fa0/1 | Cross-Over | Troncal |
| SW-NOR-A0 Fa0/2 | SW-NOR-A2 Fa0/2 | Cross-Over | Troncal |
| SW-NOR-A1 Fa0/3 | SW-NOR-A2 Fa0/3 | Cross-Over | Troncal (cierra el triángulo) |
| SW-NOR-A1 Fa0/11-12 | 2 PCs Analisis | Straight | Acceso VLAN 52 |
| SW-NOR-A1 Fa0/13-14 | 2 PCs Auditoria | Straight | Acceso VLAN 62 |
| SW-NOR-A2 Fa0/11-12 | 2 PCs Analisis | Straight | Acceso VLAN 52 |
| SW-NOR-A2 Fa0/13-14 | 2 PCs Legal | Straight | Acceso VLAN 72 |

### Oriente (Estudiante 3)

| Origen | Destino | Cable | Tipo de puerto |
|--------|---------|-------|----------------|
| MS1 Gi0/2 | MS2 Gi0/2 | Cross-Over | Troncal (cascada) |
| MS1 Fa0/1 | SW-ORI-A1 Fa0/1 | Cross-Over | Troncal |
| MS2 Fa0/2 | SW-ORI-A1 Fa0/2 | Cross-Over | Troncal |
| MS1 Fa0/3 | SW-ORI-A2 Fa0/3 | Cross-Over | Troncal |
| MS2 Fa0/4 | SW-ORI-A2 Fa0/4 | Cross-Over | Troncal |
| SW-ORI-A1 Fa0/11-14 | 4 PCs Boveda | Straight | Acceso VLAN 82 |
| SW-ORI-A2 Fa0/11-14 | 4 PCs Plataforma | Straight | Acceso VLAN 92 |

### Cables de integración (Fabio, miércoles 21)

| Origen | Destino | Cable |
|--------|---------|-------|
| CORE1 Gi1/0/10 | R-Norte Gi0/0 | Straight |
| CORE2 Gi1/0/10 | R-Norte Gi0/1 | Straight |
| CORE2 Gi1/0/11 | R-Occidente Gi0/0 | Straight |
| CORE3 Gi1/0/12 | MS1 Gi0/1 | Cross-Over |
| CORE3 Gi1/0/13 | MS2 Gi0/1 | Cross-Over |
| R-Central2 Gi0/0 | SW-DC-A0 Gi0/1 | Straight |

---

## 6. Configuración del Backbone (Fabio)

Antes de configurar:
- En la pestaña Physical de cada 3650, arrastrar el **AC-POWER-SUPPLY** a su bahía. Sin fuente, el equipo no enciende.
- En CORE1 y CORE2, insertar **GLC-LH-SMD** en Gi1/1/1 y Gi1/1/2.
- En R-Central1 y R-Central2, apagar el router, insertar **HWIC-2T** y volver a encenderlo.

### CORE1

```
en
conf t
hostname CORE1
ip routing
int range g1/1/1-2
 no switchport
 channel-group 1 mode active
 exit
int po1
 desc Fibra hacia CORE2
 no switchport
 ip add 10.5.0.1 255.255.255.252
 exit
int range g1/0/1-2
 no switchport
 channel-group 2 mode active
 exit
int po2
 desc Hacia CORE3
 no switchport
 ip add 10.5.0.5 255.255.255.252
 exit
int g1/0/10
 desc Hacia R-Norte g0/0
 no switchport
 ip add 10.5.0.13 255.255.255.252
 no sh
 exit
int g1/0/14
 desc Hacia R-Central1 g0/0
 no switchport
 ip add 10.5.0.33 255.255.255.252
 no sh
 exit
router ospf 1
 router-id 1.1.1.1
 network 10.5.0.0 0.0.0.3 area 0
 network 10.5.0.4 0.0.0.3 area 0
 network 10.5.0.12 0.0.0.3 area 0
 network 10.5.0.32 0.0.0.3 area 0
 end
```

### CORE2 (punto de redistribución OSPF ↔ EIGRP)

```
en
conf t
hostname CORE2
ip routing
int range g1/1/1-2
 no switchport
 channel-group 1 mode active
 exit
int po1
 desc Fibra hacia CORE1
 no switchport
 ip add 10.5.0.2 255.255.255.252
 exit
int range g1/0/3-4
 no switchport
 channel-group 3 mode active
 exit
int po3
 desc Hacia CORE3
 no switchport
 ip add 10.5.0.9 255.255.255.252
 exit
int g1/0/10
 desc Hacia R-Norte g0/1
 no switchport
 ip add 10.5.0.17 255.255.255.252
 no sh
 exit
int g1/0/11
 desc Hacia R-Occidente g0/0 (EIGRP)
 no switchport
 ip add 10.5.0.21 255.255.255.252
 no sh
 exit
router ospf 1
 router-id 2.2.2.2
 network 10.5.0.0 0.0.0.3 area 0
 network 10.5.0.8 0.0.0.3 area 0
 network 10.5.0.16 0.0.0.3 area 0
 redistribute eigrp 100 subnets
 exit
router eigrp 100
 no auto-summary
 network 10.5.0.20 0.0.0.3
 redistribute ospf 1 metric 100000 100 255 1 1500
 end
```

La métrica de EIGRP es obligatoria al redistribuir. Sus valores son: ancho de banda (kbps), retardo, confiabilidad, carga y MTU.

### CORE3 (punto de redistribución OSPF ↔ RIPv2)

```
en
conf t
hostname CORE3
ip routing
int range g1/0/1-2
 no switchport
 channel-group 2 mode active
 exit
int po2
 desc Hacia CORE1
 no switchport
 ip add 10.5.0.6 255.255.255.252
 exit
int range g1/0/3-4
 no switchport
 channel-group 3 mode active
 exit
int po3
 desc Hacia CORE2
 no switchport
 ip add 10.5.0.10 255.255.255.252
 exit
int g1/0/12
 desc Hacia MS1 g0/1 (RIPv2)
 no switchport
 ip add 10.5.0.25 255.255.255.252
 no sh
 exit
int g1/0/13
 desc Hacia MS2 g0/1 (RIPv2)
 no switchport
 ip add 10.5.0.29 255.255.255.252
 no sh
 exit
int g1/0/14
 desc Hacia R-Central1 g0/1
 no switchport
 ip add 10.5.0.37 255.255.255.252
 no sh
 exit
router ospf 1
 router-id 3.3.3.3
 network 10.5.0.4 0.0.0.3 area 0
 network 10.5.0.8 0.0.0.3 area 0
 network 10.5.0.36 0.0.0.3 area 0
 redistribute rip subnets
 exit
router rip
 version 2
 no auto-summary
 network 10.0.0.0
 passive-interface po2
 passive-interface po3
 passive-interface g1/0/14
 redistribute ospf 1 metric 2
 end
```

RIP solo acepta redes con clase (`network 10.0.0.0`), así que activa RIP en todas las interfaces 10.x. Los `passive-interface` evitan enviar actualizaciones RIP hacia el núcleo OSPF.

### R-Central1 (punto de redistribución estáticas → OSPF)

```
en
conf t
hostname R-Central1
int g0/0
 desc Hacia CORE1 g1/0/14
 ip add 10.5.0.34 255.255.255.252
 no sh
 exit
int g0/1
 desc Hacia CORE3 g1/0/14
 ip add 10.5.0.38 255.255.255.252
 no sh
 exit
int s0/0/0
 desc WAN hacia R-Central2
 ip add 10.5.0.41 255.255.255.252
 clock rate 64000
 no sh
 exit
ip route 10.5.40.0 255.255.255.224 10.5.0.42
ip route 10.5.40.32 255.255.255.224 10.5.0.42
ip route 10.5.40.64 255.255.255.240 10.5.0.42
router ospf 1
 router-id 5.5.5.5
 network 10.5.0.32 0.0.0.3 area 0
 network 10.5.0.36 0.0.0.3 area 0
 redistribute static subnets
 end
```

### R-Central2 (router de acceso al segmento estático)

```
en
conf t
hostname R-Central2
int s0/0/0
 desc WAN hacia R-Central1
 ip add 10.5.0.42 255.255.255.252
 no sh
 exit
int g0/0
 desc Hacia SW-DC-A0 g0/1
 ip add 10.5.0.45 255.255.255.252
 no sh
 exit
ip route 10.5.40.0 255.255.255.224 10.5.0.46
ip route 10.5.40.32 255.255.255.224 10.5.0.46
ip route 10.5.40.64 255.255.255.240 10.5.0.46
ip route 0.0.0.0 0.0.0.0 10.5.0.41
 end
```

---

## 7. Configuración Sede Occidente (Estudiante 2)

Mapeo lógico:
- **Switch principal/distribución:** SW-OCC-A0, servidor VTP.
- **Troncales 802.1Q:** R-Occidente Gi0/1↔A0 Gi0/1, A0 Fa0/1↔A1, A0 Fa0/2↔A2.
- **Puertos de acceso:** Fa0/11-14 en A1 y A2.

### R-Occidente (Router-on-a-Stick + EIGRP)

```
en
conf t
hostname R-Occidente
int g0/0
 desc Hacia CORE2 g1/0/11 (EIGRP)
 ip add 10.5.0.22 255.255.255.252
 no sh
 exit
int g0/1
 desc Troncal hacia SW-OCC-A0
 no sh
 exit
int g0/1.12
 desc Cajas
 encapsulation dot1Q 12
 ip add 10.5.10.1 255.255.255.192
 exit
int g0/1.22
 desc Asesores
 encapsulation dot1Q 22
 ip add 10.5.10.65 255.255.255.192
 exit
int g0/1.32
 desc Gerencia
 encapsulation dot1Q 32
 ip add 10.5.10.145 255.255.255.240
 exit
int g0/1.42
 desc Seguridad
 encapsulation dot1Q 42
 ip add 10.5.10.129 255.255.255.240
 exit
router eigrp 100
 no auto-summary
 network 10.5.0.20 0.0.0.3
 network 10.5.10.0 0.0.0.255
 passive-interface g0/1.12
 passive-interface g0/1.22
 passive-interface g0/1.32
 passive-interface g0/1.42
 end
```

### SW-OCC-A0 (servidor VTP)

```
en
conf t
hostname SW-OCC-A0
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
 exit
int g0/1
 desc Troncal hacia R-Occidente
 sw mode trunk
 exit
int fa0/1
 desc Troncal hacia SW-OCC-A1
 sw mode trunk
 exit
int fa0/2
 desc Troncal hacia SW-OCC-A2
 sw mode trunk
 end
```

### SW-OCC-A1 (cliente VTP)

```
en
conf t
hostname SW-OCC-A1
vtp domain bantech05
vtp password cisco
vtp mode client
int fa0/1
 desc Troncal hacia SW-OCC-A0
 sw mode trunk
 exit
int range fa0/11-12
 sw mode access
 sw access vlan 12
 spanning-tree portfast
 exit
int range fa0/13-14
 sw mode access
 sw access vlan 32
 spanning-tree portfast
 end
```

### SW-OCC-A2 (cliente VTP)

```
en
conf t
hostname SW-OCC-A2
vtp domain bantech05
vtp password cisco
vtp mode client
int fa0/2
 desc Troncal hacia SW-OCC-A0
 sw mode trunk
 exit
int range fa0/11-12
 sw mode access
 sw access vlan 22
 spanning-tree portfast
 exit
int range fa0/13-14
 sw mode access
 sw access vlan 42
 spanning-tree portfast
 end
```

Orden recomendado: primero los troncales. Luego verificar con `show vlan brief` en A1 y A2 que llegaron las 4 VLANs, y solo después asignar los puertos de acceso.

### PCs Occidente

| PC | Switch/puerto | IP | Máscara | Gateway |
|----|---------------|----|---------|---------|
| PC-CAJA1, PC-CAJA2 | A1 Fa0/11-12 | 10.5.10.2, .3 | 255.255.255.192 | 10.5.10.1 |
| PC-GER1, PC-GER2 | A1 Fa0/13-14 | 10.5.10.146, .147 | 255.255.255.240 | 10.5.10.145 |
| PC-ASE1, PC-ASE2 | A2 Fa0/11-12 | 10.5.10.66, .67 | 255.255.255.192 | 10.5.10.65 |
| PC-SEG1, PC-SEG2 | A2 Fa0/13-14 | 10.5.10.130, .131 | 255.255.255.240 | 10.5.10.129 |

---

## 8. Configuración Data Center (Estudiante 2)

Mapeo lógico:
- **Switch principal/distribución:** SW-DC-A0 (3560 multicapa, inter-VLAN por SVIs).
- **Troncales:** Po1 A0↔A1 y Po2 A0↔A2, ambos EtherChannel LACP.
- **Enlace ruteado:** A0 Gi0/1↔R-Central2.
- **Puertos de acceso:** Fa0/11 en adelante en A1 y A2.

### SW-DC-A0 (distribución, 3560)

```
en
conf t
hostname SW-DC-A0
ip routing
vlan 13
 name Core_BD
vlan 23
 name Web_Apps
vlan 33
 name NOC
 exit
int g0/1
 desc Enlace ruteado hacia R-Central2
 no switchport
 ip add 10.5.0.46 255.255.255.252
 no sh
 exit
int range fa0/1-2
 desc Po1 hacia SW-DC-A1
 sw trunk encapsulation dot1q
 sw mode trunk
 channel-group 1 mode active
 exit
int range fa0/3-4
 desc Po2 hacia SW-DC-A2
 sw trunk encapsulation dot1q
 sw mode trunk
 channel-group 2 mode active
 exit
int vlan 13
 ip add 10.5.40.33 255.255.255.224
 no sh
int vlan 23
 ip add 10.5.40.1 255.255.255.224
 no sh
int vlan 33
 ip add 10.5.40.65 255.255.255.240
 no sh
 exit
ip route 0.0.0.0 0.0.0.0 10.5.0.45
 end
```

### SW-DC-A1 (acceso servidores)

```
en
conf t
hostname SW-DC-A1
vlan 13
 name Core_BD
vlan 23
 name Web_Apps
vlan 33
 name NOC
 exit
int range fa0/1-2
 desc Po1 hacia SW-DC-A0
 sw mode trunk
 channel-group 1 mode active
 exit
int range fa0/11-12
 sw mode access
 sw access vlan 13
 spanning-tree portfast
 exit
int range fa0/13-15
 sw mode access
 sw access vlan 23
 spanning-tree portfast
 end
```

### SW-DC-A2 (acceso NOC)

```
en
conf t
hostname SW-DC-A2
vlan 13
 name Core_BD
vlan 23
 name Web_Apps
vlan 33
 name NOC
 exit
int range fa0/3-4
 desc Po2 hacia SW-DC-A0
 sw mode trunk
 channel-group 2 mode active
 exit
int range fa0/11-13
 sw mode access
 sw access vlan 33
 spanning-tree portfast
 end
```

### Servidores y PCs Data Center

| Equipo | Switch/puerto | IP | Máscara | Gateway |
|--------|---------------|----|---------|---------|
| SRV-BD1, SRV-BD2 | A1 Fa0/11-12 | 10.5.40.34, .35 | 255.255.255.224 | 10.5.40.33 |
| SRV-WEB1, 2, 3 | A1 Fa0/13-15 | 10.5.40.2, .3, .4 | 255.255.255.224 | 10.5.40.1 |
| PC-NOC1, 2, 3 | A2 Fa0/11-13 | 10.5.40.66, .67, .68 | 255.255.255.240 | 10.5.40.65 |

Opcional: dejar activo el servicio HTTP en SRV-WEB1 y abrirlo desde el navegador de un PC de Occidente. Es una evidencia adicional de servicio de extremo a extremo.

---

## 9. Configuración Sede Norte (Estudiante 3)

Mapeo lógico:
- **Switch principal:** SW-NOR-A0, Root Bridge forzado.
- **Troncales:** R-Norte Gi0/2↔A0 Gi0/1, y el triángulo A0 Fa0/1↔A1, A0 Fa0/2↔A2, A1 Fa0/3↔A2.
- **Puertos de acceso:** Fa0/11-14 en A1 y A2.

### R-Norte (Router-on-a-Stick + OSPF, doble salida al núcleo)

```
en
conf t
hostname R-Norte
int g0/0
 desc Hacia CORE1 g1/0/10
 ip add 10.5.0.14 255.255.255.252
 no sh
 exit
int g0/1
 desc Hacia CORE2 g1/0/10
 ip add 10.5.0.18 255.255.255.252
 no sh
 exit
int g0/2
 desc Troncal hacia SW-NOR-A0
 no sh
 exit
int g0/2.52
 desc Analisis
 encapsulation dot1Q 52
 ip add 10.5.20.1 255.255.255.192
 exit
int g0/2.62
 desc Auditoria
 encapsulation dot1Q 62
 ip add 10.5.20.65 255.255.255.224
 exit
int g0/2.72
 desc Legal
 encapsulation dot1Q 72
 ip add 10.5.20.97 255.255.255.224
 exit
router ospf 1
 router-id 4.4.4.4
 network 10.5.0.12 0.0.0.3 area 0
 network 10.5.0.16 0.0.0.3 area 0
 network 10.5.20.0 0.0.0.255 area 0
 passive-interface g0/2.52
 passive-interface g0/2.62
 passive-interface g0/2.72
 end
```

### SW-NOR-A0 (principal, Root Bridge)

```
en
conf t
hostname SW-NOR-A0
spanning-tree mode rapid-pvst
vlan 52
 name Analisis
vlan 62
 name Auditoria
vlan 72
 name Legal
 exit
int g0/1
 desc Troncal hacia R-Norte
 sw mode trunk
 exit
int fa0/1
 desc Troncal hacia SW-NOR-A1
 sw mode trunk
 exit
int fa0/2
 desc Troncal hacia SW-NOR-A2
 sw mode trunk
 exit
spanning-tree vlan 52,62,72 root primary
 end
```

### SW-NOR-A1 (acceso, Root secundario)

```
en
conf t
hostname SW-NOR-A1
spanning-tree mode rapid-pvst
vlan 52
 name Analisis
vlan 62
 name Auditoria
vlan 72
 name Legal
 exit
int fa0/1
 desc Troncal hacia SW-NOR-A0
 sw mode trunk
 exit
int fa0/3
 desc Troncal hacia SW-NOR-A2
 sw mode trunk
 exit
int range fa0/11-12
 sw mode access
 sw access vlan 52
 spanning-tree portfast
 exit
int range fa0/13-14
 sw mode access
 sw access vlan 62
 spanning-tree portfast
 exit
spanning-tree vlan 52,62,72 root secondary
 end
```

### SW-NOR-A2 (acceso)

```
en
conf t
hostname SW-NOR-A2
spanning-tree mode rapid-pvst
vlan 52
 name Analisis
vlan 62
 name Auditoria
vlan 72
 name Legal
 exit
int fa0/2
 desc Troncal hacia SW-NOR-A0
 sw mode trunk
 exit
int fa0/3
 desc Troncal hacia SW-NOR-A1
 sw mode trunk
 exit
int range fa0/11-12
 sw mode access
 sw access vlan 52
 spanning-tree portfast
 exit
int range fa0/13-14
 sw mode access
 sw access vlan 72
 spanning-tree portfast
 end
```

Con A0 como root y A1 como secundario, el puerto que se bloquea debería quedar en SW-NOR-A2 Fa0/3, en el enlace A1↔A2. Verificar con `show spanning-tree vlan 52` en A2 y anotar el resultado real para el manual.

### PCs Norte

| PC | Switch/puerto | IP | Máscara | Gateway |
|----|---------------|----|---------|---------|
| PC-ANA1, PC-ANA2 | A1 Fa0/11-12 | 10.5.20.2, .3 | 255.255.255.192 | 10.5.20.1 |
| PC-AUD1, PC-AUD2 | A1 Fa0/13-14 | 10.5.20.66, .67 | 255.255.255.224 | 10.5.20.65 |
| PC-ANA3, PC-ANA4 | A2 Fa0/11-12 | 10.5.20.4, .5 | 255.255.255.192 | 10.5.20.1 |
| PC-LEG1, PC-LEG2 | A2 Fa0/13-14 | 10.5.20.98, .99 | 255.255.255.224 | 10.5.20.97 |

---

## 10. Configuración Sede Oriente (Estudiante 3)

Mapeo lógico:
- **Switches principales (distribución):** MS1 (activo) y MS2 (respaldo).
- **Troncales:** MS1 Gi0/2↔MS2 Gi0/2 (cascada), y cada switch de acceso con uplink a MS1 y a MS2.
- **Enlaces ruteados:** MS1 Gi0/1 y MS2 Gi0/1 hacia CORE3.
- **Puertos de acceso:** Fa0/11-14 en A1 y A2.

### MS1 (HSRP activo, Root primario)

```
en
conf t
hostname MS1
ip routing
spanning-tree mode rapid-pvst
vlan 82
 name Boveda
vlan 92
 name Plataforma
 exit
int g0/1
 desc Enlace ruteado hacia CORE3 g1/0/12
 no switchport
 ip add 10.5.0.26 255.255.255.252
 no sh
 exit
int g0/2
 desc Cascada hacia MS2
 sw trunk encapsulation dot1q
 sw mode trunk
 exit
int fa0/1
 desc Troncal hacia SW-ORI-A1
 sw trunk encapsulation dot1q
 sw mode trunk
 exit
int fa0/3
 desc Troncal hacia SW-ORI-A2
 sw trunk encapsulation dot1q
 sw mode trunk
 exit
spanning-tree vlan 82,92 root primary
int vlan 82
 ip add 10.5.30.130 255.255.255.192
 standby 82 ip 10.5.30.129
 standby 82 priority 110
 standby 82 preempt
 no sh
 exit
int vlan 92
 ip add 10.5.30.2 255.255.255.128
 standby 92 ip 10.5.30.1
 standby 92 priority 110
 standby 92 preempt
 no sh
 exit
router rip
 version 2
 no auto-summary
 network 10.0.0.0
 end
```

### MS2 (HSRP standby, Root secundario)

```
en
conf t
hostname MS2
ip routing
spanning-tree mode rapid-pvst
vlan 82
 name Boveda
vlan 92
 name Plataforma
 exit
int g0/1
 desc Enlace ruteado hacia CORE3 g1/0/13
 no switchport
 ip add 10.5.0.30 255.255.255.252
 no sh
 exit
int g0/2
 desc Cascada hacia MS1
 sw trunk encapsulation dot1q
 sw mode trunk
 exit
int fa0/2
 desc Troncal hacia SW-ORI-A1
 sw trunk encapsulation dot1q
 sw mode trunk
 exit
int fa0/4
 desc Troncal hacia SW-ORI-A2
 sw trunk encapsulation dot1q
 sw mode trunk
 exit
spanning-tree vlan 82,92 root secondary
int vlan 82
 ip add 10.5.30.131 255.255.255.192
 standby 82 ip 10.5.30.129
 standby 82 priority 100
 standby 82 preempt
 no sh
 exit
int vlan 92
 ip add 10.5.30.3 255.255.255.128
 standby 92 ip 10.5.30.1
 standby 92 priority 100
 standby 92 preempt
 no sh
 exit
router rip
 version 2
 no auto-summary
 network 10.0.0.0
 end
```

Opcional recomendado: tracking de interfaz en MS1, para que ceda el rol activo si pierde su uplink al núcleo aunque siga encendido. Si el IOS de Packet Tracer no lo acepta, se omite.

```
int vlan 82
 standby 82 track g0/1 20
int vlan 92
 standby 92 track g0/1 20
```

### SW-ORI-A1 (acceso Boveda)

```
en
conf t
hostname SW-ORI-A1
spanning-tree mode rapid-pvst
vlan 82
 name Boveda
vlan 92
 name Plataforma
 exit
int fa0/1
 desc Uplink hacia MS1
 sw mode trunk
 exit
int fa0/2
 desc Uplink hacia MS2
 sw mode trunk
 exit
int range fa0/11-14
 sw mode access
 sw access vlan 82
 spanning-tree portfast
 end
```

### SW-ORI-A2 (acceso Plataforma)

```
en
conf t
hostname SW-ORI-A2
spanning-tree mode rapid-pvst
vlan 82
 name Boveda
vlan 92
 name Plataforma
 exit
int fa0/3
 desc Uplink hacia MS1
 sw mode trunk
 exit
int fa0/4
 desc Uplink hacia MS2
 sw mode trunk
 exit
int range fa0/11-14
 sw mode access
 sw access vlan 92
 spanning-tree portfast
 end
```

### PCs Oriente (el gateway es siempre la IP virtual HSRP)

| PC | Switch/puerto | IP | Máscara | Gateway |
|----|---------------|----|---------|---------|
| PC-BOV1 a PC-BOV4 | A1 Fa0/11-14 | 10.5.30.132 – .135 | 255.255.255.192 | 10.5.30.129 |
| PC-PLA1 a PC-PLA4 | A2 Fa0/11-14 | 10.5.30.4 – .7 | 255.255.255.128 | 10.5.30.1 |

---

## 11. Integración en el archivo maestro (Fabio, miércoles 21)

1. Cada integrante hace `wr` en todos sus equipos y sube su .pkt y sus .txt de `configs/`.
2. Abrir el archivo maestro y, en otra ventana de Packet Tracer, el archivo del estudiante.
3. En el archivo del estudiante, seleccionar todo su bloque con un recuadro, Ctrl+C, y en el maestro Ctrl+V.
4. Verificar en 2 o 3 equipos con `show run` que la configuración se conservó. Si algo se perdió, pegar el .txt correspondiente en la CLI.
5. Conectar los 6 cables de integración de la sección 5.
6. Marcar los dominios con la herramienta de rectángulos y notas de Packet Tracer:
   - "OSPF área 0 – Núcleo + Norte"
   - "EIGRP 100 – Occidente"
   - "RIPv2 – Oriente"
   - "Rutas estáticas – Data Center"
   - Además, una nota en CORE2, CORE3 y R-Central1 que diga "Punto de redistribución".
7. Verificar las adyacencias:
   - `show ip ospf neighbor` en CORE1: debe ver CORE2, CORE3, R-Norte y R-Central1.
   - `show ip eigrp neighbors` en CORE2: debe ver a R-Occidente.
   - `show ip route rip` en CORE3: debe mostrar las redes 10.5.30.x.

### Estructura sugerida del repositorio (privado, con los 3 como colaboradores)

```
Redes1_Proyecto2_Grupo2/
├── README.md                  (Manual técnico consolidado)
├── BanTech_Grupo2.pkt         (archivo maestro integrado)
├── pkt-parciales/             (archivos de cada integrante)
├── configs/                   (un .txt por equipo: CORE1.txt, MS1.txt, ...)
└── img/                       (capturas con los nombres de la sección 12)
```

---

## 12. Pruebas y checklist de capturas

### Tablas de enrutamiento esperadas

- **R-Occidente:** las redes de las otras sedes aparecen como `D EX` (externas de EIGRP).
- **CORE2:** Occidente como `D`, Norte como `O`, Oriente y Data Center como `O E2`.
- **CORE3:** Oriente como `R`, Norte como `O`, Occidente y Data Center como `O E2`.
- **R-Central1:** Data Center como `S`, y el resto como `O` u `O E2`.
- **MS1 y MS2:** todas las redes externas como `R`.
- **R-Central2:** las rutas `S` hacia el Data Center y `S*` por defecto.

### Pruebas de failover

1. **HSRP (Oriente):**
   - Desde PC-PLA1, `ping -t 10.5.40.34`.
   - Hacer `wr` en MS1 y apagarlo desde la pestaña Physical, para simular el corte de energía que pide el enunciado.
   - Se esperan 1 a 3 timeouts y luego el ping continúa. En MS2, `show standby brief` debe mostrar Active.
   - Al encender MS1, por preempt vuelve a ser Active.
2. **STP (Norte):**
   - Con `show spanning-tree vlan 52` en A2, confirmar el puerto Altn BLK.
   - Hacer `shutdown` en SW-NOR-A0 Fa0/1. El puerto bloqueado debe pasar a FWD y PC-ANA1 debe seguir haciendo ping al gateway.
3. **EtherChannel del núcleo:**
   - `show etherchannel summary` en CORE1, con Po1, Po2 y Po3 en estado (RU).
   - Hacer `shutdown` en g1/1/1: Po1 sigue arriba con un miembro.
   - Luego `shutdown` en todo Po1: con `tracert` se ve que el tráfico CORE1→CORE2 se va por CORE3.
4. **EtherChannel del Data Center:**
   - Hacer `shutdown` en SW-DC-A0 Fa0/1. Los servidores siguen alcanzables por el miembro restante.
5. **Doble salida de Norte:**
   - Hacer `shutdown` en CORE1 g1/0/10. Norte sigue alcanzable vía CORE2.

### Checklist de capturas (nombres exactos para el README)

| Archivo | Contenido | Responsable |
|---------|-----------|-------------|
| img/01_topologia_general.png | Topología completa con etiquetas de dominios | Fabio |
| img/02_etherchannel_core.png | show etherchannel summary en CORE1 | Fabio |
| img/03_ospf_vecinos.png | show ip ospf neighbor en CORE1 | Fabio |
| img/04_route_core2.png | show ip route en CORE2 | Fabio |
| img/05_route_core3.png | show ip route en CORE3 | Fabio |
| img/06_route_rcentral1.png | show ip route en R-Central1 | Fabio |
| img/07_ping_occ_dc.png | Ping de PC-CAJA1 a SRV-BD1 | Fabio |
| img/08_ping_norte_oriente.png | Ping de PC-ANA1 a PC-PLA1 | Fabio |
| img/09_failover_core.png | tracert antes y después de apagar Po1 | Fabio |
| img/10_topologia_occidente.png | Vista de la sede | Estudiante 2 |
| img/11_vtp_status.png | show vtp status en A0 y A1 | Estudiante 2 |
| img/12_vlan_brief_occ.png | show vlan brief en un cliente | Estudiante 2 |
| img/13_route_roccidente.png | show ip route en R-Occidente (D EX) | Estudiante 2 |
| img/14_intervlan_occ.png | Ping de Cajas a Asesores | Estudiante 2 |
| img/15_topologia_dc.png | Vista del Data Center | Estudiante 2 |
| img/16_etherchannel_dc.png | show etherchannel summary en SW-DC-A0 | Estudiante 2 |
| img/17_failover_etherchannel_dc.png | Ping continuo con un miembro apagado | Estudiante 2 |
| img/18_topologia_norte.png | Vista de la sede | Estudiante 3 |
| img/19_stp_root.png | show spanning-tree vlan 52 en A0 (This bridge is the root) | Estudiante 3 |
| img/20_stp_bloqueado.png | show spanning-tree vlan 52 en A2 (Altn BLK) | Estudiante 3 |
| img/21_failover_stp.png | Puerto pasando a FWD tras el shutdown | Estudiante 3 |
| img/22_topologia_oriente.png | Vista de la sede | Estudiante 3 |
| img/23_hsrp_antes.png | show standby brief en MS1 y MS2 | Estudiante 3 |
| img/24_failover_hsrp.png | ping -t con MS1 apagado y MS2 en Active | Estudiante 3 |
| img/25_route_ms1.png | show ip route en MS1 (rutas R) | Estudiante 3 |

---

## 13. Argumentos técnicos para las justificaciones

Son viñetas de apoyo. Cada quien redacta su párrafo con sus propias palabras.

### Backbone

- Triángulo de 3 switches multicapa: cualquier núcleo puede fallar y los otros dos mantienen la conectividad. No hay punto único de falla.
- EtherChannel L3 con LACP (IEEE 802.3ad / 802.1AX): suma ancho de banda, tolera la caída de un miembro sin reconvergencia de OSPF, y es un estándar abierto, interoperable entre fabricantes.
- Po1 en fibra entre CORE1 y CORE2: es el canal principal del tráfico transaccional. La fibra da inmunidad a interferencia electromagnética y mayor alcance.
- Un solo punto de redistribución por dominio externo: evita bucles y rutas subóptimas propias de la redistribución mutua en varios puntos.
- Serial hacia R-Central2: representa el enlace WAN dedicado del segmento de alta seguridad.

### Asignación de protocolos

- **Norte en OSPF:**
  - Es la sede de la que dependen los créditos de todo el país.
  - Al estar en el mismo dominio que el núcleo, no depende de redistribución.
  - Tiene doble salida a CORE1 y CORE2 con convergencia rápida (estado de enlace).
- **Occidente en EIGRP:**
  - Corresponde al "dominio de expansión regional".
  - DUAL ofrece convergencia casi inmediata con sucesores factibles.
  - Es sencillo agregar nuevas agencias regionales.
- **Oriente en RIPv2:**
  - Es el banco recién adquirido, con su red legada.
  - Se integra sin migrarlo de inmediato, aislado tras el punto de redistribución en CORE3.
- **Data Center con estáticas:**
  - Ningún protocolo dinámico publica ni aprende rutas dentro del segmento crítico.
  - El control de lo que entra y sale es explícito, y R-Central1 expone solo las 3 redes necesarias.

### Occidente (estrella con switch de distribución)

- Administración centralizada: un solo servidor VTP propaga las VLANs a los clientes.
- Cajas en SW-OCC-A1 y Asesores en SW-OCC-A2: una falla o tormenta en Asesores queda confinada a su switch y a su VLAN. Responde a la necesidad operativa de la sede.
- Router-on-a-Stick: es lo que exige el enunciado y basta para el tráfico inter-VLAN de una agencia comercial.

### Norte (triángulo con Rapid PVST+)

- Cada switch de analistas tiene dos caminos físicos hacia SW-NOR-A0. Ningún cable es punto único de falla.
- Rapid PVST+ (802.1w por VLAN) bloquea el bucle lógico y converge en segundos, frente a 30 a 50 s del STP clásico.
- Root en SW-NOR-A0 porque ahí se conecta R-Norte: el tráfico hacia el gateway sigue el camino más corto. A1 como secundario garantiza un reemplazo predecible.

### Oriente (doble conexión + HSRP)

- Cada switch de acceso está conectado a MS1 y a MS2: si uno cae, el otro conserva la Capa 2 y la Capa 3.
- HSRP en lugar de VRRP: es nativo de Cisco, está soportado por Packet Tracer y es el que pide la rúbrica.
- MS1 activo con prioridad 110 y preempt, alineado con el Root Bridge STP para evitar caminos subóptimos.
- Cada switch multicapa tiene su propio uplink a CORE3.

### Data Center (distribución multicapa + EtherChannel)

- La capa de distribución separa los servidores del router. El inter-VLAN en el 3560 se hace por hardware y es más rápido que Router-on-a-Stick.
- EtherChannel LACP hacia cada switch de acceso: suma capacidad para las ráfagas de tráfico y tolera la caída de un cable.
- Las estáticas encadenadas (SW-DC-A0 → R-Central2 → R-Central1) mantienen el segmento aislado del núcleo.

---

## 14. Problemas comunes en Packet Tracer

- **3650 apagado:** le falta el AC-POWER-SUPPLY en la pestaña Physical.
- **Sin módulo de fibra en el 3650:** probar primero que GLC-LH-SMD entre en Gi1/1/1. Si no funciona, avisar antes de seguir para definir una alternativa.
- **Trunk que no sube en un 3560:** falta `sw trunk encapsulation dot1q` antes de `sw mode trunk`.
- **Redes que no se ven entre sedes:** revisar `no auto-summary` en EIGRP y RIP. Todas son 10.x y la sumarización automática las rompe.
- **Serial caído:** falta `clock rate 64000` en el extremo DCE (R-Central1).
- **EtherChannel suspendido:** los puertos miembros deben tener exactamente la misma configuración.
- **Configuración perdida al apagar un equipo:** hacer `wr` antes de la prueba de HSRP.
- **CORE3 no pasa las rutas de Occidente o Data Center a RIP:** cambiar la redistribución por `redistribute ospf 1 metric 2 match internal external 1 external 2`.
- **PCs que no salen de su red:** revisar el gateway. En Oriente debe ser la IP virtual, no la de MS1.

---

## 15. Estructura del README (Manual Técnico)

1. Portada: curso, proyecto, grupo 2, integrantes y carnés.
2. Índice.
3. Descripción general y parámetros (XX = 05, Y = 2).
4. Topología general (captura 01) y diagrama de dominios.
5. Backbone: diseño, medios físicos, EtherChannel, dominios, puntos de redistribución, justificación y configuraciones clave.
6. Tabla de VLANs.
7. Tablas de subneteo (VLSM) y de enlaces punto a punto.
8. Una sección por sede, cada una con:
   - Topología (captura)
   - Mapeo lógico: principal, troncales y accesos
   - Justificación
   - Extractos de configuración, indicando el equipo
   - Pruebas
9. Pruebas de convergencia: pings y tablas de enrutamiento.
10. Pruebas de alta disponibilidad: HSRP, STP y EtherChannel.
11. Conclusiones y mejoras posibles. Por ejemplo: VLAN nativa distinta de la 1, puertos sin uso apagados, autenticación OSPF/EIGRP, SSH en lugar de Telnet.
