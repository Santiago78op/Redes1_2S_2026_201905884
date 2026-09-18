# Guion de defensa — Proyecto 1 · SmartCity Tech Park

**Deck:** `presentacion/defensa-proyecto1.html` (o el `-standalone.html`, que abre con doble clic sin internet)
**Planchas:** 21 (17 de exposición + 1 separador + 3 anexos para preguntas)
**Duración objetivo:** ~16 minutos + preguntas
**Navegación:** `→` avanza · `M` abre el índice · `S` abre las notas del presentador · `F` pantalla completa

Los números de plancha salen del DOM del deck, no están contados a mano. Si agregás o quitás una
plancha, regenerá este guion antes de la defensa.

---

## Bloque 1 · El problema (planchas 1–4) — 2:50

### Plancha 1 · Portada — 0:30
> Buenos días. Voy a presentar el rediseño de la red del SmartCity Tech Park. Antes de empezar, una
> aclaración de alcance: **este proyecto es de Capa 1 y Capa 2**. No hay routing, no hay ACL, y eso
> va a importar cuando lleguemos a las pruebas, porque hay dos que **tienen que fallar**.

`→` a la 2.

### Plancha 2 · El encargo — 1:00
> El enunciado **no da una topología**. Da requisitos por área: el Centro de Datos tiene que ser el
> VTP Server y llevar una granja de al menos cuatro servidores con un enlace redundante de alto
> tráfico; I+D necesita tres switches donde *la caída de uno no aísle a los demás*; el Corporativo,
> dos alas que se hablen entre sí y visitantes aislados; y la Planta conserva el hub Legacy.
>
> La columna de la derecha es lo único que no decidí yo: **sale del carné**. VLANs 14 a 54, nativa
> 94, dominio `Smart_8`, LACP y PVST+ por ser carné par. Un ID mal puesto penaliza del 50 al 100 %,
> así que es lo primero que verifiqué contra el simulador.

`→` a la 3.

### Plancha 3 · La red plana — 1:00
> Este es el punto de partida. Todo el campus en **un solo dominio de broadcast**: la maquinaria
> industrial, los servidores, las estaciones de investigación y las laptops de los visitantes.
>
> La tabla lista los cuatro síntomas y, al lado, la causa real de cada uno. Lo importante es que
> **ninguno se resuelve tendiendo más cable**.

`→` (aparece la línea de abajo)

> Y se realimentan: el ruido del segmento Legacy no se queda en la Planta, cruza los enlaces
> saturados y llega a los servidores. Peor todavía, si sobre esta topología yo agrego un cable «por
> las dudas», lo que creo es un **bucle de Capa 2** sin nadie que lo controle.

`→` a la 4.

### Plancha 4 · Cita — 0:20
> *(leer la plancha y callarse 5 segundos)*
>
> Por eso el rediseño no podía ser incremental.

`→` a la 5.

---

## Bloque 2 · El diseño (planchas 5–9) — 6:30

### Plancha 5 · La topología aplicada — 1:30
> La estructura es una **jerarquía de tres niveles**. El Core conmuta entre edificios y concentra
> los cuatro trunks; la distribución agrega cada edificio y le presenta **un solo** enlace al Core;
> el acceso conecta los equipos finales. La señal de que la jerarquía se respetó es la columna de la
> derecha: **del Core no cuelga ni una sola PC**.
>
> *(señalar en el diagrama)* En el campus hay exactamente **tres zonas con camino alterno**: el
> canal al Centro de Datos, el canal a I+D, y el anillo de I+D junto con el triángulo del
> Corporativo. Las dos primeras son agregación; la tercera es Spanning Tree. No es lo mismo, y
> vuelvo a eso en un momento.

`→` (aparece la excepción)

> Una excepción que declaro de entrada: la Planta cuelga directo del Core, sin distribución. Tiene
> un solo switch y una sola VLAN; un nivel intermedio solo agregaría costo y un punto de falla. **La
> jerarquía se aplica donde aporta, no como formalidad.**

`→` a la 6.

