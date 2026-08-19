# Informe de Desarrollo — Práctica 1: QuetzalDev S.A.

**Universidad de San Carlos de Guatemala** · Facultad de Ingeniería\
**Curso:** Redes de Computadoras 1 — Segundo Semestre 2026\
**Estudiante:** Santiago Barrera\
**Carné:** 201905884\
**Plano asignado:** Plano 3 (carnés con terminación 4-5)\
**Fecha:** 21 de agosto de 2026\

---

## 1. Introducción

En esta práctica asumí el papel de ingeniero de telecomunicaciones contratado por QuetzalDev S.A., una
empresa de desarrollo de software que acaba de inaugurar un edificio corporativo de un solo nivel. El
encargo fue puntual: diseñar la infraestructura física de red **antes** de que la empresa comprara un
solo equipo, para que la compra saliera de un plan y no al revés.

Todo el trabajo se queda en la **Capa 1 del modelo OSI**. No hay direccionamiento IP, no hay VLANs, no
hay configuración de switches ni simulación en Packet Tracer. Lo que entrego es el plano de cómo va a
quedar cableado el edificio: por dónde corren los cables, de qué categoría son, cuántos metros hacen
falta, qué equipo los termina y cómo se identifica cada uno. Suena menos vistoso que configurar
enrutamiento, pero es la parte que después no se puede cambiar sin romper pared.

Este informe no repite el Manual Técnico. El manual dice **qué** diseñé; acá cuento **cómo llegué** a
eso: en qué orden fui decidiendo, qué descarté, y en qué me trabé.

---

## 2. Interpretación del plano base

Lo primero que hice fue leer el plano sin dibujar nada encima, y me alegró encontrar que **ya traía todas
las cotas rotuladas**. Eso me ahorró el paso de deducir la escala midiendo con regla y multiplicando por
un factor, que es donde normalmente se cuela el error que después arrastra todo el cálculo de metraje.
Todas las distancias del manual salen de esas cotas, nunca de medir el dibujo.

El edificio son 28 m × 21 m, o sea 588 m², organizados en tres franjas horizontales de fondo constante:

- **Franja superior** (9 m de fondo): Recepción de 8 × 9, RRHH de 6 × 9, Legal de 6 × 9 y Sala de
  Capacitación de 8 × 9, esta última con un baño de 2 × 2 en la esquina.
- **Franja central** (7 m de fondo): Vestíbulo de Ingreso, Diseño e Innovación, Dirección General y
  Backend, todos de 6 × 7, más el Data Center de 4 × 7 en el extremo este.
- **Área Abierta** (5 m de fondo): los 28 m completos de ancho, en la parte de abajo.

Antes de seguir, **verifiqué que las cotas cerraran**, porque si no cerraban significaba que había algún
ducto o área técnica sin rotular que tendría que considerar. Sumé: la franja superior da
8 + 6 + 6 + 8 = 28 m, la central da 6 + 6 + 6 + 6 + 4 = 28 m, y los fondos dan 9 + 7 + 5 = 21 m. Cerró
exacto, sin holguras ni traslapes, así que pude descartar la existencia de áreas ocultas.

De la lectura salieron dos hechos que me condicionaron todo el trazado y que en su momento no vi como
problemas sino como datos:

**El Área Abierta es la espina dorsal del edificio.** Recorre los 28 m de ancho y recibe las puertas de
los cinco ambientes de la franja central. Es la única zona que toca a todos los ambientes de una franja
completa, así que la canalización principal iba a ir ahí, sin discusión.

**La franja superior no colinda con ningún corredor.** Los cuatro ambientes de arriba están separados del
Área Abierta por toda la franja central. Sus puertas se abren sobre las paredes divisorias laterales,
encadenando Recepción → RRHH → Legal → Capacitación. Esto sí me costó: significaba que no podía derivar
el cableado de esos cuatro departamentos desde el troncal del corredor, y que necesitaban una ruta propia.
Lo resolví más adelante, pero lo detecté acá.

Y un tercer detalle que anoté aunque no era de cableado: **el acceso al edificio es por el Vestíbulo**, en
el extremo oeste. Eso vuelve al oeste la zona de mayor tránsito de visitantes, dato que después usé como
criterio de seguridad física para descartar ubicaciones del cuarto de telecomunicaciones.

---

## 3. Proceso de diseño

Trabajé en este orden, y el orden importó más de lo que esperaba:

