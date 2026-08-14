# Manual Técnico — Práctica 1: QuetzalDev S.A.

**Universidad de San Carlos de Guatemala** · Facultad de Ingeniería
**Curso:** Redes de Computadoras 1 — Segundo Semestre 2026
**Estudiante:** Santiago Barrera
**Carné:** 201905884
**Plano asignado:** Plano 3 (carnés con terminación 4-5)
**Fecha:** <!-- COMPLETAR -->

---

> **NOTA DE TRABAJO — BORRAR ANTES DE ENTREGAR**
> Los datos marcados **(fijo)** vienen del enunciado o del plano y no se discuten.
> Todo lo marcado `<!-- COMPLETAR -->` o `[…]` es decisión tuya y debe llevar justificación propia.
> La rúbrica penaliza justificaciones repetidas: no copies la misma frase en las 8 filas de una tabla.

---

## Índice

1. [Introducción y alcance](#1-introducción-y-alcance)
2. [Datos base del edificio](#2-datos-base-del-edificio)
3. [Distribución de hosts por departamento](#3-distribución-de-hosts-por-departamento)
4. [Inventario de equipos](#4-inventario-de-equipos)
5. [Ubicación y justificación del MDF](#5-ubicación-y-justificación-del-mdf)
6. [Topología física por departamento](#6-topología-física-por-departamento)
7. [Puntos de red y tipos de toma](#7-puntos-de-red-y-tipos-de-toma)
8. [Medios de transmisión por segmento](#8-medios-de-transmisión-por-segmento)
9. [Cableado troncal vs. cableado horizontal](#9-cableado-troncal-vs-cableado-horizontal)
10. [Distancias estimadas y cálculo de bobinas](#10-distancias-estimadas-y-cálculo-de-bobinas)
11. [Equipo activo: justificación y dimensionamiento](#11-equipo-activo-justificación-y-dimensionamiento)
12. [Estándares T568A/T568B: straight-through y crossover](#12-estándares-t568at568b)
13. [Disposición de pines documentada](#13-disposición-de-pines-documentada)
14. [Canalización: tipo, ruta y justificación](#14-canalización)
15. [Rack o gabinete del MDF](#15-rack-o-gabinete-del-mdf)
16. [Respaldo de energía (UPS)](#16-respaldo-de-energía-ups)
17. [Etiquetado de cables](#17-etiquetado-de-cables)
18. [Comparación con el estándar TIA/EIA-606](#18-comparación-con-el-estándar-tiaeia-606)
19. [Flujo de conexión end-to-end](#19-flujo-de-conexión-end-to-end)
20. [Presupuesto estimado](#20-presupuesto-estimado)
21. [Consideraciones de escalabilidad futura](#21-consideraciones-de-escalabilidad-futura)
22. [Compra directa vs. proveedor externo](#22-compra-directa-vs-proveedor-externo)
23. [Referencias](#23-referencias)

---

## 1. Introducción y alcance

<!-- COMPLETAR: 2-3 párrafos.
     Qué se diseña: la infraestructura de Capa 1 (física) del edificio de QuetzalDev S.A.
     Qué NO incluye: direccionamiento IP, VLANs, configuración de equipo, simulación.
     Mencioná que el edificio es de un solo nivel, por lo que se usa un único MDF sin IDFs. -->

---

## 2. Datos base del edificio

**Dimensiones generales (fijo):** 28 m × 21 m, un solo nivel.

| Zona | Ubicación en el plano | Dimensiones | Fondo |
|---|---|---|---|
| Departamento de Recepción | Franja superior, extremo izquierdo | 8 m × 9 m | 9 m |
| Departamento de Recursos Humanos | Franja superior | 6 m × 9 m | 9 m |
| Departamento Legal | Franja superior | 6 m × 9 m | 9 m |
| Sala de Capacitación | Franja superior, extremo derecho | 8 m × 9 m | 9 m |
| Baño | Dentro de Sala de Capacitación | 2 m × 2 m | — |
| Vestíbulo de Ingreso | Franja central, extremo izquierdo | 6 m × 7 m | 7 m |
| Departamento de Diseño e Innovación | Franja central | 6 m × 7 m | 7 m |
| Dirección General | Franja central | 6 m × 7 m | 7 m |
| Departamento de Backend | Franja central | 6 m × 7 m | 7 m |
| Data Center | Franja central, extremo derecho | 4 m × 7 m | 7 m |
| Área Abierta / Zona de Circulación General | Franja inferior, todo el ancho | 28 m × 5 m | 5 m |

**Observación de diseño (fijo):** el Área Abierta inferior recorre los 28 m del edificio y todas las
puertas de la franja central desembocan en ella. Es la ruta natural para la canalización principal.

> El plano trae las medidas rotuladas, así que **no hace falta deducir la escala** — todas las
> distancias se calculan directamente sobre las cotas indicadas.

---

## 3. Distribución de hosts por departamento

**Totales del enunciado (fijo):** 30 PCs de escritorio + 12 laptops = 42 equipos de usuario, más 6 servidores.

| Departamento | Equipos usuario (fijo) | PCs escritorio | Laptops | Servidores (fijo) | Puntos de red |
|---|---:|---:|---:|---:|---:|
| Recepción | 3 | `[ ]` | `[ ]` | 1 | 4 |
| Recursos Humanos | 8 | `[ ]` | `[ ]` | 0 | 8 |
| Legal | 4 | `[ ]` | `[ ]` | 0 | 4 |
| Sala de Capacitación | 10 | `[ ]` | `[ ]` | 0 | 10 |
| Diseño e Innovación | 7 | `[ ]` | `[ ]` | 1 | 8 |
| Dirección General | 4 | `[ ]` | `[ ]` | 0 | 4 |
| Backend | 6 | `[ ]` | `[ ]` | 1 | 7 |
| Data Center | 0 | 0 | 0 | 3 | 3 |
| **TOTAL** | **42** | **30** | **12** | **6** | **48** |

<!-- COMPLETAR: un párrafo justificando el reparto PC/laptop.
     Criterio sugerido: laptops donde hay movilidad real (Dirección, Diseño, Capacitación),
     PCs fijas donde el trabajo es de escritorio permanente (RRHH, Legal, Backend).
     IMPORTANTE: el enunciado exige que la distribución sea única — no puede coincidir con otro
     estudiante. Aunque una laptop pueda usar Wi-Fi, en este diseño de Capa 1 todo host recibe
     su punto de red cableado. -->

---

## 4. Inventario de equipos

### 4.1 Equipo activo

| Ítem | Modelo propuesto | Cantidad | Ubicación | Función |
|---|---|---:|---|---|
| Switch principal | `[ ]` | 1 | MDF | Núcleo de la estrella extendida; concentra los 8 troncales |
| Switch de departamento | `[ ]` | 8 | Un gabinete por área | Concentra el cableado horizontal de su departamento |
| UPS | `[ ]` | `[ ]` | MDF | Respaldo eléctrico del equipo activo |

### 4.2 Equipo pasivo

| Ítem | Modelo propuesto | Cantidad | Ubicación | Función |
|---|---|---:|---|---|
| Patch panel MDF | `[ ]` | `[ ]` | Rack MDF | Terminación fija de los troncales |
| Patch panel de departamento | `[ ]` | `[ ]` | Gabinete de área | Terminación del horizontal del área |
| ODF (si se usa fibra) | `[ ]` | `[ ]` | MDF | Terminación y distribución de fibras |
| Rack / gabinete MDF | `[ ]` | 1 | MDF | Aloja el equipo del cuarto principal |
| Gabinete de pared de departamento | `[ ]` | 8 | Cada área | Aloja switch + patch panel del área |
| Tomas de red (faceplates + jacks) | `[ ]` | `[ ]` | Áreas de trabajo | Interfaz del área de trabajo |
| Organizadores de cable | `[ ]` | `[ ]` | Racks | Orden y radio de curvatura |
| Escalerilla / canaleta | `[ ]` | `[ ]` m | Rutas | Canalización |

---

## 5. Ubicación y justificación del MDF

**Ubicación seleccionada:** <!-- COMPLETAR: coordenada/zona sobre el plano -->

<!-- COMPLETAR: justificación con 2-3 criterios. Candidatos:
     - Centralidad: minimiza la distancia promedio a los 48 puntos de red.
     - Acceso directo a la canalización principal del Área Abierta.
     - Verificación de que el punto más lejano queda muy por debajo de los 90 m del enlace permanente.
     - Acceso restringido, ventilación y alimentación eléctrica disponibles.
     - Distancia a fuentes de interferencia electromagnética.
     Al ser un edificio de un solo nivel, un único MDF es suficiente y no se requieren IDFs. -->

**Verificación del límite de 90 m:**

| Punto más lejano al MDF | Distancia estimada | ¿Cumple < 90 m? |
|---|---:|---|
| `[ ]` | `[ ]` m | `[ ]` |

---

## 6. Topología física por departamento

**Topología global del edificio:** estrella extendida (árbol) de dos niveles — switch principal en el
MDF → 8 switches de departamento → hosts. El enunciado la impone al indicar un único switch principal
que distribuye hacia los switches de cada departamento.

<!-- COMPLETAR la tabla. La rúbrica exige justificar los TRES factores por departamento:
     número de hosts, criticidad del segmento, y balance costo/escalabilidad/tolerancia a fallos.
     No repitas la misma frase ocho veces. -->

| Departamento | Topología | N.º hosts | Criticidad | Justificación (hosts + criticidad + costo/escalabilidad/tolerancia) |
|---|---|---:|---|---|
| Recepción | `[ ]` | 4 | `[ ]` | `[ ]` |
| Recursos Humanos | `[ ]` | 8 | `[ ]` | `[ ]` |
| Legal | `[ ]` | 4 | `[ ]` | `[ ]` |
| Sala de Capacitación | `[ ]` | 10 | `[ ]` | `[ ]` |
| Diseño e Innovación | `[ ]` | 8 | `[ ]` | `[ ]` |
| Dirección General | `[ ]` | 4 | `[ ]` | `[ ]` |
| Backend | `[ ]` | 7 | `[ ]` | `[ ]` |
| Data Center | `[ ]` | 3 | `[ ]` | `[ ]` |

**Topologías evaluadas y descartadas:**

| Topología | Por qué se descartó |
|---|---|
| Bus | `[ ]` |
| Anillo | `[ ]` |
| Malla completa | `[ ]` |

---

## 7. Puntos de red y tipos de toma

**Total de puntos de red: 48** (42 equipos de usuario + 6 servidores).

| Departamento | N.º de tomas | Tipo (unitaria/doble/triple/N) | Puertos totales | Dispositivos conectados | Puertos de reserva |
|---|---:|---|---:|---|---:|
| Recepción | `[ ]` | `[ ]` | `[ ]` | 3 equipos + 1 servidor | `[ ]` |
| Recursos Humanos | `[ ]` | `[ ]` | `[ ]` | 8 equipos | `[ ]` |
| Legal | `[ ]` | `[ ]` | `[ ]` | 4 equipos | `[ ]` |
| Sala de Capacitación | `[ ]` | `[ ]` | `[ ]` | 10 equipos | `[ ]` |
| Diseño e Innovación | `[ ]` | `[ ]` | `[ ]` | 7 equipos + 1 servidor | `[ ]` |
| Dirección General | `[ ]` | `[ ]` | `[ ]` | 4 equipos | `[ ]` |
| Backend | `[ ]` | `[ ]` | `[ ]` | 6 equipos + 1 servidor | `[ ]` |
| Data Center | `[ ]` | `[ ]` | `[ ]` | 3 servidores | `[ ]` |
| **TOTAL** | | | `[ ]` | **48 dispositivos** | `[ ]` |

<!-- COMPLETAR: justificá el criterio. Sugerencia defendible:
     - Toma doble como estándar de puesto de trabajo (un puerto en uso + uno de reserva).
     - Toma triple/N en las mesas de la Sala de Capacitación y en el rack del Data Center.
     - Toma unitaria en dispositivos aislados.
     Recordá: cada puerto de toma = un cable horizontal = un puerto de patch panel. -->

---

## 8. Medios de transmisión por segmento

| Segmento | Medio | Categoría / tipo | Distancia estimada | Ancho de banda requerido | Justificación |
|---|---|---|---:|---|---|
| Horizontal: switch de depto → hosts | `[ ]` | `[ ]` | `[ ]` m | `[ ]` | `[ ]` |
| Troncal: MDF → Recepción | `[ ]` | `[ ]` | `[ ]` m | `[ ]` | `[ ]` |
| Troncal: MDF → Recursos Humanos | `[ ]` | `[ ]` | `[ ]` m | `[ ]` | `[ ]` |
| Troncal: MDF → Legal | `[ ]` | `[ ]` | `[ ]` m | `[ ]` | `[ ]` |
| Troncal: MDF → Sala de Capacitación | `[ ]` | `[ ]` | `[ ]` m | `[ ]` | `[ ]` |
| Troncal: MDF → Diseño e Innovación | `[ ]` | `[ ]` | `[ ]` m | `[ ]` | `[ ]` |
| Troncal: MDF → Dirección General | `[ ]` | `[ ]` | `[ ]` m | `[ ]` | `[ ]` |
| Troncal: MDF → Backend | `[ ]` | `[ ]` | `[ ]` m | `[ ]` | `[ ]` |
| Troncal: MDF → Data Center | `[ ]` | `[ ]` | `[ ]` m | `[ ]` | `[ ]` |

**Tabla de referencia de categorías (para respaldar tu elección):**

| Categoría | Ancho de banda | Velocidad | Distancia máx. | Uso típico |
|---|---|---|---|---|
| Cat 5e | 100 MHz | 1 Gbps | 100 m | Mínimo aceptable, en retirada |
| Cat 6 | 250 MHz | 1 Gbps (10 Gbps hasta ~55 m) | 100 m | Horizontal de oficina |
| Cat 6A | 500 MHz | 10 Gbps | 100 m | Troncales de cobre, backbone corto |
| Fibra MM OM3/OM4 | — | 10 Gbps | 300-550 m | Backbone de edificio/campus |
| Fibra SM OS2 | — | 10-100 Gbps | Kilómetros | Enlaces entre edificios |

**Regla ANSI/TIA-568 aplicada:** el enlace permanente horizontal no debe superar **90 m** de cable
sólido, más hasta 10 m de patch cords en ambos extremos = **100 m de canal máximo**.

<!-- COMPLETAR: si elegís fibra en algún troncal, justificalo por escalabilidad y aislamiento
     electromagnético, NO por distancia — en un edificio de 28 m ningún enlace se acerca al límite
     del cobre. Y si usás fibra, agregá el ODF al inventario y al flujo end-to-end. -->

---

## 9. Cableado troncal vs. cableado horizontal

| Aspecto | Troncal (backbone) | Horizontal |
|---|---|---|
| Recorrido | MDF ↔ switch de departamento | Switch de departamento ↔ host |
| Cantidad en este diseño | 8 enlaces | 48 enlaces |
| Medio | `[ ]` | `[ ]` |
| Tráfico que transporta | Agregado de todo el departamento | De un solo host |
| Formato de etiqueta | `MDF-[Departamento]` | `[Departamento]-PR##` |
| Representación en el diagrama | `[ color / grosor ]` | `[ color / grosor ]` |

<!-- COMPLETAR: definí ambos términos con tus palabras y listá explícitamente los 8 enlaces
     troncales. Este apartado vale 15 pts y debe quedar coherente con el diagrama y con la
     tabla de etiquetado (§17). -->

**Enlaces troncales del diseño:**

| # | Etiqueta | Origen | Destino | Medio | Distancia |
|---:|---|---|---|---|---:|
| 1 | `MDF-Recepcion` | Switch principal (MDF) | Switch Recepción | `[ ]` | `[ ]` m |
| 2 | `MDF-RecursosHumanos` | Switch principal (MDF) | Switch RRHH | `[ ]` | `[ ]` m |
| 3 | `MDF-Legal` | Switch principal (MDF) | Switch Legal | `[ ]` | `[ ]` m |
| 4 | `MDF-Capacitacion` | Switch principal (MDF) | Switch Sala de Capacitación | `[ ]` | `[ ]` m |
| 5 | `MDF-Diseno` | Switch principal (MDF) | Switch Diseño e Innovación | `[ ]` | `[ ]` m |
| 6 | `MDF-DireccionGeneral` | Switch principal (MDF) | Switch Dirección General | `[ ]` | `[ ]` m |
| 7 | `MDF-Backend` | Switch principal (MDF) | Switch Backend | `[ ]` | `[ ]` m |
| 8 | `MDF-DataCenter` | Switch principal (MDF) | Switch Data Center | `[ ]` | `[ ]` m |

---

## 10. Distancias estimadas y cálculo de bobinas

### 10.1 Método de estimación

1. Las distancias se miden **sobre las cotas del plano** (28 m × 21 m, con cada ambiente rotulado).
2. La ruta se traza **por donde va la canalización**, en ángulos rectos — nunca en diagonal.
3. Se suma la **subida/bajada** vertical del punto de red a la escalerilla: `[ ]` m por extremo.
4. Se aplica una **holgura de servicio (slack)** de `[ ]` % por terminación, curvas y reservas.

### 10.2 Cableado horizontal

| Etiqueta | Departamento | Distancia ruta (m) | Subida/bajada (m) | Subtotal (m) |
|---|---|---:|---:|---:|
| `Recepcion-PR01` | Recepción | `[ ]` | `[ ]` | `[ ]` |
| <!-- COMPLETAR: una fila por cada uno de los 48 puntos --> | | | | |
| **Subtotal horizontal** | | | | `[ ]` |

### 10.3 Cableado troncal

| Etiqueta | Distancia ruta (m) | Subida/bajada (m) | Subtotal (m) |
|---|---:|---:|---:|
| `MDF-Recepcion` | `[ ]` | `[ ]` | `[ ]` |
| <!-- COMPLETAR: las 8 troncales --> | | | |
| **Subtotal troncal** | | | `[ ]` |

### 10.4 Cálculo de bobinas

```
metros_totales = (subtotal_horizontal + subtotal_troncal) × (1 + slack)
               = ( [ ] + [ ] ) × (1 + [ ] )
               = [ ] m

bobinas = ⌈ metros_totales / 305 ⌉ = ⌈ [ ] / 305 ⌉ = [ ] bobinas
```

**Bobina estándar de UTP: 305 m (1000 ft).** Siempre se redondea hacia arriba.

<!-- COMPLETAR: comentá el excedente de la última bobina como reserva para crecimiento futuro.
     Este número alimenta la decisión de §22 (compra directa vs. proveedor). -->

---

## 11. Equipo activo: justificación y dimensionamiento

### 11.1 Función de cada elemento en el flujo de conexión

| Elemento | Función que cumple |
|---|---|
| Switch principal (MDF) | `[ ]` |
| Switch de departamento | `[ ]` |
| Patch panel | `[ ]` |
| ODF (si aplica) | `[ ]` |
| Rack / gabinete | `[ ]` |
| UPS | `[ ]` |
| Tomas de red | `[ ]` |

### 11.2 Dimensionamiento de switches de departamento

Regla aplicada: **puertos ≥ hosts del área + 1 uplink + reserva de crecimiento.**

| Departamento | Hosts | + Uplink | Mínimo | Switch elegido | Puertos libres |
|---|---:|---:|---:|---|---:|
| Recepción | 4 | 1 | 5 | `[ ]` | `[ ]` |
| Recursos Humanos | 8 | 1 | 9 | `[ ]` | `[ ]` |
| Legal | 4 | 1 | 5 | `[ ]` | `[ ]` |
| Sala de Capacitación | 10 | 1 | 11 | `[ ]` | `[ ]` |
| Diseño e Innovación | 8 | 1 | 9 | `[ ]` | `[ ]` |
| Dirección General | 4 | 1 | 5 | `[ ]` | `[ ]` |
| Backend | 7 | 1 | 8 | `[ ]` | `[ ]` |
| Data Center | 3 | 1 | 4 | `[ ]` | `[ ]` |

> Los switches se consiguen comercialmente en 8, 16, 24 y 48 puertos. Ojo con RRHH, Capacitación,
> Diseño y Backend: al sumar el uplink se pasan del escalón de 8 puertos.

### 11.3 Dimensionamiento del patch panel y switch del MDF

Regla del enunciado: *el patch panel del edificio se dimensiona según la cantidad total de puntos de
red, y el switch seleccionado debe tener puertos ≥ el patch panel correspondiente.*

| Elemento | Puertos requeridos | Elegido | Justificación |
|---|---:|---|---|
| Patch panel MDF | `[ ]` | `[ ]` | `[ ]` |
| Switch principal MDF | `[ ]` | `[ ]` | `[ ]` |

<!-- ⚠️ COMPLETAR CON CRITERIO — CONSULTAR AL TUTOR ANTES DE DIAGRAMAR.
     El enunciado dice "patch panel del edificio dimensionado según la cantidad TOTAL de puntos de
     red" (serían 48), pero al mismo tiempo define el troncal como MDF ↔ switch de departamento,
     con lo cual al MDF solo llegan 8 enlaces. Las dos frases no son compatibles.
     Lectura A (literal): patch panel de 48 puertos + switch de 48 puertos en el MDF.
     Lectura B (jerárquica): patch panel de 12-24 puertos en el MDF para los 8 troncales, más un
                             patch panel por departamento dimensionado a sus puntos.
     Escribí acá la lectura que confirme el tutor y dejá constancia de la consulta. -->

---

## 12. Estándares T568A/T568B

### 12.1 Regla aplicada

- **Straight-through (directo):** mismo estándar en ambos extremos. Conecta dispositivos de **distinto
  tipo** (host ↔ switch, servidor ↔ switch). El cruce TX/RX lo resuelve el switch internamente.
- **Crossover (cruzado):** T568A en un extremo y T568B en el otro. Conecta dispositivos del **mismo
  tipo** (switch ↔ switch), porque ambos extremos transmiten por los mismos pines.

**Estándar seleccionado para el cableado horizontal:** `[ T568A / T568B ]`

El cableado horizontal se poncha con el **mismo estándar en ambos extremos**: en la toma de red del
área de trabajo y en el patch panel correspondiente.

### 12.2 Tabla de enlaces

| Grupo de enlaces | Cantidad | Extremo A | Extremo B | Tipo de cable | Justificación técnica |
|---|---:|---|---|---|---|
| Switch de depto ↔ hosts | 48 | `[ ]` | `[ ]` | Straight-through | `[ ]` |
| Switch MDF ↔ switch de depto | 8 | Switch | Switch | Crossover | `[ ]` |

<!-- COMPLETAR: en la justificación explicá QUÉ dispositivo hay en cada extremo, que es lo que
     pide la rúbrica. Sumá una observación sobre Auto-MDIX: los switches modernos detectan y cruzan
     automáticamente, por lo que en la práctica casi todo se cablea straight-through; aun así este
     diseño aplica la regla clásica. Esa observación suma en "comprensión teórico-práctica". -->

---

## 13. Disposición de pines documentada

### 13.1 Orden de colores de ambos estándares

Vista del conector RJ45 con los contactos hacia arriba y la pestaña hacia abajo; el pin 1 queda a la izquierda.

| Pin | T568A | T568B | Función (10/100BASE-T) |
|---:|---|---|---|
| 1 | Blanco/Verde | Blanco/Naranja | TX+ |
| 2 | Verde | Naranja | TX− |
| 3 | Blanco/Naranja | Blanco/Verde | RX+ |
| 4 | Azul | Azul | No usado |
| 5 | Blanco/Azul | Blanco/Azul | No usado |
| 6 | Naranja | Verde | RX− |
| 7 | Blanco/Café | Blanco/Café | No usado |
| 8 | Café | Café | No usado |

La única diferencia entre ambos: los pares **verde y naranja están intercambiados** (pines 1-2 ↔ 3-6).

### 13.2 Cable straight-through — ejemplo del diseño

**Enlace:** `[ etiqueta real de tu diseño, ej. Legal-PR03 ]`
**Extremos:** `[ ]` ↔ `[ ]`

| Pin | Extremo A (`[ ]`) | Extremo B (`[ ]`) |
|---:|---|---|
| 1 | `[ ]` | `[ ]` |
| 2 | `[ ]` | `[ ]` |
| 3 | `[ ]` | `[ ]` |
| 4 | `[ ]` | `[ ]` |
| 5 | `[ ]` | `[ ]` |
| 6 | `[ ]` | `[ ]` |
| 7 | `[ ]` | `[ ]` |
| 8 | `[ ]` | `[ ]` |

### 13.3 Cable crossover — ejemplo del diseño

**Enlace:** `[ etiqueta real, ej. MDF-Backend ]`
**Extremos:** Switch principal ↔ Switch de departamento

| Pin | Extremo A (`[ ]`) | Extremo B (`[ ]`) |
|---:|---|---|
| 1 | `[ ]` | `[ ]` |
| 2 | `[ ]` | `[ ]` |
| 3 | `[ ]` | `[ ]` |
| 4 | `[ ]` | `[ ]` |
| 5 | `[ ]` | `[ ]` |
| 6 | `[ ]` | `[ ]` |
| 7 | `[ ]` | `[ ]` |
| 8 | `[ ]` | `[ ]` |

<!-- Vale 5 pts. Si además del cuadro hacés un diagrama propio del conector, mejor. -->

---

## 14. Canalización

**Tipo seleccionado para rutas principales:** `[ ]`
**Tipo seleccionado para bajadas a tomas:** `[ ]`

| Tipo | Descripción | Ventajas | Desventajas |
|---|---|---|---|
| Escalerilla metálica abierta | Bandeja tipo escalera suspendida | Barata, ventilada, fácil ampliar, inspección visual | Polvo, sin protección mecánica, estética |
| Escalerilla / ducto cerrado | Bandeja con tapa | Protección mecánica y de polvo | Más cara, menos ventilación |
| Canaleta plástica | Canal PVC sobre pared | Estética, barata | Capacidad limitada |
| Tubería conduit | Tubo EMT/PVC | Máxima protección | Capacidad fija, difícil ampliar |

**Ruta propuesta:** <!-- COMPLETAR: describí el recorrido. El Área Abierta de 28 m × 5 m es la
espina dorsal natural, ya que todas las puertas de la franja central desembocan ahí. -->

**Justificación:** <!-- COMPLETAR: volumen de cables, facilidad de crecimiento, costo, y respeto
del radio mínimo de curvatura del UTP. -->

---

## 15. Rack o gabinete del MDF

**Elección:** `[ rack de piso / gabinete de pared ]` de `[ ]` U

### Cálculo de unidades de rack

| Elemento | Cantidad | U c/u | U total |
|---|---:|---:|---:|
| Switch principal | 1 | `[ ]` | `[ ]` |
| Patch panel(s) | `[ ]` | `[ ]` | `[ ]` |
| ODF (si aplica) | `[ ]` | `[ ]` | `[ ]` |
| Organizadores de cable | `[ ]` | 1 | `[ ]` |
| UPS rackeable | `[ ]` | `[ ]` | `[ ]` |
| Bandeja | `[ ]` | `[ ]` | `[ ]` |
| **Subtotal ocupado** | | | `[ ]` |
| **Reserva de crecimiento (30-40 %)** | | | `[ ]` |
| **Total requerido** | | | `[ ]` |

> 1 U = 1.75 pulgadas (44.45 mm).

**Justificación:** <!-- COMPLETAR según TU inventario. -->

---

## 16. Respaldo de energía (UPS)

**Alcance (fijo por el enunciado):** se respalda el equipo activo del edificio — switch central y
switches de departamento.

### 16.1 Estimación de consumo

| Equipo | Cantidad | W unitario | W total | Fuente del dato |
|---|---:|---:|---:|---|
| Switch principal | 1 | `[ ]` | `[ ]` | `[ datasheet ]` |
| Switch de departamento | 8 | `[ ]` | `[ ]` | `[ datasheet ]` |
| **TOTAL** | | | `[ ]` W | |

**Consumos de referencia:** switch 8-16 puertos sin PoE ≈ 10-20 W · switch 24 puertos ≈ 20-40 W ·
switch 48 puertos ≈ 40-70 W.

### 16.2 Cálculo de capacidad

```
1. Potencia_total  = [ ] W
2. VA_requeridos   = Potencia_total / 0.9  = [ ] VA
3. VA_con_margen   = VA_requeridos × 1.25  = [ ] VA     (nunca cargar un UPS al 100 %)
4. UPS comercial   = [ ] VA                             (750 / 1000 / 1500 / 2000 / 3000)
```

**Modelo propuesto:** `[ ]` · **Autonomía estimada:** `[ ]` minutos

<!-- COMPLETAR: podés mencionar que en un diseño real el Data Center tendría su propio UPS
     dimensionado aparte, ya que los 6 servidores no entran en este cálculo. -->

---

## 17. Etiquetado de cables

**Formato obligatorio del enunciado:**
- Cableado horizontal: `[Área/Departamento]-PR[##]` → ej. `Recepcion-PR01`, `Legal-PR03`
- Cableado troncal: `MDF-[Área/Departamento]` → ej. `MDF-Recepcion`, `MDF-Backend`

### 17.1 Cableado troncal

| Etiqueta | Origen | Destino | Medio |
|---|---|---|---|
| `MDF-Recepcion` | Switch principal | Switch Recepción | `[ ]` |
| `MDF-RecursosHumanos` | Switch principal | Switch RRHH | `[ ]` |
| `MDF-Legal` | Switch principal | Switch Legal | `[ ]` |
| `MDF-Capacitacion` | Switch principal | Switch Sala de Capacitación | `[ ]` |
| `MDF-Diseno` | Switch principal | Switch Diseño e Innovación | `[ ]` |
| `MDF-DireccionGeneral` | Switch principal | Switch Dirección General | `[ ]` |
| `MDF-Backend` | Switch principal | Switch Backend | `[ ]` |
| `MDF-DataCenter` | Switch principal | Switch Data Center | `[ ]` |

### 17.2 Cableado horizontal

| Etiqueta | Departamento | Puerto switch | Toma | Dispositivo |
|---|---|---|---|---|
| `Recepcion-PR01` | Recepción | `[ ]` | `[ ]` | `[ ]` |
| <!-- COMPLETAR: las 48 filas --> | | | | |

---

## 18. Comparación con el estándar TIA/EIA-606

El estándar **ANSI/TIA/EIA-606** (actualmente TIA-606-C) norma la **administración** de la
infraestructura de telecomunicaciones: cómo se identifica, etiqueta y documenta cada elemento.

| Aspecto | Esquema usado en esta práctica | Lo que exige TIA/EIA-606 |
|---|---|---|
| Alcance de los identificadores | `[ ]` | `[ ]` |
| Codificación por colores | `[ ]` | `[ ]` |
| Registros y documentación | `[ ]` | `[ ]` |
| Unicidad del identificador | `[ ]` | `[ ]` |
| Clases de administración | `[ ]` | `[ ]` |

<!-- COMPLETAR: se exigen al menos DOS diferencias concretas y UNA razón de por qué en un entorno
     real se opta por el estándar completo. Diferencias candidatas:
     (a) El formato Depto-PR## no codifica la ubicación física (edificio-cuarto-rack-panel-puerto);
         el 606 usa identificadores jerárquicos del tipo 1A-B01-24.
     (b) El 606 exige codificación por colores normalizada por función y registros de administración
         actualizables ante cada cambio; el esquema simplificado no define ninguno de los dos.
     (c) La etiqueta Legal-PR01 no es única a nivel campus: se duplicaría en otro edificio.
     Razón real candidata: en un data center con cientos de cables, la trazabilidad ante fallas y la
     gestión de movimientos/adiciones/cambios (MACs) se vuelve inmanejable sin identificadores
     jerárquicos únicos y sin registros, y el tiempo de diagnóstico crece de forma desproporcionada.
     Investigá y escribilo con tus palabras — es parte de la nota de comprensión. -->

---

## 19. Flujo de conexión end-to-end

**Dispositivo elegido:** `[ ]` en `[ departamento ]`

```
[ Dispositivo: PC / laptop / servidor ]  — NIC RJ45
  ↓ patch cord Cat [ ] ( [ straight-through ] )
[ Toma de red [ tipo ] — etiqueta [ Depto-PR## ] ]
  ↓ cable horizontal Cat [ ] , ponchado T568[ ] en ambos extremos
  ↓ por [ canaleta de bajada ] → [ escalerilla en el Área Abierta ]
[ Patch panel del departamento — puerto [ ] ]
  ↓ patch cord
[ Switch de departamento — puerto [ ] ]
  ↓ uplink
[ Cable troncal — etiqueta MDF-[Depto] , [ medio ] , [ crossover ] ]
  ↓ por [ ruta de canalización ]
[ Patch panel / ODF del MDF — puerto [ ] ]
  ↓ patch cord
[ Switch principal — puerto [ ] ]
  ↓
[ Destino: servidor en Data Center / salida a proveedor ]
```

<!-- COMPLETAR: usá etiquetas REALES de tu diseño, no genéricas. Este apartado amarra todo el
     manual y demuestra que el diseño es coherente de punta a punta. -->

---

## 20. Presupuesto estimado

| # | Ítem | Descripción / modelo | Cantidad | Precio unitario (Q) | Subtotal (Q) |
|---:|---|---|---:|---:|---:|
| 1 | Bobina UTP Cat `[ ]` (305 m) | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 2 | Bobina UTP Cat 6A / fibra troncal | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 3 | Jacks RJ45 | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 4 | Faceplates | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 5 | Patch panel MDF | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 6 | Patch panels de departamento | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 7 | Patch cords (2 por punto) | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 8 | Conectores RJ45 | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 9 | Switch principal | `[ ]` | 1 | `[ ]` | `[ ]` |
| 10 | Switches de departamento | `[ ]` | 8 | `[ ]` | `[ ]` |
| 11 | Rack / gabinete MDF | `[ ]` | 1 | `[ ]` | `[ ]` |
| 12 | Gabinetes de pared de departamento | `[ ]` | 8 | `[ ]` | `[ ]` |
| 13 | Organizadores de cable | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 14 | Escalerilla + accesorios | `[ ]` | `[ ]` m | `[ ]` | `[ ]` |
| 15 | Canaleta | `[ ]` | `[ ]` m | `[ ]` | `[ ]` |
| 16 | UPS | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 17 | ODF + fibra + transceivers SFP (si aplica) | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 18 | Etiquetas / identificación | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 19 | Mano de obra / instalación | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 20 | Imprevistos (5-10 %) | — | — | — | `[ ]` |
| | | | | **TOTAL** | **Q `[ ]`** |

**Fuentes de precios consultadas:** <!-- COMPLETAR: catálogos Siemon/Panduit del enunciado,
tiendas locales (Intelaf, MAX, etc.). Citá la fuente de cada rubro. -->

---

## 21. Consideraciones de escalabilidad futura

<!-- Apartado RECOMENDADO por el enunciado — no es obligatorio pero suma. Ideas:
     - Puertos libres en patch panels y switches, y cuántos hosts nuevos admite el diseño.
     - Tomas dobles con un puerto de reserva desde el día uno.
     - Capacidad sobrante de la canalización y del rack (U libres).
     - Migración del troncal de cobre a fibra sin reobrar la canalización.
     - Evolución del segmento de Data Center hacia una arquitectura Spine & Leaf si crece el
       tráfico este-oeste: latencia predecible de dos saltos, ECMP en lugar de Spanning Tree,
       gateway distribuido cerca de la carga, y VXLAN/EVPN para superar el límite de 4094 VLANs.
       (Se menciona como proyección, NO como el diseño entregado en esta práctica.) -->

---

## 22. Compra directa vs. proveedor externo

<!-- Apartado RECOMENDADO. Contrastá:
     - Compra directa: menor costo de materiales, control sobre marcas, pero requiere mano de obra
       propia, herramienta (ponchadora, tester certificador) y asume el riesgo de la instalación.
     - Proveedor / integrador: mayor costo, pero incluye certificación del cableado, garantía
       extendida del fabricante (Siemon/Panduit dan garantías de 20-25 años sobre instalaciones
       certificadas), y documentación as-built.
     Cerrá con TU recomendación para QuetzalDev y el porqué, apoyándote en el número de bobinas
     y el total del presupuesto. -->

---

## 23. Referencias

<!-- COMPLETAR en formato consistente. Base sugerida: -->

1. ANSI/TIA-568 — *Commercial Building Telecommunications Cabling Standard*.
2. ANSI/TIA-606-C — *Administration Standard for Telecommunications Infrastructure*.
3. Odom, Wendell. 2019. *CCNA 200-301 Official Cert Guide*, Vol. 1. Indianápolis: Cisco Press. ISBN-10 0138229635.
4. Cisco Networking Academy. 2024. *Cursos de redes y certificaciones*. https://www.netacad.com/
5. Siemon. *Catálogo de productos 2022*. https://www.dartel-interactivo.cl/assets/catalogos_pdf/Catalogo-Siemon-2022.pdf
6. Panduit. *Infraestructura de redes — Catálogo 2025*. https://www.panduit.com/content/dam/panduit/es/website/support/documents/infraestructura-de-redes-corp-catalogo-cpcb295-sa-rolatam-01-2025.pdf
7. Notas de clase, Semanas 2 y 3 — UEDI, Redes de Computadoras 1.
8. <!-- COMPLETAR: fuentes de precios y datasheets de los modelos elegidos -->
