# Diagramas — Práctica 1, QuetzalDev S.A.

Figuras del Manual Técnico. Todas en SVG (vectorial, escalable, editable en draw.io, Inkscape,
Illustrator o Excalidraw).

## Diagramas sobre el plano arquitectónico

Ambos se dibujan **sobre `../doc/Plano3.png`**, tal como exige el enunciado. El plano de fondo se
referencia con ruta relativa y se muestra al 28 % de opacidad para que la red domine visualmente.

| Archivo | Sección | Qué muestra |
| --- | --- | --- |
| `trazado-sobre-plano.svg` | §5 · §7 · §9 · §14 | **Vista física.** Canalización en sus tres tramos, MDF, 7 gabinetes, los 8 enlaces troncales con su longitud, y las 22 tomas con su número de puertos. Los enlaces van en ángulos rectos siguiendo la canalización real. |
| `topologia-sobre-plano.svg` | §6 | **Vista topológica.** La estrella extendida de dos niveles: 8 estrellas departamentales colgando de la estrella troncal del MDF. Enlaces rectos —adyacencia lógica, no recorrido—, con la criticidad de cada segmento. |

> **Nota de calibración.** El plano base **no está dibujado a escala uniforme**: la franja superior,
> la central y el Área Abierta tienen escalas distintas (de 34.5 a 45 px/m). Por eso el mapeo de
> metros a píxeles de estos dos diagramas es lineal **por tramos**, calibrado sobre la posición real
> de los muros medida en la imagen. Es también la razón por la que todas las distancias del manual se
> calculan sobre las cotas rotuladas y nunca midiendo el dibujo (véase §2.1).

## Figuras analíticas

| Archivo | Sección | Qué muestra |
| --- | --- | --- |
| `topologias-comparadas.svg` | §6.3 | Las cuatro topologías evaluadas dibujadas con cinco nodos: estrella (adoptada), bus, anillo y malla completa. |
| `enlaces-estrella-vs-malla.svg` | §6.3 | Enlaces necesarios según el número de hosts. La malla crece como n(n−1)/2: 45 enlaces en Capacitación contra 10. |
| `margen-de-distancia.svg` | §8.1 · §8.3 | Capacidad de cada medio frente al uso real, en escala común. Demuestra que la distancia no discrimina entre opciones. |
| `ciclo-de-vida-planta.svg` | §8.1 | Vida útil de la planta pasiva frente a la activa: el cable ve pasar cuatro generaciones de switches. |
| `corte-enlace-horizontal.svg` | §10.1 | Corte constructivo de un enlace. De dónde salen los 3.2 m de tramo vertical que se suman a cada cable. |
| `regla-switch-panel.svg` | §11.3 | Verificación de la regla *switch ≥ patch panel* en las nueve ubicaciones, bajo las dos lecturas posibles. |

## Entregable

`Plano.excalidraw` es el archivo de trabajo del diagrama entregable. Los SVG de esta carpeta sirven
como base geométrica y de referencia: pueden importarse directamente en Excalidraw o draw.io.

## Paleta

Consistente en todas las figuras, y validada para daltonismo y contraste:

| Color | Uso |
| --- | --- |
| `#0E8F7E` | Cableado horizontal · tomas · estrella adoptada |
| `#1668B8` / `#0B4F8F` | Cableado troncal · switch principal |
| `#C08214` | Canalización |
| `#B4243C` | MDF |
| `#9AA9B6` | Opciones evaluadas y descartadas |
| `#C0392B` | Elemento en falla |

## Si el visor no renderiza SVG

GitHub muestra SVG en Markdown sin problema. Si el destino final lo requiere en mapa de bits,
exportá a PNG desde Excalidraw, draw.io o el navegador (abrir el SVG e imprimir a PDF/PNG).
