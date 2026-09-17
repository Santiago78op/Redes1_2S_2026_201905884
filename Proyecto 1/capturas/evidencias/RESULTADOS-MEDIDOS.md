# Evidencias E1–E14 — resultados MEDIDOS en el simulador

**Fecha:** 2026-09-16 · **Archivo:** `Proyecto1_201905884.pkt` · **Carné:** 201905884

> Esto es lo que **devolvió el simulador**, transcrito tal cual. Donde el resultado contradijo al
> Manual, se corrigió el Manual y se anotó qué cambió.
> Las capturas de pantalla de estas pruebas están en esta misma carpeta (índice en `../EVIDENCIAS.md`); acá queda el dato medido.

## Direccionamiento usado para las pruebas

El proyecto es de **Capa 2 pura** y el Manual no definía direccionamiento, así que se asignó uno
coherente con los IDs de VLAN, **sin gateway y sin router**: eso es justamente lo que hace que
E10 y E11 fallen, que es el resultado correcto.

| VLAN | Red | Equipos |
|---|---|---|
| 14 GERENCIA | `192.168.14.0/24` | PC-GER-1…6 = `.11`–`.16` |
| 24 INVESTIGACION | `192.168.24.0/24` | PC-ID-1…8 = `.11`–`.18` |
| 34 PRODUCCION | `192.168.34.0/24` | PC-MAQ-1…4 = `.11`–`.14` · PC-SUP-1 = `.21` · PC-SUP-2 = `.22` |
| 44 SERVIDORES | `192.168.44.0/24` | SRV-WEB `.11` · SRV-BD `.12` · SRV-ARCHIVOS `.13` · SRV-DNS `.14` |
| 54 VISITANTES | `192.168.54.0/24` | PC-VIS-1 `.11` · LAP-VIS-1…3 = `.21`–`.23` |

## E9 — Ping intra-VLAN entre switches distintos ✅

`PC-GER-1 (192.168.14.11, SW-ALA-A) → PC-GER-4 (192.168.14.14, SW-ALA-B)`

