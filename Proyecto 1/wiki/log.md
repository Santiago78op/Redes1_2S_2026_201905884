# Bitácora del cerebro `redes`

## [2026-09-07] ingest | Creación del cerebro y carga del Proyecto 1 "SmartCity Tech Park"
Se convirtió `0972_Proyecto_1_2S2026.pdf` (11 páginas) con markitdown + pdfplumber. Se crearon el MOC, 6 notas del proyecto y 6 notas de conceptos de Capa 2. Hallazgo: el PDF está incompleto (faltan §8.2 y §8.3; §6 vacía).

## [2026-09-07] lint | Verificación de integridad del PDF
Se comprobó página por página: índice corrido una página; §8.2/§8.3 solo existen en el índice. Copia portable del análisis en `Proyecto 1/cerebro/analisis-enunciado.md` (repo del curso, fuera de git).

## [2026-09-07] lint | Mudanza al repo
El cerebro se movió de `C:/mcp/brains/personal/redes` a `Proyecto 1/wiki/` (versionado; `brains.json` re-apuntado). Se sumaron `CONTEXTO-CLAUDE.md` (importado por el stub `CLAUDE.md`) y `analisis-enunciado.md`.

## [2026-09-07] ingest | Convención Marco Teórico / Marco Práctico
El Manual se redacta en dos marcos, como la Práctica 1: teoría (notas de `02 - Conceptos Capa 2/`) y práctica (implementación con evidencia). Registrado en `CONTEXTO-CLAUDE.md` y `Entregables y checklist`.

## [2026-09-07] ingest | Estructura de entregables
Se crearon `README.md` (plantilla del Manual en dos marcos, 29 secciones), `capturas/` (4 subcarpetas + EVIDENCIAS.md), `configs/` y `diagrama/` con sus README. El árbol quedó en `CONTEXTO-CLAUDE.md`.

## [2026-09-07] ingest | Teoria contrastada con la documentacion Cisco del enunciado
Se consultaron los 4 enlaces oficiales de §5 (VLAN Trunks, VTP 10558, STP 2960, EtherChannel 2960) y se enriquecieron las notas con citas y numeros verificados: costos STP por velocidad, prioridad 32768 / extended system ID, temporizadores 2/15/20 s y ~50 s de convergencia, priority multiplo de 4096 y root primary = 24576, tabla DTP, limite de 8 puertos y 6 canales, balanceo por flujo. Dos correcciones: la nativa desalineada **puede provocar bucles** (no solo un aviso de CDP), y PVST no es 'el modo por defecto' sino el que se selecciona con `spanning-tree mode pvst`.

## [2026-09-07] ingest | Modo clase guiada paso a paso
Se creo el slash command de proyecto `/paso` (`.claude/commands/paso.md`, versionado), el `PROTOCOLO-CATEDRA.md` (metodo de 4 etapas + secuencia de 11 pasos) y `AVANCE.md` (estado del progreso, fuente de verdad). Hallazgo: `.claude/` estaba entero en `.git/info/exclude`, lo que habria impedido que el comando viajara al remoto; se estrecho a `.claude/settings.local.json`.

## [2026-09-07] lint | Refresco del cerebro y contexto sin pasos manuales
Se reviso el cerebro completo (20 notas). El MOC lista ahora `CONTEXTO-CLAUDE`, `analisis-enunciado`, `log` y `README`, y declara el conteo. Se reconcilio la doble vista del trabajo: `Plan de trabajo` es el calendario (8 fases con fecha) y `PROTOCOLO-CATEDRA` la secuencia didactica (11 pasos), con tabla de correspondencia entre ambas. Se corrigieron las referencias obsoletas a `C:/mcp/brains/personal/redes` y al conteo de 16 notas en `analisis-enunciado` §13 y en `AVANCE`. El Glosario sumo DTP, Bridge ID, port-channel, PortFast, storm-control y port-security. Cambio de fondo: el patron `CLAUDE.md` del `.git/info/exclude` se anclo a la raiz (`/CLAUDE.md`), asi `Proyecto 1/CLAUDE.md` quedo versionado y en otra maquina ya no hay que crearlo a mano: clonar y `/paso`.
