# Estado del avance — Tarea 3 (VLANs + VTP)

**Última sesión:** 28/08/2026 · **⚠️ ENTREGA: HOY**

## 🟢 Resumen rápido (28/08)

| Lección | Estado |
|---|---|
| 1 — Topología | ✅ verificada en vivo |
| 2 — Trunks | ✅ verificada (`show interfaces trunk` OK en Switch0, 4 capturas) |
| 3 — VTP | ✅ aplicada (falta captura `show vtp status`) |
| 4 — VLANs 10/20/30 | ✅ **verificada por MCP en los 4 switches** |
| 5 — Puertos de acceso | ✅ verificada (se corrigió `MERCA` Fa0/1: estaba en VLAN 10, debía ser 20) |
| 6 — IPs de las PCs | ✅ verificadas por MCP |
| 7 — Pings | ✅ **6/6 verificados por MCP** — 3 OK, 3 fallan como corresponde |
| 8 — Capturas | ✅ **23 de 23 tomadas** |
| 9 — PDF | ✅ `Manual_Tecnico.pdf` generado (~42 pág, 3.4 MB) |

**Manual_Tecnico.md corregido y limpio**: matriz llena con datos reales, secciones 12.4/12.5/13.1
nuevas, sin lenguaje de tutor. La Evidencia 19 (tabla MAC) se reescribió para describir la salida
real capturada, que muestra `0030.f296.5a01` en 4 VLANs a la vez.

### Cómo regenerar el PDF
```
scratchpad/md2html.py  +  Chrome headless --print-to-pdf
```
Requiere venv con `markdown`. Si se edita el `.md`, hay que regenerar el PDF.

### Pendientes de Julian
- `<NOMBRE COMPLETO>` y `<CARNET>` (líneas 10-11) — o borrar esa tabla si la carátula la reemplaza
- 3 valores de `Configuration Revision` en la tabla de la sección 10
- ⚠️ **Cmd+S en Packet Tracer** — el `.pkt` sigue guardado a las 17:30 y las PDUs se crearon después

### Pings verificados en vivo (28/08)

```
PC1 → 192.168.10.60  VLAN 10  ✅ 4/4      PC1 → 192.168.20.20  ❌ 100% loss
PC2 → 192.168.20.30  VLAN 20  ✅ 4/4      PC3 → 192.168.30.40  ❌ 100% loss
PC4 → 192.168.30.50  VLAN 30  ✅ 4/4      PC5 → 192.168.10.10  ❌ 100% loss
```

**La topología está funcionalmente COMPLETA y correcta.** Falta solo evidencia.

⚠️ `write memory` hecho en ADMIN/MERCA/VENTAS. **Falta confirmarlo en `Switch0`.**
✅ Typo de `VENTAS` Fa0/24 ya corregido.

---

## ✅ Lección 1 — Topología física: COMPLETA Y VERIFICADA

Verificado en vivo contra Packet Tracer (`pt_export_topology`): 11 dispositivos, 9 enlaces.

```
Switch0:Fa0/1  <-->  ADMIN:Fa0/24      (cross-over, sera trunk)
Switch0:Fa0/2  <-->  MERCA:Fa0/24      (cross-over, sera trunk)
Switch0:Fa0/3  <-->  VENTAS:Fa0/24     (cross-over, sera trunk)
ADMIN:Fa0/1    <-->  PC1               ADMIN:Fa0/2   <--> PC2
MERCA:Fa0/1    <-->  PC3               MERCA:Fa0/2   <--> PC4
VENTAS:Fa0/1   <-->  PC5               VENTAS:Fa0/2  <--> PC6
```

- Las 6 PCs se renombraron de `PC0..PC5` a `PC1..PC6`, en orden DESCENDENTE
  (`PC5->PC6`, `PC4->PC5`, ... `PC0->PC1`) para que ningún nombre destino
  estuviera ocupado al momento del cambio.
- Hay un `Power Distribution Device0` fantasma fuera del lienzo. Inofensivo, ignorar.

> ✅ **Guardado confirmado:** `Tarea_3.pkt` (61 KB, 25/08/2026 21:44).

---

## 🔵 Lección 2 — Trunks: TEORÍA DADA, FALTA TECLEAR

**Punto exacto donde retomar.** El 27/08 se dio la teoría completa; Packet Tracer
NO estaba conectado (`pt_bridge_status`: sin HTTP ni file-bridge), así que
**no se tecleó ni un comando y nada está verificado en vivo.**

### Teoría ya cubierta (no hace falta repetirla)

- **Por qué existe el trunk:** un puerto de acceso pertenece a UNA VLAN; sin trunk
  harían falta 3 cables por switch. El trunk multiplexa todas las VLANs en un cable.