### Plancha 6 · Las cuatro áreas — 0:45
> Así quedó cada área en Packet Tracer. No me detengo en ellas — están documentadas en el §12 del
> manual — pero sí quiero que se vea que hay **tres formas topológicas conviviendo**, y cada una por
> un motivo distinto.

`→` (aparece la línea)

> Estrella jerárquica en el campus. Anillo en I+D, porque el requisito es que la caída de un switch
> no aísle a los demás. Y triángulo en el Corporativo, porque las alas tienen que hablarse aunque
> caiga el distribuidor.

`→` a la 7.

### Plancha 7 · VLANs y dominios — 1:15
> Cinco VLANs de usuario, más dos que no tienen usuarios a propósito.
>
> La **94** es la nativa de todos los trunks y la dejo **vacía**: como la VLAN nativa viaja sin
> etiqueta, si no hay ningún puerto de acceso en ella, el ataque de VLAN hopping por doble
> etiquetado se queda sin vector. La **999** es donde confino los puertos apagados; esa no la pide
> el enunciado, la agrego como buena práctica.
>
> A la derecha está el resultado cuantificable: de **un** dominio de broadcast pasamos a **cinco**.
> Y 54 dominios de colisión, de los cuales **52 son punto a punto en full-duplex**, donde la
> colisión es estructuralmente imposible. Los dos compartidos son el hub y el aire del Access Point,
> y ambos están ahí por requisito, no por descuido.

`→` a la 8.

### Plancha 8 · VTP — 1:15
> El Core es el VTP Server porque es el único punto por donde pasan los cuatro trunks: un anuncio
> suyo llega a los tres edificios en un salto. Los otros nueve son Client.
>
> La excepción es **SW-COMUNES, en Transparent**. Ahí el aislamiento no es de tráfico, es **de
> administración**: ese switch ni siquiera conoce las VLANs 14, 24, 34 y 44.
>
> El recuadro de abajo es lo que más me interesa señalar: **el riesgo real de VTP no es el modo, es
> el número de revisión**. Manda el switch con la revisión más alta, aunque esté en Client. Por eso
> el procedimiento antes de conectar cualquier equipo es pasarlo por Transparent y devolverlo a
> Client, que deja la revisión en cero.

`→` (aparece la medición)

> Medido en los once switches: los nueve Client comparten **revisión 29** con el Server, y
> SW-COMUNES está en **cero**. Y la prueba de fondo de que VTP propagó no es este `show vtp status`,
> es que **SW-ALA-A tiene las siete VLANs sin que yo creara ninguna ahí**.

`→` a la 9.

### Plancha 9 · STP — 1:45  *(la plancha más importante)*
> Modo **PVST+**, un árbol por VLAN.
>
> La decisión que quiero defender es **dónde va la raíz**. La propuesta inicial era ponerla en el
> Core para casi todas las VLANs, y la descarté. El criterio que la sustituyó es: **la raíz va donde
> está la redundancia de esa VLAN**, no en el switch más importante del campus.
>
> El razonamiento es concreto: STP bloquea el puerto **más lejano a la raíz**. Si pongo la raíz en
> el distribuidor de cada edificio, lo que queda bloqueado es el **enlace de respaldo** —el que une
> las dos alas, o la cuerda del anillo— y no un uplink que se usa todos los días.

`→` (detalle fino)

> Y un detalle que no es casualidad: el cierre del anillo de I+D va a **100 Mbps a propósito**. Eso
> le da costo STP 19 frente a 4, así que es el candidato natural al bloqueo. El resultado es
> predecible en lugar de depender de qué MAC salió más baja.

`→` (la medición)

> Las cinco raíces y los tres puertos bloqueados que devolvió el simulador **coinciden exactamente**
> con lo documentado. El detalle completo está en el anexo, plancha 20.

`→` a la 10.

---

## Bloque 3 · Las dos redundancias y la Capa 1 (planchas 10–12) — 2:50

### Plancha 10 · Cita — 0:20
> *(leer y pausar)* Esta distinción es la que ordena todo el diseño.

`→` a la 11.

