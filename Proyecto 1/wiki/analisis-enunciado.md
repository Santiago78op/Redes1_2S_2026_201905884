# Análisis del enunciado — Proyecto 1 "SmartCity Tech Park"

> **Para Claude Code en cualquier máquina.** Este archivo es autocontenido: resume el enunciado oficial (`../doc/0972_Proyecto_1_2S2026.pdf`), los parámetros que me tocan por carné, lo que exige cada área, los entregables, las ambigüedades detectadas y las decisiones de diseño propuestas. Si el PDF no está en esta máquina, este documento basta para trabajar. Vive en `Proyecto 1/wiki/`, carpeta versionada: viaja con el repo.
>
> Generado el 2026-09-07 a partir de la conversión con markitdown + pdfplumber del PDF (11 páginas) y de la lectura visual de la página 10 rasterizada con pypdfium2.

## 1. Ficha del proyecto

| Ítem | Valor |
|---|---|
| Curso | Redes de Computadoras 1, USAC, Facultad de Ingeniería, Ing. en Ciencias y Sistemas, 2S-2026 |
| Estudiante | Santiago Barrera, carné **201905884** |
| Ponderación / tiempo | **22 pts** / 35 h estimadas |
| Cronograma | Asignación 28/08/2026 · Elaboración 28/08 → **17/09/2026** · Calificación 18–19/09/2026 |
| Repositorio | `Redes1_2S_2026_201905884` (el mismo de la práctica), carpeta **`Proyecto 1/`** |
| Entrega | Plataforma UEDI o Classroom; otro medio se anula |
| Herramientas obligatorias | Cisco Packet Tracer ≥ 8.0 · GitHub · editor Markdown |
| Entregables | `Proyecto1_201905884.pkt` + Manual Técnico `README.md` en Markdown |

## 2. Estado de integridad del PDF (hallazgo importante)

El índice del documento (pág. 2) anuncia 15 páginas de contenido, pero el archivo tiene **11**. Verificación hecha buscando cada término en las 11 páginas:

| Sección anunciada | Página según índice | Página real | Estado |
|---|---|---|---|
| 1–5 (marco, objetivo, resumen, enunciado, material) | 3–9 | 3–10 | Completas; el índice va corrido ~1 página |
| 6. Metodología | 10 | 10 | **Encabezado sin contenido**: solo la frase introductoria; no hay lista ni figura (se rasterizó la página para confirmarlo) |
| 7. Cronograma | 10 | 10 | Completa |
| 8. / 8.1 Requisitos para optar a la calificación | 10 | 11 | Completa; es la última página |
| **8.2 Detalle de la Calificación** | 12 | — | **Ausente**: el texto "8.2" y "Detalle de la Calificación" solo existen en la página del índice |
| **8.3 Comentarios Generales** | 15 | — | **Ausente**, misma evidencia |

Conclusión: la numeración del índice está desfasada (como se sospechó), **y además** las secciones 8.2 y 8.3 no están en el archivo. Se desconoce cómo se reparten los 22 puntos. **Acción:** pedir al tutor la versión completa o la rúbrica detallada; mientras, priorizar según la lista de entregables de §4.5, que es lo único que la rúbrica visible referencia.

## 3. Parámetros derivados del carné 201905884

Carné `2019058` **8** **4** → penúltimo dígito **# = 8**, último dígito **X = 4** (par). No seguir este esquema penaliza **del -50 % al -100 %** (§8.1).

| Parámetro | Regla del enunciado | Valor para mí |
|---|---|---|
| VLAN Gerencia (Edificio Corporativo) | `1X` | **14** |
| VLAN Investigacion (Centro de I+D) | `2X` | **24** |
| VLAN Produccion (Planta de Producción) | `3X` | **34** |
| VLAN Servidores (Centro de Datos) | `4X` | **44** |
| VLAN Visitantes (Edificio Corporativo, Áreas Comunes) | `5X` | **54** |
| VLAN nativa de todos los trunks | `9X` | **94** |
| Dominio VTP | `Smart_#` | **`Smart_8`** |
| Contraseña VTP | fija | **`proyecto12S2026`** |
| EtherChannel | LACP si par, PAgP si impar | **LACP** |
| STP | PVST si par, Rapid-PVST si impar | **PVST** (`spanning-tree mode pvst`) |
| Banner MOTD en switches de distribución | `Acceso Restringido - TechPark_[Carné]` | **`Acceso Restringido - TechPark_201905884`** |
| Nombre del archivo | `Proyecto1_#carnet.pkt` | **`Proyecto1_201905884.pkt`** |