```
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

**Demuestra** que la VLAN 14 atraviesa los trunks y que dos alas distintas son el mismo dominio de
broadcast. Coincide con lo previsto.

## E10 — Ping inter-VLAN ✅ (falla, y ESO es lo correcto)

`PC-GER-1 (VLAN 14) → SRV-BD (192.168.44.12, VLAN 44)`

```
Packets: Sent = 4, Received = 0, Lost = 4 (100% loss)
```

**Demuestra** el aislamiento entre VLANs: sin dispositivo de Capa 3 no hay tránsito entre ellas.
Un 0 % de pérdida acá sería un **error de diseño**, no un éxito.

## E11 — Aislamiento de visitantes ✅ (falla, y ESO es lo correcto)

`PC-VIS-1 (192.168.54.11, VLAN 54) → SRV-BD (192.168.44.12, VLAN 44)`

```
Packets: Sent = 4, Received = 0, Lost = 4 (100% loss)
```

**Demuestra** que las tres medidas de Áreas Comunes funcionan: VLAN 54 separada, VTP Transparent y
el trunk restringido a `allowed vlan 1,54,94`.

## E12 — Caída de SW-ID-2 ✅ mejor que lo estimado

`PC-ID-1 (192.168.24.11, SW-ID-1) → PC-ID-7 (192.168.24.17, SW-ID-3)`

| Momento | Resultado |
|---|---|
| **Antes** | `Sent = 4, Received = 4, Lost = 0 (0% loss)` |
| **Con SW-ID-2 apagado** | `Sent = 4, Received = 4, Lost = 0 (0% loss)` |

**Estimado inicialmente: 30–50 s de convergencia. Medido: interrupción nula.**

**Por qué, y por qué es una buena noticia:** el camino SW-ID-1 ↔ SW-ID-3 **nunca pasaba por
SW-ID-2**, porque los dos tienen uplink propio a SW-DIST-ID. La predicción suponía que el tráfico
cruzaba el anillo. Es decir: **la decisión de poner dos uplinks en vez de uno hace que la caída de
SW-ID-2 ni siquiera requiera reconvergencia de STP.** §24.2 del Manual se corrigió con esta
medición. Lo que sí queda sin servicio son las PC colgadas de SW-ID-2
(PC-ID-4, 5 y 6), que es inevitable y esperado.

## E13 — Caída del uplink del Ala B ✅ coincide con lo previsto

`SW-ALA-B Gi0/1 shutdown` · `PC-GER-1 → PC-GER-4`

| Momento | Resultado |
|---|---|
| **Durante** | `Sent = 4, Received = 0, Lost = 4 (100% loss)` |
| **Reconvergiendo** | `Sent = 4, Received = 2, Lost = 2 (50% loss)` ← el enlace vuelve a mitad del ping |
| **Después** | `Sent = 4, Received = 4, Lost = 0 (0% loss)` |

**Demuestra** que el enlace directo entre alas asume el tráfico cuando cae la ruta al distribuidor,
y que el tiempo de recuperación es el de **PVST+ (~30–50 s)**, no instantáneo. La secuencia
100 % → 50 % → 0 % es la firma de una reconvergencia de STP en curso.

## E14 — Caída de un miembro de Po1 ✅ recuperación inmediata

`SW-CORE Gi1/1 shutdown` (un miembro del EtherChannel hacia SW-SRV)

| Momento | SW-CORE | SW-SRV |
|---|---|---|
| **Antes** | `Po1 up` · `Gi0/1 up` · `Gi1/1 up` | — |
| **Durante** | **`Po1 up`** · `Gi0/1 up` · `Gi1/1 DOWN` | **`Po1 up`** · `Gi0/1 up` · `Gi0/2 DOWN` |
| **Después** | `Po1 up` · `Gi0/1 up` · `Gi1/1 up` | — |

**Demuestra la diferencia de fondo entre las dos redundancias del diseño:** el canal **no se cae**
al perder un miembro y **no hay reconvergencia de STP**, porque para STP `Po1` sigue siendo **un
solo enlace lógico** que nunca desapareció. Frente a los ~30–50 s de E13, acá la recuperación es
inmediata. Si esta prueba tardara 30 s, significaría que el EtherChannel **no se formó**.

---

## Segunda sesión (2026-09-16, tarde): E1–E8 y repetición de E9–E14 con captura

Las salidas se leyeron de la consola de cada switch y las capturas se tomaron de la ventana de cada
equipo en Packet Tracer, con su nombre en la barra de título. En estos chasis no existe
`terminal length 0`, así que los `--More--` se avanzaron a mano.

### E1–E8 — salidas leídas en los 11 switches

| Ev. | Lo que devolvió el simulador |
|---|---|
| **E1** | SW-CORE: `VTP Operating Mode : Server` · `VTP Domain Name : Smart_8` · `VTP Version : 2` · `Configuration Revision : 29` |
| **E2** | SW-ALA-A (`Client`, revisión 29): `14 GERENCIA`, `24 INVESTIGACION`, `34 PRODUCCION`, `44 SERVIDORES`, `54 VISITANTES`, `94 NATIVA`, `999 SIN-USO`. Los 9 Client tienen revisión 29; SW-COMUNES está en `Transparent`, revisión 0 |
| **E3** | Raíces: VLAN 14 y 54 → SW-DIST-CORP (`24590`, `24630`); VLAN 24 → SW-DIST-ID (`24600`); VLAN 34 y 44 → SW-CORE (`24610`, `24620`). **Las cinco coinciden con §18** |
| **E4** | VLAN 14: `SW-ALA-B Gi0/2 Altn BLK 4`. VLAN 24: `SW-ID-3 Fa0/24 Altn BLK 19` y `SW-ID-2 Gi0/2 Altn BLK 4`. **Los tres coinciden con §18** |
| **E5** | SW-CORE: `Po1(SU) LACP Gig0/1(P) Gig1/1(P)` · `Po2(SU) LACP Gig2/1(P) Gig3/1(P)`. SW-SRV: `Po1(SU) Gig0/1(P) Gig0/2(P)`. SW-DIST-ID: `Po2(SU) Gig0/1(P) Gig1/1(P)` |
| **E6** | SW-CORE: `Po1 1,44,94` · `Po2 1,24,94` · `Gig4/1 1,14,54,94` · `Gig5/1 1,34,94`, todos con `Native vlan 94` |
| **E7** | Tras `exit`, al volver a entrar a SW-DIST-CORP: `Acceso Restringido - TechPark_201905884` |
| **E8** | SW-PLANTA `Gi4/1`: `Secure-up` · `Restrict` · máximo 5 · `Sticky MAC Addresses : 1` (tras la corrección de abajo) |

### Discrepancias encontradas al comparar configuración real y Manual

Se compararon los 11 `running-config` con §23 **en las dos direcciones**. Manda el simulador:

| Hallazgo | Resolución |
|---|---|
| `spanning-tree portfast` + `bpduguard enable` aplicados en 21 puertos de PC y servidores (y sólo `portfast` en el AP y el hub), pero §22 decía «BPDU Guard no implementado» | Se corrigieron §22, §23 y §27 |
| `switchport port-security mac-address sticky` **faltaba** en `Gi4/1` de SW-PLANTA | Se aplicó, `write memory` y se guardó el `.pkt` (161 865 bytes). Reabierto el archivo, la línea sigue ahí |
| `storm-control action trap` **no existe** en Packet Tracer (la ayuda sólo ofrece `broadcast`) | Queda comentado en §23.11 |
| `interface range FastEthernet2/1 - 3` → `command rejected` | Se reemplazó por `FastEthernet2/1 , FastEthernet3/1`, aceptado |
| `no ip domain-lookup` ausente en los 4 chasis modulares: SW-PLANTA intentó resolver por DNS un `end` mal ubicado | Sin efecto en la red; anotado en §23 |

### Repetición de E9–E14 con captura

Los resultados **coinciden con la primera medición** y agregan tiempos más finos:

| Ev. | Resultado de esta sesión |
|---|---|
| **E9** | `Sent = 4, Received = 4, Lost = 0 (0% loss)` |
| **E10** | `Sent = 4, Received = 0, Lost = 4 (100% loss)` |
| **E11** | `Sent = 4, Received = 0, Lost = 4 (100% loss)` |
| **E12** | SW-ID-2 apagado: PC-ID-1 → PC-ID-7 **0 %**; PC-ID-1 → PC-ID-4 **100 %**. Al encenderlo, PC-ID-4 vuelve: 100 % a los 32 s, 25 % a los 47 s y 0 % a los 57 s (incluye el arranque del switch) |
| **E13** | `shutdown` en `Gi0/1` de SW-ALA-B: inmediatamente `Gi0/2 Root LIS`, y el ping lanzado a continuación terminó a los 26 s con 100 %; la siguiente lectura, a los 42 s, dio `Gi0/2 Root FWD`, y el ping de ese momento 50 %; el siguiente, 0 %. Al restaurar, `Gi0/1` recorrió `LIS → LRN → FWD` en unos 35 s y `Gi0/2` volvió a `BLK` |
| **E14** | `shutdown` en `Gi1/1` de SW-CORE: `Po1(SU) Gig0/1(P) Gig1/1(D)`, y en la VLAN 44 `Po1 Desg FWD` con costo **4** (antes 3). Al levantarlo, `Gig1/1(P)` a los 4 s, **pero `Po1 Desg LIS 3`**: la reincorporación del miembro hizo que el simulador volviera a pasar `Po1` por Listening. Minutos después, `FWD` |

**Estado final verificado.** Después de las tres fallas, los 11 switches tienen la configuración del
mismo tamaño en bytes que antes de empezar, las mismas raíces y los mismos puertos bloqueados, y los
dos canales en `(SU)` con los cuatro miembros en `(P)`.
