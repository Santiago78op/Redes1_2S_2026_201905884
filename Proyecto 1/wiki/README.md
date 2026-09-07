# wiki/ — cerebro del Proyecto 1

Bóveda Obsidian con el conocimiento de trabajo del proyecto: contexto para Claude Code, análisis del enunciado, decisiones de diseño y conceptos de Capa 2. **No es un entregable**; el Manual Técnico es `../README.md`.

| Archivo | Para qué |
|---|---|
| `CONTEXTO-CLAUDE.md` | Lo que Claude Code debe saber al abrir el proyecto. El `../CLAUDE.md` local lo importa con `@wiki/CONTEXTO-CLAUDE.md`. |
| `analisis-enunciado.md` | Análisis completo y autocontenido del PDF del enunciado. |
| `00 - 🌐 Cerebro Redes (MOC).md` | Índice de las notas; empezar por acá. |
| `01 - Proyecto 1 SmartCity/` | Resumen, parámetros por carné, áreas, entregables, ambigüedades, plan. |
| `02 - Conceptos Capa 2/` | Dominios, VLAN/802.1Q, VTP, STP/PVST, EtherChannel/LACP, comandos IOS. |
| `Glosario.md` · `log.md` | Términos en una línea · bitácora de cambios del cerebro. |

## Usarla en otra PC
1. Crear `Proyecto 1/CLAUDE.md` con una sola línea: `@wiki/CONTEXTO-CLAUDE.md`.
2. Si hay diamon: en `brains.json`, mundo `personal`, agregar `"redes": "<ruta-del-repo>/Proyecto 1/wiki"` y reiniciar la sesión.