1. **Conté y repartí los hosts** entre los ocho departamentos.
2. **Ubiqué el MDF**, evaluando alternativas.
3. **Marqué los puntos de red** y decidí el tipo de toma de cada uno.
4. **Definí la topología** y separé troncal de horizontal.
5. **Medí distancias y calculé materiales.**
6. **Dimensioné el equipo activo, el rack y el UPS.**
7. **Cerré con etiquetado, presupuesto y documentación.**

La razón de ese orden es que cada paso depende del anterior. No podía medir distancias sin saber dónde
estaban las tomas y el MDF, y no podía dimensionar el UPS sin haber elegido los switches. Cuando intenté
adelantarme en algo, me tocó volver.

### Dos veces que me tocó devolverme

**El patch panel del edificio.** El enunciado dice que "el patch panel del edificio se dimensiona según
la cantidad total de puntos de red" y que el switch debe tener puertos iguales o mayores al "patch panel
correspondiente". Empecé asumiendo un panel único de 48 puertos en el MDF, y avancé bastante con esa
idea. Después caí en que eso implicaba que **los 48 cables horizontales llegaran hasta el Data Center**,
lo que hacía irrelevantes los switches departamentales que el propio enunciado exige, y disparaba el
metraje. Me devolví, releí la palabra "correspondiente" y adopté la lectura de que la capacidad de
terminación se distribuye: cada departamento aloja el panel de su horizontal —48 puertos poblados en
total, igual al total de puntos del edificio— y el MDF termina solo los 8 troncales. Dejé documentadas
ambas lecturas en §11.3 del manual, y verifiqué que la regla `switch ≥ panel` se cumple bajo las dos, para
no depender de cómo la interprete quien califique.

Esa fue la decisión más cara en términos de tiempo, porque de haberla resuelto mal después de medir
distancias, habría tenido que recalcular las bobinas desde cero.

**Los puertos de reserva.** Al principio quise dejar un puerto libre cableado en cada toma doble, pensando
que era buena práctica. Cuando llegué al conteo me di cuenta de que eso rompía la relación básica del
cableado estructurado —un puerto de toma equivale a un cable horizontal y a un puerto de patch panel— y
que el total dejaba de ser 48, que es la cifra sobre la que el enunciado pide dimensionar el panel.
Retrocedí y moví toda la reserva a capas que no consumen cable: posiciones libres en los marcos de panel,
puertos libres en los switches y alojamientos ciegos en los faceplates. Terminé con margen para 44 puntos
nuevos sin comprar equipo activo, que es más reserva de la que habría conseguido con el plan original.

---

## 4. Criterios de selección

### 4.1 Distribución de equipos de usuario

El enunciado fija cuántos equipos tiene cada departamento, pero deja a mi criterio cómo se reparten las
30 PC de escritorio y las 12 laptops, y advierte que la distribución no puede ser idéntica entre
estudiantes.

El criterio que apliqué fue la **movilidad real del puesto de trabajo**: laptop para quien se mueve como
parte de su función, PC de escritorio para el puesto estacionario o de alta demanda de cómputo.

Con eso, las 12 laptops quedaron así: 3 en Dirección General, porque los directivos salen a reuniones y
solo el puesto de asistencia es fijo; 3 en Diseño e Innovación, para los perfiles de UI/UX que presentan
propuestas fuera de su escritorio, dejando 4 workstations fijas para Data Analytics y el Laboratorio de
QA; 4 en la Sala de Capacitación, entre el instructor y las dinámicas grupales, complementando 6
estaciones fijas de práctica; y una en RRHH y otra en Legal, para la jefatura que hace entrevistas y para
las diligencias en juzgados.

Las 30 PC quedaron en los puestos estacionarios: el mostrador de Recepción, los escritorios
administrativos de RRHH y Legal, las mesas de práctica de Capacitación, las workstations de analítica y QA
y **todo Backend**, donde el desarrollo se hace sobre equipos fijos de alto rendimiento.

Algo que quiero dejar explícito porque me lo pregunté al inicio: aunque una laptop podría trabajar por
Wi-Fi, esta práctica diseña la Capa 1 **cableada**, así que todo host —PC, laptop o servidor— recibe su
punto de red. El reparto entre escritorio y portátil no cambia el total de 48 puntos.

### 4.2 Ubicación del cuarto de telecomunicaciones

