# Actividad Práctica 3 — Spanning Tree Protocol (PVST vs Rapid PVST)

**Curso:** Redes de Computadoras 1
**Carné:** 201905884 → dígito de red **X = 4**
**Archivo de simulación:** `APT3_201905884_STP.pkt`

---

## 1. Topología

Tres switches Cisco 2960-24TT conectados en **triángulo**, es decir con un enlace
redundante que cierra un anillo físico de capa 2:

```
                       ┌──────────────┐
                       │   Switch0    │  ← RAÍZ (priority 4096)
                       └─Gi0/1  Gi0/2─┘
                          │        │
                troncal   │        │   troncal
                          │        │
             ┌─Gi0/1──────┘        └──────Gi0/2─┐
             │  Switch1                 Switch2 │
             └─Gi0/2─────── troncal ─────Gi0/1──┘
                   ▲
                   └── Switch1 Gi0/2 queda en BLOCKING

   Switch1                            Switch2
    Fa0/1 → PC0  VLAN 10 Ventas        Fa0/1 → PC2  VLAN 10 Ventas
    Fa0/2 → PC1  VLAN 20 Compras       Fa0/2 → PC3  VLAN 20 Compras
```

### Direccionamiento

| Área    | VLAN | Red              | Equipo | Dirección        | Switch / puerto |
|---------|------|------------------|--------|------------------|-----------------|
| Ventas  | 10   | 192.168.14.0/24  | PC0    | 192.168.14.10/24 | Switch1 Fa0/1   |
| Ventas  | 10   | 192.168.14.0/24  | PC2    | 192.168.14.11/24 | Switch2 Fa0/1   |
| Compras | 20   | 192.168.24.0/24  | PC1    | 192.168.24.10/24 | Switch1 Fa0/2   |
| Compras | 20   | 192.168.24.0/24  | PC3    | 192.168.24.11/24 | Switch2 Fa0/2   |

Los tres enlaces entre switches son **troncales 802.1Q** que transportan ambas
VLANs. No hay router: el tráfico evaluado es intra-VLAN (PC0↔PC2 y PC1↔PC3), que
es justo lo que exige la actividad — *ping entre máquinas de la misma VLAN*.

---

## 2. La red sin STP

Con los tres enlaces activos y sin STP, el anillo Switch0–Switch1–Switch2–Switch0
no tiene nada que corte la redundancia. La trama Ethernet **no tiene TTL**, así
que un broadcast (un ARP, un DHCP Discover, una trama a MAC desconocida) se
reenvía por todos los puertos menos el de entrada, vuelve al switch original y se
reenvía otra vez, para siempre:

- **Tormenta de broadcast:** la trama circula sin fin y se duplica en cada vuelta
  del anillo; la CPU de los switches se satura.
- **Inestabilidad de la tabla MAC:** el mismo MAC origen llega alternadamente por
  Gi0/1 y Gi0/2, así que cada switch reescribe la entrada una y otra vez
  (*MAC address table flapping*) y deja de saber por dónde alcanzar al host.
- **Tramas unicast duplicadas:** el destino recibe varias copias del mismo paquete.
- La red queda inutilizable aunque físicamente todo esté bien conectado.

---

## 3. Cómo se eligió el switch raíz

STP elige la raíz por **menor Bridge ID**, que son 8 bytes:

```
  Bridge ID = [ Prioridad (4 bits) | Extended System ID = VLAN (12 bits) | MAC (48 bits) ]
                    ↑ múltiplos de 4096                                      ↑ desempate
```

Las MAC reales de los tres switches de esta simulación son:

| Switch  | MAC (Bridge ID)  | Prioridad por defecto |
|---------|------------------|-----------------------|
| Switch0 | `000D.BD3E.13D4` | 32768                 |
| Switch1 | `0010.1173.4E32` | 32768                 |
| Switch2 | `0001.4298.2D34` | 32768                 |

El proceso fue:

1. **Al arrancar, los tres se creen raíz.** Cada uno envía BPDUs anunciándose a
   sí mismo, con prioridad por defecto 32768 más el ID de VLAN → 32778 en la
   VLAN 10 y 32788 en la VLAN 20.