### Plancha 11 · EtherChannel — 1:15
> Dos canales, ambos LACP en `active/active`. **Po1** hacia la granja de servidores, en cobre.
> **Po2** hacia I+D, en fibra OM4: dos gigas agregados, el **trunk de mayor ancho de banda del
> campus**, que es un requisito explícito del enunciado.
>
> Por qué `active` y no `on`: el modo `on` fuerza el canal sin negociar nada. Si el cableado está
> mal, `on` produce directamente un **bucle**. LACP simplemente no levanta el canal y deja que STP
> bloquee lo sobrante. Es la diferencia entre fallar de forma segura y fallar de forma catastrófica.
>
> En la evidencia hay tres marcas que leer: **S** de Capa 2, **U** de *in use*, y **(P)** en cada
> miembro, que significa *bundled*. Si un miembro apareciera en `(I)`, ese cable estaría trabajando
> suelto y LACP no habría negociado.

`→` (aparece la línea)

> Y el dato que conecta con la plancha anterior: para STP, un Port-channel es **un solo enlace
> lógico**. Por eso no hay bucle que bloquear… y por eso perder un miembro no dispara reconvergencia.

`→` a la 12.

### Plancha 12 · Medios — 1:15
> Capa 1. Los cuatro criterios se aplican en orden de descarte: distancia, ancho de banda,
> interferencia, costo.
>
> Los dos primeros enlaces de fibra **se explican solos**: 180 y 120 metros están fuera del alcance
> normativo del cobre, no hay decisión que tomar. El de servidores es cobre porque son 10 metros
> dentro del mismo rack y poner fibra sería pagar transceptores sin ganancia.

`→` (aparece el recuadro)

> La fila que quiero defender es la tercera. **El enlace a la Planta mide 90 metros: cabe en cobre,
> y aun así va en fibra.** Los motores, los variadores de frecuencia y los equipos de soldadura de
> una planta industrial inducen ruido que degrada el UTP y provoca errores de trama. La fibra
> transporta luz: es inmune por construcción, y además aísla galvánicamente los dos edificios.
>
> Es la única fila donde el criterio ganador no es la distancia, y por eso es la que demuestra que
> los cuatro criterios se aplicaron de verdad y no como regla de pulgar.

`→` a la 13.

---

## Bloque 4 · Seguridad y evidencia (planchas 13–17) — 4:30

### Plancha 13 · Seguridad de Capa 2 — 1:15
> Siete medidas. Pero la columna que me interesa es **la tercera**: lo que cada una **no** resuelve.
>
> La nativa 94 no sirve de nada si dejo un puerto de acceso dentro de ella. El `port-security` se
> basa en una MAC, que es falsificable. El `storm-control` contiene la tormenta pero **no elimina la
> colisión** — eso solo se logra quitando el hub, y el enunciado me obliga a conservarlo. Y el banner
> no impide el acceso: es respaldo legal, advierte.

`→` (aparece la línea)

> Sobre visitantes: el aislamiento es **triple** —VLAN separada, VTP Transparent y trunk
> restringido— pero es **de Capa 2**. Impide que un visitante alcance las VLANs internas; dentro de
> la 54 sí se ven entre ellos, porque no hay Capa 3 ni ACL. Prefiero declararlo a presentarlo como
> aislamiento total.

`→` a la 14.

### Plancha 14 · Evidencia — 1:15
> Doce pruebas, doce aprobadas, veintinueve capturas. Y **un** resultado que obligó a corregir el
> documento, que es la siguiente plancha.
>
> De las doce, tres que hay que saber leer:
>
> **E10 y E11 fallan al 100 %, y ese es el éxito.** Un ping entre VLANs distintas sin router *debe*
> perder todos los paquetes. Un 0 % ahí sería un error de diseño, no un logro.
>
> **E13** es la firma de una reconvergencia de STP: 100 %, luego 50 %, luego 0 % de pérdida. Ese es
> el costo de PVST+, medido en unos 26 y 42 segundos.
>
> **E14** es el contraste: cae un miembro de Po1 y el canal **sigue arriba en ambos extremos**, sin
> reconvergencia. Si esa prueba tardara 30 segundos, significaría que el EtherChannel no se formó.