Nombres de VLAN: la tabla oficial los escribe `Gerencia`, `Investigacion`, `Produccion`, `Servidores`, `Visitantes` (sin tildes); el ejemplo del enunciado dice que el nombre "debe ser exactamente **GERENCIA**". Ver ambigüedad A2.

## 4. El problema que se resuelve (§3 y §4.1)

El complejo SmartCity Tech Park creció (I+D, Planta automatizada, Edificio Corporativo) con una **red plana**: maquinaria Legacy, servidores críticos e invitados comparten un dominio de broadcast; el segmento industrial arrastra **un único dominio de colisión**; hay enlaces saturados y **rutas únicas** cuya falla deja sin servicio a áreas críticas. Se pide rediseñar **Capa 1 y Capa 2**: fragmentar dominios de colisión, limitar el broadcast con VLANs, agregar capacidad (EtherChannel) y tolerancia a fallos (redundancia + STP).

## 5. Requerimientos por área (§4.2) y alcance obligatorio (§4.3)

### 5.1 Centro de Datos (Core)
- Núcleo de la jerarquía; **administración centralizada del dominio VTP** → switch **VTP Server**.
- Enlaces **troncales** hacia los switches de distribución de los otros 3 edificios.
- Granja de **≥ 4 servidores críticos** conectada por un enlace de **alto volumen de tráfico** que **no dependa de una única conexión física** → EtherChannel LACP.
- Cantidad de switches intermedios y forma de resolverlo: a criterio, justificado.

### 5.2 Centro de I+D
- Área crítica de **alta disponibilidad**: **≥ 3 switches interconectados entre sí**, de modo que la caída de uno no aísle a los demás (anillo/triángulo con STP).
- Su trunk al Core debe soportar **más ancho de banda que el resto de los troncales** del campus (el "enlace gordo").
- **≥ 8 estaciones de trabajo** (PCs/laptops).

### 5.3 Edificio Corporativo
- Personal administrativo (VLAN 14) + invitados (VLAN 54); en conjunto, uno de los mayores volúmenes de tráfico del campus.
- **Al menos dos alas**, cada una con su **switch de acceso**; la conectividad entre alas debe **mantenerse aunque la ruta al distribuidor más cercano quede inhabilitada** → enlace directo entre alas (triángulo) con STP.
- **Áreas Comunes** para visitantes: **aislar completamente el tráfico y la administración de VLANs** del resto del campus; servicio **inalámbrico** a laptops de invitados con un **Access Point**.

### 5.4 Planta de Producción (Legacy)
- Maquinaria y protocolos antiguos; no se puede migrar.
- Debe evidenciar **un dominio de colisión compartido en Capa 1**: un **hub** con las máquinas, conectado a **un switch de acceso**.
- El Manual debe documentar el **impacto** de ese dominio compartido sobre el rendimiento y las **medidas de contención a nivel de switch de acceso** que lo mitigan **sin eliminar** el segmento Legacy.

### 5.5 Reglas transversales
- **Topología jerárquica**: un switch central en el Centro de Datos + trunks a los 3 distribuidores.
- **Medio de transmisión** de cada enlace (cobre o fibra) **seleccionado y justificado** por distancia, ancho de banda y buenas prácticas; **etiquetado** en el `.pkt`.
- **VTP** con el modo de cada switch **según su rol** (Server / Client / Transparent).
- **VLANs** creadas en el Server y **propagadas por VTP**.
- **EtherChannel** donde el diseño lo requiera (LACP).
- **STP** PVST; **Root Bridge por VLAN** a criterio, **justificado** en el Manual.
- **Seguridad básica**: banner MOTD en distribución; **VLAN nativa 94** en todos los trunks (en vez de la 1).