Acá tomé la decisión que más discutí conmigo mismo, porque el criterio del enunciado y el criterio
normativo apuntaban a lugares distintos.

El enunciado pide ubicar el MDF minimizando la distancia hacia los puntos de red. Lo primero que hice fue
precisar el alcance de ese criterio, y encontré algo que cambió el peso de la decisión: como el diseño es
una **estrella extendida de dos niveles**, los 48 enlaces horizontales miden lo mismo sin importar dónde
esté el MDF, porque van de cada host al switch de su propia área. La ubicación del MDF **solo afecta a los
8 enlaces troncales**. O sea, el ahorro posible se mide sobre 8 cables, no sobre 56.

Evalué tres opciones. El **Vestíbulo de Ingreso** lo descarté rápido: es el punto de acceso al edificio y
la zona de más tránsito de personal externo, lo que incumple de frente el criterio de seguridad física de
ANSI/TIA-569.

La segunda fue un **cuarto nuevo de 3 × 3 m recortado del Área Abierta**, en la posición geométricamente
más céntrica. Medí las ocho rutas troncales en ángulo recto para las dos opciones y la céntrica ganaba:
105 m contra 121 m de cable troncal, un promedio de 13.1 m contra 15.1 m. Pero **el ahorro son 16 m en
todo el edificio, el 5 % de una bobina de 305 m**, y a cambio había que construir un ambiente nuevo con
su propia climatización, control de acceso y circuito eléctrico dedicado; mantener dos espacios técnicos
en lugar de uno; y meter el montante vertical atravesando la Dirección General, con obra dentro de una
oficina ejecutiva.

Me quedé con el **Data Center**, con el rack contra el muro oeste en (24.5, 6.0). Es el único ambiente
concebido como espacio técnico de acceso restringido, ya tiene climatización y circuito dedicado porque
aloja tres servidores, está en el extremo opuesto al Vestíbulo, y su puerta desemboca en el Área Abierta
donde corre la canalización. Un beneficio que no había previsto es que el montante hacia la franja
superior sube **dentro del propio ambiente técnico** y entra directo a la Sala de Capacitación, sin pasar
por ninguna oficina ocupada.

**Verificación del límite de 90 m.** Antes de cerrar la decisión comprobé el peor caso de cada tipo de
cableado, sumando los tramos verticales de subida y bajada y una holgura del 10 %. El troncal más largo,
`MDF-Recepcion`, da 34.1 m, y el horizontal más largo del edificio 17.3 m. Contra los 90 m de enlace
permanente que permite ANSI/TIA-568, el enlace más largo usa el **38 % del límite**. Eso me confirmó dos
cosas: que podía decidir la ubicación del MDF por seguridad y operación sin comprometer el desempeño, y
que un segundo cuarto de telecomunicaciones sería innecesario en un edificio de este tamaño.

### 4.3 Topologías físicas

A nivel de edificio la topología es una **estrella extendida**, o árbol, de dos niveles: el switch
principal del MDF alimenta a ocho switches departamentales, y cada uno atiende a los hosts de su área.
No la elegí en el sentido estricto: el enunciado la impone al dar un switch por departamento y un único
switch principal, y el cableado estructurado la impone por norma, porque ANSI/TIA-568 define el sistema
como una jerarquía en estrella.

Lo que sí decidí fue **la topología de cada área y qué factor domina la justificación en cada caso**.
Los ocho departamentos quedaron en estrella, pero por razones distintas, y eso es lo que traté de que no
se leyera como una tabla mecánica.

Para poder comparar los ocho entre sí primero definí una escala de criticidad, porque me di cuenta de que
sin ella estaba diciendo "crítico" con significados diferentes en cada párrafo. La criticidad no la medí
por tamaño sino por impacto de la indisponibilidad: crítica el Data Center, alta Backend y Dirección
General, media-alta Diseño e Innovación, media Recepción, RRHH y Legal, y baja la Sala de Capacitación.

Con eso, el factor dominante quedó así. En la **Sala de Capacitación** manda el costo, y es donde el
argumento se cuantifica mejor: diez nodos en malla completa serían 45 enlaces contra 10 de la estrella.
En **Backend** manda el aislamiento de fallos: un cable dañado deja sin servicio a un desarrollador, no a
los siete. En **Legal** manda la confidencialidad, porque el switch entrega la trama solo al puerto
destino en lugar de difundirla por un medio compartido. En **Diseño e Innovación** manda el ancho de banda
dedicado por puesto. En **Dirección General** manda la tolerancia a fallos, aunque tenga pocos hosts, por
la relación criticidad/densidad más desfavorable del edificio. Y en el **Data Center** la estrella se
implementa dentro del propio rack, lo que elimina toda una clase de fallos: sin trayecto de cable por
canalización, no hay daño mecánico ni humedad ni intervención accidental.

