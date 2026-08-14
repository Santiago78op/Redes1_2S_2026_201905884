# Informe de Desarrollo — Práctica 1: QuetzalDev S.A.

**Universidad de San Carlos de Guatemala** · Facultad de Ingeniería
**Curso:** Redes de Computadoras 1 — Segundo Semestre 2026
**Estudiante:** Santiago Barrera
**Carné:** 201905884
**Plano asignado:** Plano 3 (carnés con terminación 4-5)
**Fecha:** <!-- COMPLETAR -->

---

> **NOTA DE TRABAJO — BORRAR ANTES DE ENTREGAR**
> Este informe **no repite el Manual Técnico**. El manual dice *qué* se diseñó; este informe cuenta
> *cómo se llegó* a ese diseño: los criterios, las alternativas descartadas y los problemas reales
> que aparecieron al interpretar el plano.
> El enunciado pide explícitamente cuatro cosas: el proceso de diseño, los criterios de selección
> (topologías, medios de transmisión, equipo activo), los retos de planificación física al
> interpretar el plano base, y la justificación del medio usado en el cableado troncal.
> Escribilo en primera persona. 1-3 páginas honestas valen más que 10 genéricas.

---

## 1. Introducción

<!-- COMPLETAR: 1-2 párrafos.
     El rol asumido (ingeniero de telecomunicaciones contratado por QuetzalDev S.A.), el encargo
     (diseñar la infraestructura de Capa 1 de un edificio de un nivel antes de comprar equipo), y
     el alcance del trabajo: diseño físico, sin configuración ni simulación. -->

---

## 2. Interpretación del plano base

<!-- COMPLETAR: contá cómo leíste el plano antes de dibujar nada.
     Datos que podés usar: el edificio es de 28 m × 21 m en un solo nivel, organizado en tres
     franjas — cuatro ambientes de 9 m de fondo arriba (Recepción 8×9, RRHH 6×9, Legal 6×9,
     Sala de Capacitación 8×9 con un baño de 2×2), cinco ambientes de 7 m de fondo al centro
     (Vestíbulo 6×7, Diseño e Innovación 6×7, Dirección General 6×7, Backend 6×7, Data Center 4×7),
     y el Área Abierta / Zona de Circulación General de 28 m × 5 m abajo.
     Puntos que vale la pena narrar:
     - Que el plano ya trae las cotas rotuladas, así que no hubo que deducir la escala.
     - Que todas las puertas de la franja central desembocan en el Área Abierta, lo que la
       convierte en la espina dorsal natural de la canalización.
     - Cómo afecta al tendido que la franja central se interponga entre el corredor y los
       ambientes de la franja superior. -->

---

## 3. Proceso de diseño

<!-- COMPLETAR: narrá el orden en que fuiste tomando las decisiones y por qué ese orden.
     Una secuencia razonable para contar:
     1. Conteo y distribución de hosts por departamento.
     2. Ubicación del MDF.
     3. Marcado de puntos de red y tipos de toma.
     4. Definición de la topología y del esquema troncal/horizontal.
     5. Medición de distancias y cálculo de materiales.
     6. Dimensionamiento de equipo activo, rack y UPS.
     Si cambiaste de opinión en el camino, contalo — es lo que hace que el informe se lea como
     trabajo real y no como un resumen del manual. -->

---

## 4. Criterios de selección

### 4.1 Distribución de equipos de usuario

<!-- COMPLETAR: los totales por departamento son fijos (42 equipos y 6 servidores), pero el reparto
     entre 30 PCs de escritorio y 12 laptops lo definiste vos. Explicá con qué criterio.
     Recordá que el enunciado exige que esta distribución sea única entre estudiantes. -->

### 4.2 Ubicación del cuarto de telecomunicaciones

