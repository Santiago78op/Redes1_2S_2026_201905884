---
tags: [redes/proyecto, proyecto1, estado, bitacora]
aliases: ["avance", "estado", "dónde quedamos", "progreso", "bitácora del proyecto"]
paso_actual: 1
actualizado: 2026-09-07
---

# Avance del Proyecto 1 — estado actual

> **Este archivo es la fuente de verdad del progreso.** `/paso` lo lee al arrancar y lo actualiza al
> cerrar cada paso. Si trabajás en otra máquina, esto es lo que te dice dónde quedaste.
> Método y secuencia completa: [[PROTOCOLO-CATEDRA]].

## Estado

| Dato | Valor |
|---|---|
| **Paso actual** | **1 — Dominios de colisión y broadcast** (no iniciado) |
| Pasos completados | 0 de 11 |
| Última sesión | 2026-09-07 — se montó el material y la estructura de entregables |
| Días hasta la entrega | 17/09/2026 |

## Tablero de pasos

| # | Paso | Estado | Cerrado el |
|---|---|---|---|
| 1 | Dominios de colisión y broadcast → inventario | ⬜ pendiente | |
| 2 | Medios de transmisión → elección por enlace | ⬜ pendiente | |
| 3 | Topología jerárquica → Capa 1 en Packet Tracer | ⬜ pendiente | |
| 4 | VLANs y trunks 802.1Q → VLANs, access, trunks | ⬜ pendiente | |
| 5 | VTP → Server, Client, Transparent | ⬜ pendiente | |
| 6 | STP y PVST+ → Root Bridge por VLAN | ⬜ pendiente | |
| 7 | EtherChannel LACP → Po1 y Po2 | ⬜ pendiente | |
| 8 | Seguridad de Capa 2 y segmento Legacy | ⬜ pendiente | |
| 9 | Verificación y evidencia | ⬜ pendiente | |
| 10 | Redacción y cierre del Manual | ⬜ pendiente | |
| 11 | Parte física en laboratorio | ⬜ pendiente | |

Leyenda: ⬜ pendiente · 🟡 en curso · ✅ cerrado

## Decisiones tomadas (con su justificación)

<!-- Al cerrar cada paso, agregar aquí las decisiones con su porqué. Este es el borrador literal de
las justificaciones del Manual, así que escribirlas completas, no en clave. -->

| # | Decisión | Justificación | Paso | Sección del Manual |
|---|---|---|---|---|
| — | *(ninguna todavía; solo están fijados los parámetros por carné, que no son decisión propia)* | | | |

## Dudas abiertas para el tutor

| # | Duda | Estado |
|---|---|---|
| 1 | El PDF del enunciado no incluye §8.2 *Detalle de la Calificación* ni §8.3 (solo aparecen en el índice); §6 *Metodología* está vacía. Pedir la versión completa. | ⬜ sin preguntar |
| 2 | Los nombres de VLAN: la tabla escribe `Gerencia`, el ejemplo dice "exactamente GERENCIA". ¿Mayúsculas obligatorias? | ⬜ sin preguntar |
| 3 | Fecha del laboratorio de la parte física y confirmación de la pareja. | ⬜ sin preguntar |

Detalle completo de las diez ambigüedades detectadas: [[Ambigüedades y riesgos del enunciado]].

## Bitácora de sesiones

### 2026-09-07 — Montaje
- Se analizó el enunciado (`analisis-enunciado.md`) y se detectó que el PDF está incompleto.
- Se creó el cerebro del proyecto en `Proyecto 1/wiki/` (20 notas, versionadas) y se contrastó la
  teoría de Capa 2 con los cuatro enlaces oficiales del §5 del enunciado, corrigiendo dos puntos: una
  VLAN nativa desalineada **puede producir bucles de STP** (no es solo un aviso de CDP) y PVST no es
  «el modo por defecto», sino el que se selecciona con `spanning-tree mode pvst`.
- Se creó la estructura de entregables: plantilla del Manual en dos marcos (§1–9 teórico, §10–29
  práctico), `capturas/` con cuatro subcarpetas e índice, `configs/` y `diagrama/`.
- Se definió el modo de trabajo paso a paso: [[PROTOCOLO-CATEDRA]] + comando `/paso`.
- Se hizo portable el contexto: `Proyecto 1/CLAUDE.md` y `.claude/commands/paso.md` quedaron
  **versionados**, así que en otra máquina basta clonar y escribir `/paso`, sin copiar archivos.
- **Nada implementado aún en Packet Tracer.**

<!-- Agregar una entrada por sesión: qué se explicó, qué se implementó, qué quedó pendiente. -->