**Lo que descarté.** El **bus** quedó fuera porque todos los nodos comparten un medio, el ancho de banda
se reparte, un corte tumba el segmento completo, y además es incompatible con el equipo activo que el
enunciado exige y con el cableado estructurado en sí; es una topología en desuso desde 10BASE-2. El
**anillo** lo descarté por comportamiento, no por costo, y ese matiz me pareció importante: con cinco
nodos, estrella y anillo cuestan lo mismo —cinco enlaces cada uno—, pero ante un corte en estrella cae un
nodo y en anillo cae el segmento. Además agregar un host obliga a abrir el lazo e interrumpir el área, y
requiere hardware tipo Token Ring o FDDI que ya no está en el mercado. La **malla completa** la descarté
con aritmética: los enlaces crecen como n(n−1)/2, o sea **1 128 enlaces si se aplicara a los 48 puntos**
del edificio, cada host con n−1 interfaces de red. Y la **malla parcial** no la descarté por deficiencia
técnica —es lo normal entre nodos de backbone— sino porque con un único switch principal no hay pares de
nodos entre los que tender enlaces alternativos.

También dejé escrito, en lugar de esconderlo, que **toda estrella concentra el riesgo en su nodo central**.
El switch de un departamento tumba su área; el del MDF interrumpe la comunicación entre departamentos,
aunque el tráfico interno de cada área siga conmutando localmente. La mitigación más barata que encontré
fue un efecto secundario de otra decisión: al estandarizar los ocho switches de acceso en un solo modelo,
**una sola unidad de repuesto cubre los ocho departamentos**.

### 4.4 Equipo activo

Dimensioné los switches con la regla `puertos ≥ hosts del área + 1 uplink + reserva`. Como los escalones
comerciales son 8, 16, 24 y 48 puertos, RRHH, Capacitación, Diseño y Backend necesitaban 16 por fuerza al
sumar el uplink. Para los otros cuatro —Recepción, Legal, Dirección y Data Center— un switch de 8 puertos
habría bastado, pero **adopté el de 16 en los ocho departamentos** por tres razones: cumple la regla del
enunciado sin ambigüedad incluso comparando contra la capacidad total del marco de panel y no solo contra
los puertos poblados; deja un único modelo en planta, lo que reduce el inventario de repuestos a una
referencia; y da 72 puertos libres, margen para casi duplicar la población de hosts. El sobrecosto son
cuatro equipos y lo reflejé en el presupuesto.

Para el MDF elegí **24 puertos** y no 16, aunque el mínimo eran 9 —los 8 troncales más el enlace del
proveedor—, porque es el equipo que concentra todo el tráfico entre departamentos y quería reserva para
segmentos futuros, puntos de acceso Wi-Fi o un segundo enlace de salida.

En cuanto a marca, me fui por la línea **Cisco Business**: el CBS250-16T-2G para acceso y el CBS350-24T-4G
para el núcleo. Además de tener un solo proveedor para soporte y garantía, ambos traen puertos SFP, y eso
es lo que hace que la migración a fibra del backbone sea después un cambio de transceptores y no un cambio
de plataforma.

El **patch panel** fue el punto que ya conté en la sección 3: nueve marcos modulares de 12 posiciones, ocho
en las áreas para el horizontal y uno en el MDF para los troncales. Los marcos parcialmente poblados no
son un truco para cuadrar números; los paneles tipo keystone se venden así justamente para poblarlos según
necesidad.

Del resto del equipo activo, lo que más me sorprendió fue el **UPS**, y lo cuento en la sección 6 porque
fue uno de los retos.

---

## 5. Justificación del medio de transmisión del cableado troncal

El enunciado pide evaluar tres ejes —velocidad de uplink requerida, distancia y costo/escalabilidad— y
quiero empezar por el que **no** decidió nada, porque creo que es el punto más honesto del análisis.