<!-- COMPLETAR: qué ubicaciones evaluaste y por qué elegiste la final.
     Vale mucho mostrar la alternativa descartada: por ejemplo, ubicar el MDF dentro del Data Center
     es cómodo por seguridad física y por tener los servidores al lado, pero el Data Center está
     en el extremo derecho del edificio (4 m × 7 m, franja central), lo que aumenta la distancia
     promedio hacia los departamentos del extremo opuesto.
     Contá cómo verificaste el límite de 90 m del enlace permanente. -->

### 4.3 Topologías físicas

<!-- COMPLETAR: por qué la estrella extendida a nivel edificio y qué topología elegiste por área.
     Explicá cómo pesaste los tres factores que pide la rúbrica: número de hosts, criticidad del
     segmento y balance costo/escalabilidad/tolerancia a fallos.
     Mencioná explícitamente qué topologías descartaste (bus, anillo, malla completa) y por qué. -->

### 4.4 Equipo activo

<!-- COMPLETAR: cómo dimensionaste los switches (hosts + uplink + reserva), por qué esos escalones
     comerciales de puertos, y cómo dimensionaste el patch panel y el switch del MDF.
     Si consultaste al tutor sobre el criterio del patch panel del edificio, dejá constancia acá. -->

---

## 5. Justificación del medio de transmisión del cableado troncal

<!-- COMPLETAR: el enunciado pide este apartado de forma explícita, así que dedicale espacio propio.
     Los tres ejes que pide evaluar son:
     - Velocidad de uplink requerida por los switches de departamento.
     - Distancia real hacia cada departamento, medida sobre tu plano.
     - Costo y escalabilidad de la solución elegida.
     Argumento honesto que conviene explicitar: en un edificio de 28 m ningún troncal se acerca al
     límite de 100 m del cobre, así que la distancia NO es el factor decisivo. Si elegís fibra en
     algún enlace, el argumento válido es escalabilidad futura, ancho de banda agregado y
     aislamiento electromagnético — no distancia. Si elegís cobre en todos, justificalo por costo,
     simplicidad de terminación y suficiencia técnica. Ambas posturas son defendibles si el
     razonamiento está escrito. -->

---

## 6. Retos de planificación física encontrados

<!-- COMPLETAR: acá es donde se nota si de verdad hiciste el trabajo. Retos reales de esta práctica:
     - Estimar rutas de cable en ángulos rectos por canalización en vez de distancias en línea recta.
     - Decidir cómo llegar a los ambientes de la franja superior, que no colindan con el corredor.
     - Definir el tipo de toma cuando un mismo escritorio agrupa varios dispositivos.
     - Sumar las subidas y bajadas verticales y la holgura de servicio al metraje.
     - Resolver la ambigüedad del enunciado sobre el dimensionamiento del patch panel del edificio.
     - Elegir entre centralidad geométrica del MDF y conveniencia operativa de pegarlo al Data Center.
     Contá qué hiciste ante cada uno, incluso si la solución fue asumir un criterio y documentarlo. -->

---

## 7. Conclusiones

<!-- COMPLETAR: 3-5 conclusiones concretas sobre el diseño y sobre lo aprendido.
     Evitá generalidades tipo "aprendí mucho sobre redes". Apuntá a cosas específicas:
     qué implica que el diseño quede en Capa 1, qué margen de crecimiento dejaste, qué harías
     distinto con más presupuesto, o qué parte del estándar te resultó más difícil de aplicar. -->

---

## 8. Referencias

<!-- COMPLETAR: mismas fuentes que el Manual Técnico más lo que hayas consultado aparte. -->

1. ANSI/TIA-568 — *Commercial Building Telecommunications Cabling Standard*.
2. ANSI/TIA-606-C — *Administration Standard for Telecommunications Infrastructure*.
3. Odom, Wendell. 2019. *CCNA 200-301 Official Cert Guide*, Vol. 1. Indianápolis: Cisco Press.
4. Cisco Networking Academy. 2024. *Cursos de redes y certificaciones*. https://www.netacad.com/
5. Notas de clase, Semanas 2 y 3 — UEDI, Redes de Computadoras 1.