- **Etiqueta 802.1Q:** 4 bytes insertados después de la MAC origen.
  TPID `0x8100` (16b) + PCP (3b) + DEI (1b) + **VLAN ID (12b → 4094 VLANs usables**,
  0 y 4095 reservadas). Se recalcula el FCS. La trama llega a 1522 B (*baby giant*).
- **Regla de oro:** la etiqueta SOLO vive dentro del trunk. El switch la agrega al
  salir por trunk y la quita al entregar a un puerto de acceso. Ningún host ve un tag.
- **VLAN nativa (pregunta que estaba pendiente — YA RESPONDIDA):** es la única VLAN
  que viaja sin etiqueta, por compatibilidad con equipos sin 802.1Q; por defecto la 1.
  Si `Switch0` tiene nativa 1 y `ADMIN` tiene nativa 99 → **VLAN hopping accidental**:
  `ADMIN` manda VLAN 99 sin tag, `Switch0` recibe sin tag y lo mete en SU nativa (la 1).
  Se rompe el aislamiento. Explotable a propósito (*double tagging*). CDP avisa con
  `Native VLAN mismatch`. En producción la nativa se mueve a una VLAN muerta ≠ 1.
  **En esta tarea se deja en 1.**
- **DTP:** dos puertos en `dynamic auto` nunca forman trunk (ambos esperan). Por eso
  forzamos `switchport mode trunk`. En producción se agrega `switchport nonegotiate`.
- **2960 no necesita** `switchport trunk encapsulation dot1q` (solo soporta 802.1Q).
  El 3560 sí lo necesita, porque también soporta ISL.

### Comandos a teclear (CLI de cada switch)

`Switch0` — los tres trunks:

```cisco
enable
configure terminal
hostname Switch0
interface FastEthernet0/1
 description TRUNK a ADMIN
 switchport mode trunk
 no shutdown
exit
interface FastEthernet0/2
 description TRUNK a MERCA
 switchport mode trunk
 no shutdown
exit
interface FastEthernet0/3
 description TRUNK a VENTAS
 switchport mode trunk
 no shutdown
exit
end
```

`ADMIN`, `MERCA`, `VENTAS` — mismo bloque, cambiando solo el hostname:

```cisco
enable
configure terminal
hostname ADMIN
interface FastEthernet0/24
 description TRUNK a Switch0
 switchport mode trunk
 no shutdown
exit
end
```

### Verificación del paso

```cisco
show interfaces trunk
```
Esperado: `Mode: on` · `Encapsulation: 802.1q` · `Status: trunking` · `Native vlan: 1`.
En `Vlans allowed on trunk` va a decir `1-1005`: correcto, las VLANs 10/20/30 todavía
no existen pero el trunk ya las permite de antemano.

📸 Captura pendiente: `evidencias/02-trunks-switch0.png`

---

## ❓ Pregunta de tutor ABIERTA (contestar al retomar)

El switch quita el tag antes de entregar a un puerto de acceso, y para saber por qué
puerto sacar la trama usa su tabla de direcciones MAC.

**¿Puede existir la misma dirección MAC en dos VLANs distintas al mismo tiempo dentro
del mismo switch?** Pista: pensá qué campos necesita realmente la tabla MAC de un
switch con VLANs para no confundirse.

---

## 📋 Lecciones que faltan

| # | Tema | Referencia en el manual |
|---|---|---|
| 2 | Trunks (teoría lista, falta teclear + verificar) | Sección 4 |
| 3 | VTP: dominio `REDES1` + modos (server/client/transparent) | Sección 5 |
| 4 | Crear VLANs 10/20/30 en `Switch0`; a mano en `VENTAS` | Sección 6 |
| 5 | Asignar puertos de acceso | Sección 7 |
| 6 | IPs de las 6 PCs (sin gateway) | Sección 8 |
| 7 | Capturas `show vtp status` / `show vlan brief` | Secciones 10 y 11 |
| 8 | Pings: 3 exitosos + 3 fallidos + prueba extra de capa 2 | Sección 12 |

---

## 🔧 Cómo retomar

1. Abrir Packet Tracer y cargar `Tarea_3.pkt` de esta carpeta.
2. `Extensions` → `MCP BUILDER` y **dejar esa ventana abierta** — sin eso no puedo
   verificar el trabajo en vivo.
3. Decir "seguimos con la Lección 2, a teclear los trunks".

> **No cerrar PT sin guardar.** El `.pkt` no se autoguarda (Cmd+S).
> **Pendiente administrativo:** el carné sigue sin darse — el manual usa `<CARNET>`.
> Entrega en la carpeta `Tarea 3` del repo `Redes1_2S_2026_CARNET`.