**La distancia no discrimina en este edificio.** El troncal más largo, `MDF-Recepcion`, mide 31 m
incluyendo tramos verticales. El límite de canal del cobre es 100 m desde Cat 5e, y la fibra multimodo
alcanza de 300 a 550 m. Las dos opciones sobran por márgenes enormes: Cat 6A usa el 31 % de su alcance y
la fibra multimodo apenas el 10 %. Invocar la distancia para justificar un medio superior habría sido
incorrecto, y prefiero decirlo en lugar de usar el argumento porque suena bien.

**Velocidad de uplink.** Cada troncal agrega el tráfico de un departamento completo: 4 puntos en Recepción,
8 en RRHH y Diseño, 10 en Capacitación, 7 en Backend. Los switches que instalo son gigabit, así que los
troncales operan hoy a 1 Gbps y con eso alcanza de sobra para la demanda actual. Pero acá apliqué un
principio que ordenó toda la sección de medios: **la planta pasiva sobrevive a la activa**. Un switch dura
de cinco a siete años; un cableado bien instalado y certificado, de quince a veinticinco. Cambiar un switch
es una intervención de horas; recablear un edificio es una obra. Entonces el cable se dimensiona para el
horizonte largo y la electrónica se compra para la necesidad presente.

**La decisión: Cat 6A U/FTP en los ocho troncales y Cat 6 U/UTP en el horizontal.**

El Cat 6A entrega 10 Gbps hasta los 100 m, de modo que el día que el ancho de banda agregado lo pida, la
migración consiste en cambiar switches **sin abrir una sola pared**. El apantallado U/FTP lo elegí porque
el troncal es el enlace que corre por bandeja compartida a lo largo del edificio, y aunque la ruta no
colinda con tableros ni cuartos de máquinas, el margen extra en un enlace que representa a un departamento
entero me pareció justificado. En el horizontal me quedé en Cat 6 U/UTP: cubre 1 Gbps por puesto con
margen, admite 10GBASE-T hasta unos 55 m —muy por encima del enlace más largo, que mide 14.7 m— y el
sobrecosto frente a Cat 5e es marginal, además de que Cat 5e ya está en retirada comercial.

Adopté **la misma categoría en los ocho troncales** aunque midan entre 2 y 31 m. Diferenciarla por
departamento habría dado un ahorro despreciable —el troncal completo son 135 m— a cambio de multiplicar
referencias de compra, repuestos y herramienta de certificación.

**Por qué descarté la fibra.** La evalué en serio, y la conclusión fue que la razón habitual para elegirla
no aplica acá. La distancia no aporta ningún argumento, como ya expliqué. El ancho de banda tampoco: Cat 6A
da 10 Gbps y la ventaja de la fibra solo se materializaría por encima de eso. La inmunidad
electromagnética sería válida si la canalización compartiera trayecto con acometidas de fuerza o
maquinaria, pero es un edificio de oficinas y el apantallado del Cat 6A cubre el riesgo residual. Y en
contra estaba el costo real: había que sumar ODF, transceptores SFP+ en los dieciséis extremos, y una
segunda disciplina de terminación —fusión o conectorización— con herramienta y personal distintos de los
del cobre.

La fibra encarecía y complicaba la instalación sin resolver ninguna limitación real. Así que la documenté
como **ruta de migración** en lugar de descartarla del todo: la canalización queda dimensionada para
alojarla, con menos del 5 % de llenado en el tramo más cargado, de modo que un salto futuro a 40 o 100 Gbps
no exigiría rehacer la ruta, solo tender el nuevo medio sobre ella.

Una consecuencia práctica de usar dos categorías: los cálculos de bobinas se separan por material, porque
son dos referencias comerciales distintas. Salen 2 bobinas de Cat 6 para los 438 m del horizontal y 1 de
Cat 6A para los 148 m del troncal, y eso convierte las **tres bobinas** de una recomendación por
contingencia en una obligación de la solución adoptada.

---

## 6. Retos de planificación física encontrados

Estos fueron los seis puntos donde de verdad me trabé.

**Medir por canalización y no en línea recta.** Mi primer impulso fue medir distancias con el teorema de
Pitágoras entre coordenadas, y estaba mal: el cable no puede ir en diagonal atravesando oficinas. Tuve que
rehacer las mediciones **en ángulos rectos siguiendo la ruta real**, sumando los quiebres. Un enlace que en
línea recta mide 15 m puede requerir 22 m de cable. Si no lo hubiera corregido, habría subestimado la
compra.

