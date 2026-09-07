---
tags: [redes/proyecto, proyecto1, smartcity, capa2]
aliases: ["Proyecto 1", "SmartCity", "Tech Park", "proyecto redes"]
estado: en-curso
entrega: 2026-09-17
ponderacion: 22
---

# Proyecto 1 — "SmartCity Tech Park"

**Curso:** Redes de Computadoras 1 · USAC · 2S-2026 · **22 pts** · 35 h estimadas.
**Estudiante:** Santiago Barrera · carné **201905884** · repo `Redes1_2S_2026_201905884`, carpeta `Proyecto 1/`.

## El problema (en una frase)
Un campus tecnológico creció con red **plana**: maquinaria industrial, servidores críticos e invitados comparten un mismo dominio de broadcast, el segmento industrial arrastra **un solo dominio de colisión**, y las áreas críticas dependen de **un único cable**. Hay que rediseñar Capa 1 y Capa 2 desde cero.

## Lo que se pide (alcance obligatorio)
1. **Topología jerárquica**: switch central en el Centro de Datos + troncales a los switches de distribución de 3 edificios. Justificar el medio (cobre/fibra) de cada enlace. → [[Requerimientos por área]]
2. **Segmento Legacy**: un **hub** en la Planta de Producción colgado de un switch de acceso, y documentar su impacto y mitigaciones.
3. **VTP**: dominio y contraseña fijos; modo de cada switch según su rol. → [[VTP]]
4. **5 VLANs por carné**, creadas en el Server y propagadas. → [[Parámetros por carné 201905884]]
5. **EtherChannel** donde haga falta (LACP para mí). → [[EtherChannel LACP]]
6. **STP** (PVST para mí) con Root Bridge justificado por VLAN. → [[STP y PVST]]
7. **Seguridad básica**: banner MOTD en distribución + VLAN nativa 9X en todos los trunks.
8. **Parte física** (laboratorio, por pareja): 2 switches reales, uno VTP Server y otro Client, trunk entre ellos, puertos access hacia PCs.

**Opcional** (suma comprensión, no está claro si suma puntos): capturar en Modo Simulación una BPDU (Root ID, Bridge ID, costo) y una PDU VTP (domain name, revision number).

## Cronograma oficial
| Fase | Inicio | Fin |
|---|---|---|
| Asignación | 28/08/2026 | 28/08/2026 |
| Elaboración | 28/08/2026 | **17/09/2026** |
| Calificación | 18/09/2026 | 19/09/2026 |

## Requisitos para optar a nota (si falla uno → 0 pts)
- Mismo repositorio de la práctica, carpeta **"Proyecto 1"** con los entregables.
- Entrega por **UEDI o Classroom**; otro medio se anula.
- Manual Técnico en **Markdown** dentro de la carpeta.
- Esquema de VLANs por carné: no seguirlo penaliza **-50 % a -100 %**.
- **Originalidad**: topología idéntica a la de otro = copia, aunque cambien los parámetros. Las decisiones (dónde va la redundancia, qué enlace es el gordo, medio, Root Bridge) deben ser propias y justificadas.

## Entregables
Ver [[Entregables y checklist]]: `Proyecto1_201905884.pkt` + `README.md` (Manual Técnico) con capturas, tablas de dominios, comandos, VLANs, puertos, justificaciones, evidencia de `show`, etiquetado de medios y presupuesto.

## Estado actual (2026-09-07)
- [x] Enunciado leído y convertido a `.md`.
- [x] Parámetros por carné calculados.
- [ ] Diseño de topología (bosquejo por área).
- [ ] Implementación en Packet Tracer.
- [ ] Manual Técnico.
- [ ] Parte física en laboratorio (coordinar pareja).
- [ ] **Pedir el PDF completo**: faltan §8.2 y §8.3 (ver [[Ambigüedades y riesgos del enunciado]]).

Seguí con [[Plan de trabajo Proyecto 1]].

> 📚 Fuente: `Proyecto 1/doc/0972_Proyecto_1_2S2026.pdf`, §3, §4, §7, §8.1.