### 5.6 Alcance opcional (sin puntaje declarado)
Usar el **Modo Simulación** de Packet Tracer filtrando STP y VTP: capturar y abrir una **BPDU** (señalar Root ID, Bridge ID y costo) y una **PDU de VTP** (señalar VTP Domain Name y Configuration Revision Number).

### 5.7 Parte física (laboratorio, por pareja)
Dos switches reales, uno por estudiante: **Switch 1 en VTP Server** (Core) y **Switch 2 en VTP Client** (distribución/acceso). Obligatorio: crear y nombrar las VLANs por carné en el Server y verificar la **propagación automática** al Client; puerto de interconexión en **trunk** permitiendo las VLANs; puertos a dispositivos finales en **access** con su VLAN.

## 6. Entregables del Manual Técnico (§4.5) — checklist

- [ ] Capturas de la **topología completa** y de **cada área**.
- [ ] **Tabla de dominios de colisión**: cuántos genera cada switch (según puertos activos) y cuál es el dominio compartido del segmento Legacy.
- [ ] **Tabla de dominios de broadcast**: uno por cada VLAN activa.
- [ ] **Lista de comandos** utilizados, **por dispositivo**.
- [ ] **Tabla de VLANs** (ID, nombre).
- [ ] **Tabla de asignación de puertos por switch**.
- [ ] Captura + **justificación del switch Server de VTP**.
- [ ] Captura + **justificación del Root Bridge para cada VLAN**.
- [ ] Captura + **justificación de los EtherChannel** utilizados.
- [ ] **Evidencia de pruebas**: `show spanning-tree`, `show etherchannel summary`, `show interfaces trunk`.
- [ ] **Etiquetado de medios** en el `.pkt` + **justificación** del medio por segmento en el Manual.
- [ ] **Presupuesto** estimado de los equipos simulados: switches, módulos de fibra, cableado UTP y fibra.
- [ ] Impacto y **medidas de contención** del segmento Legacy (lo exige §4.2).
- [ ] (Opcional) Capturas de BPDU y PDU VTP con los campos señalados.

## 7. Requisitos para optar a nota (§8.1) — si falla uno, la nota es 0

| Tema | Exigencia |
|---|---|
| Repositorio oficial | El mismo de la práctica, carpeta **"Proyecto 1"** con los entregables. (El texto escribe `Redes1_1S_2026_Carnet`; es un error tipográfico, el curso es 2S.) |
| Formato de entrega | UEDI o Classroom; entregas por otro medio se anulan. |
| Documentación obligatoria | Manual Técnico en Markdown dentro de la carpeta. |
| Uso de VLANs | Seguir el esquema por carné; si no, penalización **-50 % a -100 %**. |
| Originalidad | VLANs, nativa y protocolos según carné; decisiones de diseño (dónde va la redundancia, cuál es el enlace de mayor capacidad, medio, Root Bridge) **propias y justificadas**. Una topología idéntica a la de otro estudiante **es copia** aunque cambien los parámetros. |

## 8. Ambigüedades detectadas y decisiones

