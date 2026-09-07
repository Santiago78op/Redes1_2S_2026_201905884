# Proyecto 1 — "SmartCity Tech Park" · Contexto para Claude Code

> Archivo de contexto **portable y versionado**: viaja con el repo dentro de `Proyecto 1/wiki/`. Lo importa `Proyecto 1/CLAUDE.md` —también versionado— con la línea `@wiki/CONTEXTO-CLAUDE.md`, así que Claude Code lo carga solo al abrir la carpeta, en cualquier máquina y sin instalar nada. Contiene todo lo que Claude necesita saber para continuar el proyecto sin releer el enunciado.

## Quién y qué
- **Curso:** Redes de Computadoras 1, USAC, Facultad de Ingeniería, 2S-2026. Ponderación **22 pts**, 35 h estimadas.
- **Estudiante:** Santiago Barrera, carné **201905884**. Repo `Redes1_2S_2026_201905884`, carpeta `Proyecto 1/`.
- **Entrega:** elaboración hasta el **17/09/2026**; calificación 18–19/09/2026, vía UEDI/Classroom.
- **Problema:** campus tecnológico con red plana (maquinaria Legacy, servidores e invitados en un mismo dominio de broadcast, un solo dominio de colisión industrial, enlaces únicos sin redundancia). Se rediseña Capa 1 y Capa 2 en **Cisco Packet Tracer ≥ 8.0**.
- **Enunciado:** `doc/0972_Proyecto_1_2S2026.pdf` (+ `.md` convertido, ambos ignorados en git). **Está incompleto:** el índice va corrido una página y, además, §8.2 *Detalle de la Calificación* y §8.3 no existen en el archivo (solo en el índice); la §6 *Metodología* viene vacía. Pedir la versión completa.
- **Análisis completo y autocontenido:** `wiki/analisis-enunciado.md` — leerlo primero al retomar el proyecto en otra máquina.

## Parámetros por carné (NO cambiar: penaliza -50 % a -100 %)
| Ítem | Valor |
|---|---|
| VLANs | **14** Gerencia (Corporativo) · **24** Investigacion (I+D) · **34** Produccion (Planta) · **44** Servidores (Centro de Datos) · **54** Visitantes (Corporativo, Áreas Comunes) |
| VLAN nativa de todos los trunks | **94** |
| Dominio VTP / contraseña | `Smart_8` / `proyecto12S2026` |
| EtherChannel | **LACP** (carné par) |
| STP | **PVST** (`spanning-tree mode pvst`, carné par) |
| Banner MOTD (distribución) | `Acceso Restringido - TechPark_201905884` |
| Archivo | `Proyecto1_201905884.pkt` |
| Manual Técnico | `Proyecto 1/README.md` en Markdown |

Duda abierta: la tabla del enunciado escribe `Gerencia` pero el ejemplo dice "exactamente `GERENCIA`". Si el tutor no aclara, usar MAYÚSCULAS.

## Requerimientos por área (mínimos obligatorios)
1. **Centro de Datos (Core):** VTP **Server**; trunks a los 3 edificios; granja de **≥ 4 servidores** conectada por un enlace de alto tráfico **redundante** (EtherChannel LACP).
2. **Centro de I+D:** **≥ 3 switches** interconectados entre sí (caída de uno no aísla a los demás); su trunk al Core es el de **mayor ancho de banda** del campus; **≥ 8 PCs/laptops**.
3. **Edificio Corporativo:** **2 alas** con switch de acceso cada una; conectividad entre alas debe sobrevivir a la caída de la ruta al distribuidor (enlace directo entre alas + STP); **Áreas Comunes** para visitantes con aislamiento total de tráfico y de administración de VLANs (VTP Transparent propuesto), con **Access Point** para laptops.
4. **Planta de Producción (Legacy):** un **hub** con las máquinas industriales conectado a un switch de acceso, mostrando un dominio de colisión compartido; documentar impacto y medidas de contención en el switch (storm-control, port-security, VLAN 34).
5. **Transversal:** justificar el medio (cobre/fibra) de cada enlace por distancia, ancho de banda y buenas prácticas; etiquetar los medios en el `.pkt`.
6. **Parte física (lab, por pareja):** 2 switches reales, uno VTP Server y otro Client, trunk entre ellos, puertos access a PCs, VLANs propagadas.

## Entregables del README.md
Capturas (topología completa + cada área) · tabla de dominios de colisión (por switch = puertos activos; el compartido del hub) · tabla de dominios de broadcast (uno por VLAN) · lista de comandos por dispositivo · tabla de VLANs · tabla de puertos por switch · captura + justificación del VTP Server · captura + justificación del Root Bridge por VLAN · captura + justificación de cada EtherChannel · evidencia de `show spanning-tree`, `show etherchannel summary`, `show interfaces trunk` · justificación de medios · presupuesto (switches, módulos de fibra, UTP, fibra) · impacto y contención del segmento Legacy. Opcional: capturas de BPDU y PDU VTP en Modo Simulación.

## Requisitos para optar a nota
Carpeta exactamente **"Proyecto 1"** en el mismo repo de la práctica · entrega por UEDI/Classroom · Manual en Markdown · esquema de VLANs por carné · **originalidad** (topología idéntica a otro = copia).