2. **Se compara la prioridad primero.** Al ser las tres iguales, el desempate
   pasa a la **MAC más baja**. Aquí la más baja es la de **Switch2**
   (`0001.…`), así que sin intervención la raíz habría sido Switch2 — un
   resultado que depende del hardware y no del diseño.
3. **Se fuerza la raíz manualmente.** Para que la raíz sea Switch0 de forma
   explícita y reproducible, como pide la actividad, se baja su prioridad:

   ```
   Switch0(config)# spanning-tree vlan 10 priority 4096
   Switch0(config)# spanning-tree vlan 20 priority 4096
   ```

   Su Bridge ID pasa a **4106** en la VLAN 10 y **4116** en la VLAN 20, muy por
   debajo de los 32778/32788 de los otros dos. En el siguiente intercambio de
   BPDUs, Switch1 y Switch2 dejan de anunciarse y aceptan a Switch0 como raíz.

   > `spanning-tree vlan 10,20 root primary` hace lo mismo, calculando la
   > prioridad automáticamente. Se usó `priority 4096` por ser explícito.

4. **Roles de puerto resultantes:**
   - **Switch0**, al ser la raíz, tiene *todos* sus puertos **Designated** y en
     `FWD`. Una raíz nunca bloquea nada.
   - **Switch1** y **Switch2** eligen su **Root Port**: el de menor costo
     acumulado hacia la raíz. Ambos tienen un enlace Gigabit directo a Switch0
     (costo 4), así que su Root Port es `Gi0/1` en los dos.
   - En el segmento **Switch1↔Switch2** ninguno es la raíz y ambos tienen el
     mismo costo hacia ella (4). El desempate vuelve a ser el **Bridge ID más
     bajo**: `0001.4298.2D34` (Switch2) < `0010.1173.4E32` (Switch1), así que
     **Switch2 Gi0/2 queda Designated / FWD** y **Switch1 Gi0/2 queda
     Alternate / BLOCKING**.

**Verificación empírica del puerto bloqueado.** No basta con predecirlo: se
eliminó el cable `Switch1 Gi0/2 ↔ Switch2 Gi0/2` mientras corría un ping de PC0 a
PC2, y el resultado fue **`Sent = 4, Received = 4, Lost = 0 (0% loss)`** — cero
impacto. Un enlace cuya desaparición no cuesta un solo paquete es, por
definición, un enlace que no estaba reenviando tráfico: confirma que
**`Switch1 Gi0/2` era el puerto en BLOCKING**.

**Comandos de verificación:**
- En Switch0: `show spanning-tree vlan 10` → `This bridge is the root`.
- En Switch1: `show spanning-tree vlan 10` → bloque `Root ID` con prioridad 4106
  y la MAC de Switch0, y `Gi0/2` con rol `Altn` y estado `BLK`.

---

## 4. Análisis con PVST (modo por defecto)

**Procedimiento:** ping extendido de PC0 (192.168.14.10) a PC2 (192.168.14.11) y,
mientras corre, se elimina el **puerto raíz de Switch1** (`Gi0/1`, su camino
activo hacia Switch0). Eso obliga a Switch1 a promover su puerto bloqueado.

**Medición real de esta simulación:**

| Evento | Hora | Resultado |
|---|---|---|
| Se corta `Switch1 Gi0/1` | `14:08:03` | — |
| Ping lanzado ~1 s después del corte | `14:08:04` → `14:08:35` | **Sent = 4, Received = 0, Lost = 4 (100% loss)** |
| Ping siguiente | `14:08:35` → | **Sent = 4, Received = 4, Lost = 0 (0% loss)** |

El último paquete del primer ping seguía expirando a los ~24 s del corte, y el
siguiente ping ya pasaba completo. **La convergencia tomó del orden de 25 a 32
segundos.**

**¿Qué pasa con los paquetes?** Se pierden todos durante la ventana de
convergencia. **¿Existe convergencia?** Sí — la red se recupera sola, sin tocar
nada — pero es lenta.

**Por qué tarda tanto:** al caer el enlace, el puerto que estaba en `BLK` debe
recorrer la máquina de estados completa de 802.1D antes de reenviar:

| Estado      | Temporizador  | Duración | Qué hace |
|-------------|---------------|----------|----------|
| Blocking    | Max Age       | 20 s     | Espera a que expire la BPDU superior guardada |
| Listening   | Forward Delay | 15 s     | Procesa BPDUs y recalcula, no aprende MACs |
| Learning    | Forward Delay | 15 s     | Aprende MACs, todavía no reenvía datos |
| Forwarding  | —             | —        | Reenvía tráfico |

Los ~30 s medidos corresponden a **Listening + Learning (15 + 15)**. Los 20 s de
Max Age se ahorraron porque el fallo fue **directo** sobre el puerto (pérdida de
portadora), que STP detecta al instante. Si la caída hubiera sido indirecta se
habrían pagado los ~50 s completos.

**Detalle de PVST:** mantiene una **instancia de STP independiente por VLAN**;
por eso `show spanning-tree` imprime un bloque para la VLAN 10 y otro para la 20.
Permite raíces distintas por VLAN y balanceo de carga, a costa de más CPU y más
BPDUs.

---

## 5. Análisis con Rapid PVST

```
Switch(config)# spanning-tree mode rapid-pvst     ! en los TRES switches
```

Se repitió **exactamente la misma prueba**: mismo ping PC0→PC2, mismo enlace
cortado (`Switch1 Gi0/1`).

**Medición real de esta simulación:**

| Evento | Hora | Resultado |
|---|---|---|
| Se corta `Switch1 Gi0/1` | `14:11:13` | — |
| **Primer** ping después del corte | `14:11:14` → | **Sent = 4, Received = 4, Lost = 0 (0% loss)** |

**¿Qué pasa con los paquetes? ¿Hay diferencia?** Sí, y es drástica: el ping
lanzado en el mismo instante del corte pasó **íntegro, sin perder un solo
paquete**. Con PVST, ese mismo ping en el mismo punto de la prueba perdía los 4.

**Por qué es tanto más rápido:** RSTP (802.1w, que es lo que Rapid PVST corre por
VLAN) no espera temporizadores, **negocia**:

1. **Respaldo precalculado.** Además de Root y Designated existen los roles
   **Alternate** (camino alternativo a la raíz, ya calculado y en espera) y
   **Backup**. Cuando el Root Port cae, el Alternate se promueve **de inmediato**,
   sin pasar por Listening ni Learning.
2. **Solo dos estados operativos:** `Discarding` y `Forwarding` (Learning es
   transitorio). Desaparecen los 15 + 15 segundos.
3. **Proposal/Agreement.** Dos vecinos sobre un enlace punto a punto acuerdan
   explícitamente pasar a Forwarding en milisegundos, en vez de esperar un
   temporizador.
4. **Cada switch origina sus propias BPDUs** cada Hello (2 s) en lugar de solo
   retransmitir las de la raíz, y **tres Hellos perdidos (6 s)** bastan para
   declarar muerto al vecino, contra los 20 s de Max Age de 802.1D.
5. **Tipos de enlace:** los puertos full-duplex se tratan como *point-to-point*
   (elegibles para el handshake rápido) y los de acceso con `portfast` como
   *edge*, que pasan a Forwarding al instante.

---

## 6. Comparación y mejoras observadas

| Aspecto | Sin STP | PVST (802.1D) | Rapid PVST (802.1w) |
|---|---|---|---|
| Bucles de capa 2 | **Sí**, tormenta de broadcast | Eliminados | Eliminados |
| Estados de puerto | — | 5 (Blk/Lis/Lrn/Fwd/Dis) | 2 (Discarding/Forwarding) |
| Detección de fallo | — | Max Age 20 s | 3 × Hello = 6 s |
| **Convergencia medida** | Nunca se estabiliza | **~25–32 s** | **imperceptible** |
| **Paquetes perdidos en la prueba** | Erráticos / todos | **4 de 4 (100%)** | **0 de 4 (0%)** |
| Uso del enlace redundante | Destructivo | Respaldo lento | Respaldo casi inmediato |

**Mejoras concretas observadas:**

1. **La tormenta de broadcast desapareció.** Con `Switch1 Gi0/2` en BLOCKING el
   anillo queda lógicamente abierto: la topología física sigue siendo un
   triángulo, pero la lógica es un árbol sin ciclos.