**Llegar a la franja superior.** Este fue el problema estructural del plano. Los cuatro ambientes de arriba
no colindan con el Área Abierta, así que no podía derivarlos del troncal principal. Lo resolví con una ruta
de tres tramos en forma de C: la bandeja principal sobre el Área Abierta en Y = 4.5, un montante en
X = 24.5 que cruza el Data Center hacia la Sala de Capacitación, y un ramal que recorre la franja superior
en Y = 12.5 de este a oeste. Que el montante subiera dentro del propio Data Center fue una ventaja de la
ubicación del MDF que descubrí después de haberla elegido por otras razones.

**Los tramos verticales, que casi se me olvidan.** Estuve un buen rato calculando metraje solo en planta,
hasta que me di cuenta de que el cable no viaja a ras de piso: sube 0.80 m del gabinete a la canalización a
2.80 m y baja 2.40 m hasta la toma, que está a 0.40 m del piso. Son **3.2 m por enlace horizontal** y 2.0 m
por troncal. Sobre 45 enlaces con acometida de pared eso da 144 m, más 14 m de los troncales: cerca del
**30 % de todo el cable del proyecto**. Omitirlos habría subestimado la compra en más de media bobina.

**Definir el tipo de toma cuando un escritorio agrupa varios equipos.** El enunciado dice que la toma se
define según la cantidad de dispositivos que se conectan en ese punto, pero no dice qué es "un punto".
Adopté la regla de que una toma sirve a los dispositivos de un mismo puesto o mueble contiguo, y que se
instala toma independiente cuando el dispositivo está separado o requiere acceso restringido, como los
servidores. Con eso los 48 puntos se agrupan en **22 tomas**: 6 unitarias, 7 dobles, 8 triples y una
cuádruple. Un detalle de comercialización que tuve que resolver: los faceplates se venden en 1, 2, 4 y 6
posiciones, no en 3, así que las tomas triples van sobre placas de cuatro con una tapa ciega. Y el Data
Center fue un caso aparte, porque en un rack no hay toma de pared: ahí la función la cumple un panel
keystone de tres puertos montado en el propio gabinete.

**La ambigüedad del patch panel.** Ya la conté en la sección 3. Lo que aprendí es que cuando el enunciado
admite dos lecturas, conviene resolver la que menos daño hace si me equivoco y **documentar las dos**. Por
eso verifiqué la regla `switch ≥ panel` contra los puertos poblados y contra la capacidad total del marco:
el diseño la cumple en los dos escenarios, así que la ambigüedad dejó de ser un riesgo.

**El UPS, que resultó ser el apartado más interesante.** Calculé el consumo agregado de los nueve switches
—174 W— y de ahí salieron 242 VA con margen, que redondeando al escalón comercial dan un UPS de 750 VA.
Iba a dejarlo así hasta que caí en algo obvio que el cálculo agregado esconde: **esos 174 W no están en un
solo lugar**. Están repartidos en ocho ambientes distintos. Un UPS en el MDF no puede alimentar el switch
de Recepción, que está a 29 m, sin tender un circuito eléctrico regulado hasta cada gabinete: ocho
corridas de fuerza en paralelo a la canalización de datos, con la interferencia que eso implica y un costo
de obra que supera varias veces el del propio respaldo.

Terminé distribuyendo el respaldo igual que se distribuyó la conmutación: un UPS rackeable de 1 000 VA en
el MDF y siete compactos de 600 VA en los gabinetes de área. Y me tocó explicar por qué la capacidad
instalada —5 200 VA— es tan superior a los 242 VA calculados: **la capacidad no la fija la carga, la fija
el mínimo comercial**, porque no existen UPS de 70 VA. Con cargas del 5 al 7 %, el efecto secundario es
que la autonomía se estira a horas en lugar de minutos, lo cual en un edificio donde los cortes duran unos
minutos significa que la red completa sobrevive sin que nadie se dé cuenta.

**Un reto extra: que el diagrama se entendiera.** Cuando terminé la vista física del plano y me puse a
revisarla, no lograba ver la estrella en mi propio dibujo. Tardé en entender por qué: los cuatro troncales
que van a la franja superior comparten el montante y el ramal, así que al dibujarlos **se superponen y se
ven como una sola línea con cuatro derivaciones**, que es exactamente la pinta de un bus. Compartir la ruta
física no es compartir el medio, pero el dibujo no lo mostraba. Lo resolví separando los trazos paralelos
dentro de la bandeja y agregando una vista topológica de apoyo, con los enlaces en línea recta, donde la
estrella extendida aparece de inmediato. Fue un recordatorio de que un diagrama correcto puede seguir
siendo ilegible.