## Decisiones de diseño (estado al 2026-09-07)
- Cerradas: ninguna todavía, solo los parámetros por carné.
- Propuestas por justificar: EtherChannel para servidores e I+D; anillo de 3 switches en I+D; triángulo distribuidor–Ala A–Ala B; Áreas Comunes en VTP Transparent; Root Bridge = Core para VLANs 14/34/44/54 y por decidir para la 24; fibra entre edificios, UTP dentro.

## Modo de trabajo: clase guiada paso a paso

El proyecto se trabaja **enseñando la teoría y aplicándola en el mismo paso**, no de corrido. El
método y la secuencia de los 11 pasos están en `wiki/PROTOCOLO-CATEDRA.md`; el estado actual (paso en
curso, decisiones tomadas con su justificación, dudas abiertas) en **`wiki/AVANCE.md`**, que es la
fuente de verdad del progreso.

Se invoca con el slash command **`/paso`** (`.claude/commands/paso.md`, versionado: viaja con el
`git clone`). Cada paso tiene cuatro etapas obligatorias en orden: **teoría con cita oficial →
2-3 preguntas de comprensión que el estudiante debe responder → implementación → registro en
`AVANCE.md` y en la sección del Manual**. Al retomar el proyecto en cualquier máquina: leer
`AVANCE.md` y escribir `/paso`.

## Cómo trabajar conmigo en este proyecto
- Los commits y pushes los hace el usuario; Claude no commitea.
- **El proyecto se trabaja en dos marcos, como en la Práctica 1:**
  - **Marco Teórico**: los conceptos que sustentan cada decisión (dominios de colisión/broadcast, VLAN/802.1Q, VTP, STP/PVST, EtherChannel/LACP, medios de transmisión, seguridad básica), redactados con definiciones, comparaciones y referencias, antes de configurar nada. Fuente: notas de `wiki/02 - Conceptos Capa 2/`.
  - **Marco Práctico**: la implementación (topología, tablas de VLANs/puertos/dominios, comandos por dispositivo, capturas de `show`, justificaciones de Root Bridge/EtherChannel/medios, presupuesto). Cada decisión práctica cita la sección teórica que la respalda.
  - En la Práctica 1 esto se materializó en dos documentos: `../Practica1/ManualTecnico.md` (23 secciones) e `../Practica1/InformeDesarrollo.md` (proceso, criterios, retos, conclusiones). Reutilizar su encabezado institucional, índice numerado, tablas y sección de referencias.
- Todo comando ejecutado se copia al README de inmediato, por dispositivo.
- Toda decisión de diseño se anota con su justificación en el momento (la rúbrica califica la justificación).
- Conocimiento ampliado (conceptos con citas oficiales, comandos con los valores ya sustituidos, ambigüedades del enunciado, calendario): **esta misma carpeta `wiki/`**, que es una bóveda Obsidian de 20 notas versionada en el repo y registrada como cerebro diamon `redes` en el `brains.json` de la PC principal. Índice: `wiki/00 - 🌐 Cerebro Redes (MOC).md`.

## Estructura de la carpeta (creada el 2026-09-07)
```
Proyecto 1/
├── CLAUDE.md                    ← importa wiki/CONTEXTO-CLAUDE.md (versionado: viaja al clonar)
├── README.md                    ← Manual Técnico (PLANTILLA: Parte I Marco Teórico §1–9, Parte II Marco Práctico §10–29)
├── Proyecto1_201905884.pkt      ← topología (entregable; se genera en Packet Tracer)
├── capturas/
│   ├── EVIDENCIAS.md            ← índice de capturas con convención NN-<dispositivo>-<comando>.png
│   ├── topologia/  areas/  evidencias/  laboratorio/
├── configs/                     ← running-config por switch (<hostname>.txt); README con cabecera obligatoria
├── diagrama/                    ← figuras SVG propias (README con índice)
├── doc/                         ← enunciado PDF/MD (ignorados en git)
├── wiki/                        ← cerebro del proyecto (versionado, viaja con el push)
│   ├── AVANCE.md                ← estado del progreso: LEER PRIMERO
│   ├── PROTOCOLO-CATEDRA.md     ← método paso a paso y secuencia de los 11 pasos
└── cerebro/                     ← notas personales locales, si hacen falta (no versionado)

.claude/commands/paso.md         ← (raíz del repo) el slash command /paso, versionado
```
Las guías de redacción de la plantilla van en comentarios HTML `<!-- -->`; se borran al cerrar cada sección.

## Retomar el proyecto en otra PC

Sin pasos manuales: el contexto (`Proyecto 1/CLAUDE.md` + `wiki/`) y el comando
(`.claude/commands/paso.md`) están versionados.

```bash
git clone https://github.com/Santiago78op/Redes1_2S_2026_201905884.git
cd Redes1_2S_2026_201905884
claude          # y adentro:  /paso
```

Dos aclaraciones sobre lo que **no** viaja, para no buscarlo: la memoria de Claude vive en
`~/.claude/projects/…/memory/` de cada máquina, y el output style «Catedrático» también es local. Por
eso todo lo que importa está acá, en el repo, y el comando `/paso` trae sus propias reglas de
redacción.

Opcional, si esa máquina tiene diamon: agregar en `brains.json`, mundo `personal`,
`"redes": "<ruta-del-repo>/Proyecto 1/wiki"` y reiniciar la sesión.