| # | Hallazgo | Decisión / acción |
|---|---|---|
| A1 | PDF sin §8.2 ni §8.3; §6 vacía (ver §2). | Pedir versión completa. Priorizar por la lista de §4.5. |
| A2 | Nombre de VLAN `Gerencia` (tabla) vs "exactamente GERENCIA" (ejemplo). | Preguntar al tutor; sin respuesta, usar **MAYÚSCULAS** (es lo que el texto enfatiza). |
| A3 | Repo `Redes1_1S_2026_Carnet` en §8.1 vs curso 2S. | Mantener `Redes1_2S_2026_201905884`; el texto dice "el mismo repositorio de la práctica". |
| A4 | Áreas Comunes debe aislar "la administración de VLANs", pero la VLAN 54 debe crearse en el Server y propagarse. | Switch de Áreas Comunes en **VTP Transparent** con la VLAN 54 creada localmente: no adopta la base del dominio, pero reenvía anuncios. Justificar. |
| A5 | Banner "en todos los switches de distribución": ¿Core y acceso también? | Configurarlo en distribución **y** Core; decidir si también en acceso (no penaliza tener más). |
| A6 | Dos enlaces "de alto tráfico": servidores→Core e I+D→Core. | Servidores: EtherChannel (redundancia + capacidad). I+D: el trunk **más ancho del campus** (EtherChannel o Gigabit por fibra frente a Fast/cobre en el resto). Justificar por separado. |
| A7 | "PVST" en Cisco IOS es PVST+. | Comando `spanning-tree mode pvst`; aclararlo en el Manual. |
| A8 | Alcance opcional sin puntaje. | Solo si sobra tiempo; sirve para la defensa. |
| A9 | Parte física: sin fecha ni instrucción de documentarla. | Confirmar fecha y pareja; incluir `show` y fotos en el README por si acaso. |
| A10 | Presupuesto sin moneda ni fuente. | Cotizar en USD con referencias públicas, como en la Práctica 1. |

## 9. Propuesta de diseño (borrador, pendiente de cerrar y justificar)

| Área | Propuesta |
|---|---|
| Core | 1 switch Core (VTP Server, Root Bridge de la mayoría de VLANs) + 1 switch de servidores (VLAN 44) unido al Core por **EtherChannel LACP de 2 enlaces**. |
| I+D | 1 distribuidor + 3 switches de acceso en **anillo** (cada uno con dos caminos); ≥ 8 PCs en VLAN 24; trunk al Core por **EtherChannel LACP** o Gigabit en fibra = enlace de mayor capacidad. Root de la VLAN 24: por decidir (Core o distribuidor de I+D). |
| Corporativo | 1 distribuidor (banner) + Ala A + Ala B (VLAN 14) con **enlace directo Ala A↔Ala B**; switch de Áreas Comunes en **VTP Transparent**, VLAN 54, con **Access Point** y laptops inalámbricas. |
| Planta | 1 switch de acceso (VLAN 34) con un **hub** de máquinas en un solo puerto; contención: `storm-control broadcast`, `port-security maximum`, confinamiento a la VLAN 34. |
| Medios | **Fibra** en los troncales entre edificios (distancia > 100 m, mayor ancho de banda, inmunidad electromagnética en la Planta); **UTP Cat 6/6A** dentro de cada edificio. En Packet Tracer, la fibra requiere módulos SFP (p. ej. `GLC-LH-SMD` en 3560/3650) o el módulo de fibra del switch genérico. |
| STP | `spanning-tree mode pvst`; Core `root primary` para 14/34/44/54; Root de la 24 por decidir. |

Diagrama borrador:

```mermaid
flowchart TD
    CORE[Core · VTP Server]
    SRV[Sw Servidores · VLAN 44] ==LACP== CORE
    CORE ==LACP / fibra== DID[Dist I+D]
    CORE --fibra--> DCO[Dist Corporativo · MOTD]
    CORE --fibra--> DPR[Sw Acceso Planta · VLAN 34]
    DID --- A1[Sw I+D 1] --- A2[Sw I+D 2] --- A3[Sw I+D 3] --- A1
    DCO --- ALA[Ala A · VLAN 14] --- ALB[Ala B]
    DCO --- ALB
    DCO --- AC[Areas Comunes · VTP Transparent · VLAN 54] --> AP((AP))
    DPR --> HUB{{Hub Legacy}}
```

## 10. Plan de trabajo (la §6 del PDF está vacía; este es el propio)