`→` (aparece la línea)

> Ahí están las dos redundancias del diseño, contrastadas con números del simulador.

`→` a la 15.

### Plancha 15 · El hallazgo — 0:50
> Esta es la única prueba donde el simulador me contradijo, y no fue un fallo de la red sino de mi
> estimación.
>
> Yo había documentado 30 a 50 segundos de convergencia al apagar SW-ID-2. **Medí interrupción
> nula.** La predicción suponía que el tráfico cruzaba el anillo, y no lo hace: SW-ID-1 y SW-ID-3
> tienen uplink propio, así que la caída de SW-ID-2 ni siquiera requiere que STP reconverja. La
> decisión de poner dos uplinks en vez de uno resultó **mejor** de lo que yo había escrito.

`→` (aparece la regla)

> Reescribí el §24.2 con la medición. La regla de trabajo del proyecto fue esa: cuando el simulador
> contradice al documento, manda el simulador.

`→` a la 16.

### Plancha 16 · Conclusiones — 0:50
> Cuatro cosas quedan demostradas: que el problema era de fronteras y no de cableado; que pasamos de
> uno a cinco dominios de broadcast; que cada tipo de redundancia está donde corresponde; y que la
> raíz de STP va donde está la redundancia.

`→` (aparecen los pendientes)

> Y declaro lo que queda fuera: el hub sigue ahí porque el enunciado lo exige; PVST+ en lugar de
> Rapid-PVST+ porque lo fija el carné; el acceso de gestión hoy no tiene contraseña —el banner
> advierte, pero no impide—; y no hay routing inter-VLAN porque está fuera del alcance.

`→` a la 17.

### Plancha 17 · Cierre — 0:20
> *(leer la cita)* Gracias. Tengo los anexos con las salidas completas para lo que quieran preguntar.

---

## Q&A — qué anexo responde cada pregunta

| Pregunta probable | Respuesta corta | Dónde |
|---|---|---|
| ¿Por qué el ping entre VLANs falla? | Porque no hay dispositivo de Capa 3. Es el resultado correcto: demuestra el aislamiento | Plancha **14** y anexo **21** |
| ¿Cómo sé que VTP propagó de verdad? | Por el `show vlan brief` de un Client con VLANs que nunca se crearon ahí, no por el `show vtp status` | Plancha **8** |
| ¿Por qué no pusiste el Core como raíz de todo? | Porque STP bloquea el puerto más lejano a la raíz; con la raíz en el distribuidor, lo bloqueado es el respaldo | Plancha **9** y anexo **20** |
| ¿Qué pasa si cae un switch de I+D? | Nada para los otros dos: tienen uplink propio. Medido: interrupción nula | Plancha **15** |
| ¿Por qué fibra en 90 metros? | Interferencia electromagnética del entorno industrial, más aislamiento galvánico | Plancha **12** |
| ¿El EtherChannel se formó de verdad? | `Po1(SU)` y `Po2(SU)` con los cuatro miembros en `(P)`, y la prueba E14: cae un miembro y el canal no se cae | Plancha **11** |
| ¿Cuántos dominios de colisión hay? | 54: 52 punto a punto y 2 compartidos (el hub y el AP) | Plancha **7** |
| ¿Qué direccionamiento usaste? | Uno por VLAN, sin gateway y sin router, solo para poder hacer ping | Anexo **21** |
| ¿Qué le falta al diseño? | Gestión con contraseña y SSH, Rapid-PVST+, routing inter-VLAN con ACL, y sustituir el hub | Plancha **16** |

---

## Checklist antes de exponer

- [ ] Abrir el **standalone** (`defensa-proyecto1-standalone.html`) — no depende de la carpeta `reveal/` ni de internet
- [ ] `F` para pantalla completa; probar que la primera plancha anima
- [ ] Tener el `.pkt` abierto en otra ventana por si piden ver algo en vivo
- [ ] `M` para saltar a un anexo sin pasar plancha por plancha durante las preguntas