2. **La tabla MAC se estabilizó.** Cada MAC se aprende por un único puerto, así
   que el switching vuelve a ser eficiente en vez de inundar todo.
3. **La redundancia pasó a ser útil en vez de dañina.** El tercer enlace ya no
   rompe la red: queda de respaldo y entra en servicio solo cuando hace falta —
   demostrado al cortar `Gi0/1` y ver que la conectividad se restablece sola.
4. **Rapid PVST convirtió la redundancia en alta disponibilidad real.** Con PVST
   el respaldo existía pero tardaba tanto que una aplicación en tiempo real se
   caía igual; con Rapid PVST el corte fue invisible para el ping. Esa es la
   razón por la que **Rapid PVST es hoy el modo recomendado por defecto** en
   redes Cisco de campus.
5. **Al ser por VLAN**, se podría hacer que Switch1 sea raíz de la VLAN 10 y
   Switch2 de la VLAN 20 para repartir el tráfico entre los dos troncales en vez
   de dejar uno ocioso.

---

## 7. Comandos de verificación usados

En los switches:

```
show vlan brief                  ! VLANs creadas y puertos asignados
show interfaces trunk            ! troncales activos y VLANs permitidas
show spanning-tree vlan 10       ! raíz, roles y estados de puerto
show spanning-tree vlan 20
show spanning-tree summary       ! confirma modo pvst / rapid-pvst
show spanning-tree blockedports  ! lista directa de puertos en BLK
show spanning-tree root          ! resumen de quién es la raíz por VLAN
```

En el Command Prompt de las PCs:

```
ipconfig                         ! evidencia de la IP asignada
ping 192.168.14.11               ! desde PC0 hacia PC2 (misma VLAN 10)
ping -t 192.168.14.11            ! ping extendido durante el corte del enlace
```

**Resultados de conectividad verificados (topología final, Rapid PVST):**

| Origen | Destino | VLAN | Resultado |
|---|---|---|---|
| PC0 (192.168.14.10) | PC2 (192.168.14.11) | 10 Ventas | `Sent = 4, Received = 4, Lost = 0 (0% loss)` |
| PC1 (192.168.24.10) | PC3 (192.168.24.11) | 20 Compras | `Sent = 4, Received = 4, Lost = 0 (0% loss)` |
| PC0 (192.168.14.10) | PC1 (192.168.24.10) | 10 → 20 | `Sent = 4, Received = 0, Lost = 4 (100% loss)` — **esperado**: sin router no hay ruteo inter-VLAN, es la prueba de que la segmentación funciona |

---

## 8. Evidencias

Las capturas están en la carpeta `capturas/`, con su índice y su lectura
detallada en `capturas/EVIDENCIAS.md`. Resumen:

| # | Archivo | Qué demuestra |
|---|---------|---------------|
| 1 | `01-topologia-final.png` | Topología en triángulo con enlace redundante y direccionamiento |
| 2 | `02-vlans-switch1.png` | `show vlan brief`: VLAN 10 Ventas → Fa0/1, VLAN 20 Compras → Fa0/2 |
| 3 | `03-troncales-switch1.png` | `show interfaces trunk`: Gi0/1 y Gi0/2 en 802.1q con VLANs 1,10,20 |
| 4 | `04-switch-raiz-switch0.png` | **`This bridge is the root`** en Switch0, prioridad 4106 |
| 5 | `05-puerto-bloqueado-switch1.png` | **`Gi0/2 Altn BLK`** en Switch1 — el puerto que rompe el bucle |
| 6 | `06-ping-pc0-vlan10.png` | `ipconfig` + ping PC0→PC2 dentro de VLAN 10, 0% loss |
| 7 | `07-aislamiento-vlan-pc0.png` | Ping PC0→VLAN 20 con 100% loss: las VLANs aíslan |
| 8 | `08-ping-pc1-vlan20.png` | `ipconfig` + ping PC1→PC3 dentro de VLAN 20, 0% loss |

Los dos requisitos explícitos de la rúbrica —*"incluir capturas donde se observe
el switch raíz y los puertos bloqueados"*— corresponden a las capturas **4** y
**5** respectivamente.