| Fase | Contenido | Meta |
|---|---|---|
| 0 Dudas | PDF completo, nombre de VLAN, fecha de lab | 08/09 |
| 1 Diseño en papel | Bosquejo por área, tabla de switches (rol, modo VTP), tabla de puertos, medio por enlace, Root por VLAN | 09/09 |
| 2 Capa 1 en PT | Dispositivos, cableado, etiquetas de medios, hub, AP | 10/09 |
| 3 VTP + VLANs | Server `Smart_8`, Clients/Transparent, 5 VLANs, trunks con nativa 94, access | 11/09 |
| 4 Redundancia | EtherChannel LACP, PVST con Root por VLAN, verificar bloqueos | 12/09 |
| 5 Pruebas | ping intra-VLAN, aislamiento inter-VLAN, fallas simuladas, los tres `show` | 13/09 |
| 6 Manual | README con todas las tablas, capturas, comandos, presupuesto | 14–16/09 |
| 7 Lab + entrega | Switches reales con la pareja; subir a repo y UEDI | ≤ 17/09 |

Reglas: cada comando ejecutado se copia al README en el momento, por dispositivo; el `.pkt` se versiona localmente por fase; toda decisión se anota con su porqué al tomarla.

## 11. Comandos Cisco IOS con los valores ya sustituidos

```
! Identidad y banner (distribución y Core)
hostname SW-CORE
banner motd #Acceso Restringido - TechPark_201905884#

! VTP — Core
vtp mode server
vtp domain Smart_8
vtp password proyecto12S2026
vtp version 2
! VTP — resto del campus: vtp mode client (mismo dominio y contraseña)
! VTP — Áreas Comunes: vtp mode transparent

! VLANs (solo en el Server)
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

! Trunk (ambos extremos iguales)
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk native vlan 94
 switchport trunk allowed vlan 14,24,34,44,54,94
! En 3560/3650 agregar antes: switchport trunk encapsulation dot1q

! Access
interface range FastEthernet0/1 - 8
 switchport mode access
 switchport access vlan 24
 spanning-tree portfast

! Puerto hacia el hub Legacy (contención)
interface FastEthernet0/24
 switchport mode access
 switchport access vlan 34
 storm-control broadcast level 20
 switchport port-security
 switchport port-security maximum 4
 switchport port-security violation restrict

! EtherChannel LACP (ambos extremos)
interface range GigabitEthernet0/1 - 2
 channel-group 1 mode active
interface Port-channel 1
 switchport mode trunk
 switchport trunk native vlan 94
 switchport trunk allowed vlan 14,24,34,44,54,94

! STP
spanning-tree mode pvst
spanning-tree vlan 14,34,44,54 root primary      ! en el Core
spanning-tree vlan 24 root secondary             ! en el Core, si el Root de la 24 es I+D

! Verificación / evidencia
show vlan brief
show vtp status
show interfaces trunk
show spanning-tree
show etherchannel summary
show running-config
copy running-config startup-config
```

## 12. Material de apoyo del enunciado (§5)

| Recurso | URL |
|---|---|
| Cisco — VLANs and Trunks (Catalyst 9000) | https://www.cisco.com/c/en/us/td/docs/switches/lan/c9000/lyr2-fwd/vlan/vlan-configuration-guide/configure-vlan-trunks.html |
| Cisco — VLAN Trunking Protocol (VTP), doc 10558 | https://www.cisco.com/c/en/us/support/docs/lan-switching/vtp/10558-21.html |
| Cisco — Configuring Spanning Tree (Catalyst 2960) | https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst2960/software/release/12-2_53_se/configuration/guide/2960scg/swstp.html |
| Cisco — Configuring EtherChannels (Catalyst 2960) | https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst2960/software/release/12-2_53_se/configuration/guide/2960scg/swethchl.html |
| NetAcad — Packet Tracer, Modo Simulación | https://www.netacad.com/ |

## 13. Dónde está el resto del material

- `Proyecto 1/CLAUDE.md`: versión corta de este análisis que Claude Code carga automáticamente.
- Cerebro diamon `redes` (`C:\mcp\brains\personal\redes`, **solo en la PC principal**): las mismas ideas repartidas en 16 notas enlazadas, con conceptos ampliados (dominios, VLAN/802.1Q, VTP, STP/PVST, EtherChannel/LACP) y glosario.
- Estilo del Manual a imitar: `../Practica1/ManualTecnico.md`.
