# Evidencias de la Actividad Práctica 3 — STP

**Carné:** 201905884 · **X = 4** · **Archivo:** `APT3_201905884_STP.pkt`
**Modo STP del archivo entregado:** Rapid PVST (`protocol rstp` en la salida)

Todas las capturas se tomaron sobre la simulación corriendo en Packet Tracer, en
resolución completa de la ventana. Cada una es la ventana del dispositivo, así que
en la barra de título se ve **de qué equipo salió cada salida**.

---

| # | Archivo | Dispositivo | Comando | Qué evidencia |
|---|---------|-------------|---------|---------------|
| 1 | `01-topologia-final.png` | — | — | Topología en triángulo, direccionamiento y anotaciones |
| 2 | `02-vlans-switch1.png` | Switch1 | `show vlan brief` | VLAN 10 Ventas → Fa0/1, VLAN 20 Compras → Fa0/2 |
| 3 | `03-troncales-switch1.png` | Switch1 | `show interfaces trunk` | Gi0/1 y Gi0/2 en 802.1q transportando VLANs 1,10,20 |
| 4 | `04-switch-raiz-switch0.png` | Switch0 | `show spanning-tree vlan 10` | **`This bridge is the root`**, prioridad 4106 |
| 5 | `05-puerto-bloqueado-switch1.png` | Switch1 | `show spanning-tree vlan 10` | **`Gi0/2  Altn  BLK`** — el puerto que rompe el bucle |
| 6 | `06-ping-pc0-vlan10.png` | PC0 | `ipconfig` + `ping 192.168.14.11` | IP 192.168.14.10 y ping a PC2 con **0% loss** |
| 7 | `07-aislamiento-vlan-pc0.png` | PC0 | `ping 192.168.24.10` | Ping a la otra VLAN con **100% loss** → las VLANs sí aíslan |
| 8 | `08-ping-pc1-vlan20.png` | PC1 | `ipconfig` + `ping 192.168.24.11` | IP 192.168.24.10 y ping a PC3 con **0% loss** |

---

## Lo que hay que saber leer de cada captura

### 4 — Switch raíz (la que más pesa en la rúbrica)

```
VLAN0010
  Spanning tree enabled protocol rstp
  Root ID    Priority    4106
             Address     000D.BD3E.13D4
             This bridge is the root          ← LA EVIDENCIA
  Bridge ID  Priority    4106  (priority 4096 sys-id-ext 10)
             Address     000D.BD3E.13D4
Interface   Role Sts Cost   Prio.Nbr Type
Gi0/1       Desg FWD 4      128.25   P2p
Gi0/2       Desg FWD 4      128.26   P2p
```

`4106 = 4096` (la prioridad que se configuró) `+ 10` (el ID de la VLAN). Los dos
puertos de la raíz salen `Desg FWD`: **una raíz nunca bloquea nada**.

### 5 — Puerto bloqueado

```
  Root ID    Priority    4106
             Address     000D.BD3E.13D4      ← la MAC de Switch0, no la propia
             Cost        4
             Port        25(GigabitEthernet0/1)
  Bridge ID  Priority    32778  (priority 32768 sys-id-ext 10)
             Address     0010.1173.4E32      ← la MAC de Switch1

Interface   Role Sts Cost   Prio.Nbr Type
Fa0/1       Desg FWD 19     128.1    P2p
Gi0/1       Root FWD 4      128.25   P2p
Gi0/2       Altn BLK 4      128.26   P2p     ← EL PUERTO BLOQUEADO
```

Dos cosas en la misma pantalla: Switch1 **reconoce a Switch0 como raíz** (Root ID
≠ Bridge ID) y **`Gi0/2` está en `Altn/BLK`**. En Switch0 y Switch2 no hay ningún
`BLK` — por eso esta captura es de Switch1.

Por qué le tocó a Switch1: Switch1 y Switch2 tienen el mismo costo hacia la raíz
(4), así que desempata el Bridge ID, y el MAC de Switch2 (`0001.4298.2D34`) es
menor que el de Switch1 (`0010.1173.4E32`).

### 6 y 7 — Conectividad y segmentación

La 6 trae `ipconfig` y el ping en la misma pantalla, que es como lo pide el
enunciado. La 7 es el complemento que demuestra que las VLANs **sí** están
segmentando: el mismo PC0 alcanza a PC2 (su VLAN) con 0% de pérdida y no alcanza
a PC1 (otra VLAN) con 100% — no hay router haciendo inter-VLAN, así que ese
timeout es el resultado correcto, no una falla.

---

## Si el catedrático pide también la fase 1 (PVST)

El `.pkt` quedó guardado en **Rapid PVST**, que es la fase 2. Para mostrar la
fase 1, en los **tres** switches:

```
enable
configure terminal
 spanning-tree mode pvst
end
```

y volver a capturar. Para regresar: `spanning-tree mode rapid-pvst`. El bloque
listo para pegar está en `configs/Cambio-a-RapidPVST.txt`.

> Ojo: cambiar el modo obliga a recalcular el árbol; esperá ~30 s antes de
> capturar o `show spanning-tree` sale a medio converger.

---

## Pendiente antes de subir

- [ ] Confirmar el **formato de nombre del archivo**. El PDF da 10 pts por ese
      criterio pero nunca dice cuál es. Ahora está como `APT3_201905884_STP.pkt`;
      si en clase pidieron otro formato, renombralo.
- [ ] Subir el `.pkt`, `Explicacion-STP.md` y esta carpeta `capturas/`.
