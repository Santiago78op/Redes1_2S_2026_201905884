---
tags: [redes/proyecto, proyecto1, metodo, catedra]
aliases: ["protocolo", "cómo damos la clase", "modo cátedra", "paso a paso", "secuencia de pasos"]
---

# Protocolo de cátedra — cómo trabajamos el Proyecto 1

Este documento define **cómo** se trabaja el proyecto: no de corrido, sino en pasos donde primero se
entiende la teoría y después se implementa esa misma teoría. Lo invoca el slash command **`/paso`**
(definido en `.claude/commands/paso.md`, en la raíz del repo, así que viaja con el `git clone`).

El estado vive en [[AVANCE]]; este archivo solo describe el método y la secuencia.

## El método de cada paso

```
   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
   │ 1. TEORÍA    │──►│ 2. PREGUNTAS │──►│ 3. PRÁCTICA  │──►│ 4. REGISTRO  │
   │ concepto +   │   │ 2-3, hay que │   │ implementar  │   │ AVANCE.md +  │
   │ cita oficial │   │ responderlas │   │ + evidencia  │   │ sección del  │
   │              │   │              │   │              │   │ Manual       │
   └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

Las cuatro etapas son obligatorias y en ese orden. La etapa 2 existe por una razón concreta: si la
implementación empieza antes de que el concepto esté claro, el Manual termina con justificaciones
inventadas al final, y eso es exactamente lo que la rúbrica §8.1 castiga.

## Secuencia de pasos

Cada paso empareja una nota de teoría con una parte de la implementación y cierra una sección del
Manual (`Proyecto 1/README.md`).

| # | Teoría (nota del cerebro) | Práctica | Cierra en el Manual |
|---|---|---|---|
| 1 | [[Dominios de colisión y broadcast]] | Inventario de dispositivos por área y conteo previsto de dominios | §2, §11.1, borrador de §15 y §16 |
| 2 | Medios de transmisión (§8 del Manual) | Elegir cobre o fibra en cada enlace, con su argumento | §8, §20 |
| 3 | Topología jerárquica (§4.2 del enunciado) | Armar la Capa 1 en Packet Tracer: dispositivos, cableado, etiquetas de medio, hub, AP | §11, §12 |
| 4 | [[VLAN y enlaces troncales 802.1Q]] | Crear VLANs, puertos access, trunks con nativa 94 y VLANs permitidas | §4, §13, §14 |
| 5 | [[VTP]] | Core en Server, resto en Client, Áreas Comunes en Transparent; verificar propagación | §5, §17 |
| 6 | [[STP y PVST]] | `spanning-tree mode pvst`, elegir y fijar el Root Bridge por VLAN | §6, §18 |
| 7 | [[EtherChannel LACP]] | Po1 (servidores) y Po2 (I+D) con LACP `active` en ambos extremos | §7, §19 |
| 8 | Seguridad de Capa 2 y segmento Legacy | Banner MOTD, `storm-control`, `port-security`; documentar impacto del hub | §9, §21, §22 |
| 9 | Verificación y evidencia | Los tres `show`, pings intra e inter-VLAN, pruebas de falla | §24 y `capturas/EVIDENCIAS.md` |
| 10 | Redacción y cierre | Completar el Manual, presupuesto, conclusiones y referencias | §26, §28, §29 |
| 11 | Parte física | Dos switches reales con la pareja: Server + Client, trunk, access | §25 |

El paso 11 depende del calendario del laboratorio: puede adelantarse sin romper la secuencia, porque
solo necesita la teoría de los pasos 4 y 5.

## Reglas de trabajo

| Regla | Por qué |
|---|---|
| Los comandos se copian a `configs/<hostname>.txt` y a §23 **en el momento** | Reconstruirlos después cuesta el doble y se pierden detalles |
| Cada decisión se anota en [[AVANCE]] **con su porqué** | Es el borrador de la justificación que pide la rúbrica |
| Los valores por carné se verifican antes de teclear | Un ID de VLAN mal puesto penaliza del -50 % al -100 % |
| El `.pkt` se guarda por fase en local (`Proyecto1_201905884_fN.pkt`) | Permite volver atrás sin rearmar |
| Los commits los hace el estudiante | Convención del repositorio |

## Cómo usarlo en cualquier máquina

No hay pasos manuales: tanto el comando como el contexto (`Proyecto 1/CLAUDE.md` y esta carpeta)
están versionados.

```bash
git clone <repo> && cd <repo>
claude          # y adentro:  /paso
```

`/paso` sin argumentos continúa donde marca [[AVANCE]]. También acepta `/paso 4` (ir a un paso
concreto), `/paso siguiente` y `/paso repasar 6` (solo la teoría, sin implementar).

> 📚 Método propio, derivado de la rúbrica §8.1 del enunciado y del estilo de la Práctica 1.