---

## 7. Conclusiones

**Diseñar la Capa 1 es comprometerse a largo plazo.** La diferencia de vidas útiles entre el cable y la
electrónica —de quince a veinticinco años contra cinco a siete— es lo que ordenó casi todas mis
decisiones de medio físico. El presupuesto lo terminó de confirmar: el 27 % del proyecto se va en equipo
activo que se va a renovar cuatro veces, contra el 17 % en cable que va a durar todo el período. Sobre esa
asimetría se justifica sobredimensionar la planta pasiva y comprar la electrónica para hoy.

**El criterio de centralidad del MDF pesa menos de lo que parece en una estrella extendida.** Fue el
hallazgo que más me hizo pensar. Como los 48 horizontales miden lo mismo sin importar dónde esté el cuarto,
la centralidad solo afecta a 8 cables, y en este edificio el ahorro de la posición más céntrica eran 16 m
—el 5 % de una bobina— a cambio de construir y climatizar un ambiente nuevo. Los criterios de seguridad
física y de concentración de espacios técnicos ganaron con facilidad.

**El diseño quedó con margen real de crecimiento, y lo puedo cuantificar.** Absorbe 44 puntos de red
nuevos sin comprar un switch ni un patch panel, porque el factor limitante son las posiciones de panel —44
libres— y no los puertos de switch, de los que hay 72. Cada punto adicional costaría del orden de Q 600
contra los Q 2 765 que costó cada punto de la instalación inicial, porque el switch, el panel, el gabinete
y la canalización ya están pagados.

**Con más presupuesto haría dos cosas concretas, y en este orden.** Primero, el segundo enlace de subida
del Data Center: dos metros de cable y un puerto de cada lado protegen el segmento más crítico del
edificio, y es la mejor relación costo-beneficio que identifiqué. Después, el switch principal redundante,
que ya tiene 8 U libres en el gabinete y un puerto reservado esperándolo. La fibra en el backbone, en
cambio, **no la haría** ni con más presupuesto: en 31 m no resuelve ninguna limitación real, y ya está
preparada la ruta para cuando sí haga falta.

**Lo que más me costó aplicar del estándar fue el 606, y no por difícil sino por incómodo.** Investigarlo
me dejó viendo lo pobre que es un esquema de etiquetado como `Legal-PR03`: no dice dónde está el cable, no
identifica canalizaciones ni gabinetes ni tierras, no define colores por función y no sobreviviría a una
segunda sede porque la etiqueta se duplicaría. En 56 cables se puede vivir con eso. Entender que el
problema no crece con el tamaño de la instalación sino **con el tiempo** —con cada movimiento, adición y
cambio que va desactualizando la documentación— fue probablemente lo más útil que saqué de esta práctica.

---

## 8. Referencias

**Normas técnicas**

1. ANSI/TIA-568 — *Commercial Building Telecommunications Cabling Standard*.
2. ANSI/TIA-569 — *Telecommunications Pathways and Spaces*.
3. ANSI/TIA-606-C — *Administration Standard for Telecommunications Infrastructure*.
4. IEEE 802.3ab — *1000BASE-T*.

**Bibliografía del curso**

5. Odom, Wendell. 2019. *CCNA 200-301 Official Cert Guide*, Vol. 1. Indianápolis: Cisco Press.
   ISBN-10 0138229635.
6. Cisco Networking Academy. 2024. *Cursos de redes y certificaciones*. https://www.netacad.com/
7. Notas de clase, Semanas 2 y 3 — UEDI, Redes de Computadoras 1.

**Catálogos y hojas de datos**

8. Panduit. *Infraestructura de redes — Catálogo 2025*.
9. Siemon. *Catálogo de productos 2022*.
10. Cisco Systems. *Cisco Business 250 y 350 Series — Data Sheets*.
11. Schneider Electric / APC. *Smart-UPS y Back-UPS — Especificaciones técnicas*.

**Documento propio**

12. Barrera, Santiago. 2026. *Manual Técnico — Práctica 1: QuetzalDev S.A.* Documento entregado junto a
    este informe, donde constan los cálculos, tablas y justificaciones que acá se narran.
