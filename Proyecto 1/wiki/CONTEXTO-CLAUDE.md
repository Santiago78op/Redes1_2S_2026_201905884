# Proyecto 1 — "SmartCity Tech Park" · Contexto para Claude Code

> Archivo de contexto **portable y versionado**: viaja con el repo dentro de `Proyecto 1/wiki/`. El `Proyecto 1/CLAUDE.md` local (excluido de git) es solo un stub de una línea, `@wiki/CONTEXTO-CLAUDE.md`, que importa este archivo para que Claude Code lo cargue automáticamente. Contiene todo lo que Claude necesita saber para continuar el proyecto sin releer el enunciado.

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

## Cómo trabajar conmigo en este proyecto
- Los commits y pushes los hace el usuario; Claude no commitea.
- Estilo del Manual: seguir el de `../Practica1/ManualTecnico.md` (encabezado institucional, índice numerado, tablas, referencias).
- Todo comando ejecutado se copia al README de inmediato, por dispositivo.
- Toda decisión de diseño se anota con su justificación en el momento (la rúbrica califica la justificación).
- Conocimiento ampliado (conceptos, comandos con valores sustituidos, ambigüedades, plan): cerebro diamon `redes` en `C:\mcp\brains\personal\redes` (solo existe en la PC principal).

## Estructura prevista de la carpeta
```
Proyecto 1/
├── CLAUDE.md                    ← stub local: @wiki/CONTEXTO-CLAUDE.md (no versionado)
├── README.md                    ← Manual Técnico (entregable)
├── Proyecto1_201905884.pkt      ← topología (entregable)
├── doc/                         ← enunciado PDF/MD (ignorados en git)
├── wiki/                        ← cerebro del proyecto (versionado, viaja con el push)
│   ├── CONTEXTO-CLAUDE.md       ← este archivo
│   ├── analisis-enunciado.md    ← análisis completo del enunciado
│   ├── 00 - 🌐 Cerebro Redes (MOC).md
│   ├── 01 - Proyecto 1 SmartCity/  y  02 - Conceptos Capa 2/
│   └── Glosario.md · log.md
├── cerebro/                     ← notas personales locales, si hacen falta (no versionado)
├── capturas/                    ← evidencias PNG para el README
└── configs/                     ← running-config exportada por switch
```

## Instalar el contexto en otra PC (2 pasos)
1. Clonar el repo y crear el stub: en `Proyecto 1/` un archivo `CLAUDE.md` con la única línea `@wiki/CONTEXTO-CLAUDE.md`.
2. (Opcional, si esa PC tiene diamon) agregar en `brains.json`, mundo `personal`: `"redes": "<ruta-del-repo>/Proyecto 1/wiki"` y reiniciar la sesión.
