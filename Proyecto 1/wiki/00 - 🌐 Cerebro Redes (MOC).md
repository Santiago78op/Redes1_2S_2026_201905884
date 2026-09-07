---
tags: [moc, redes, indice]
aliases: [Inicio, Home, Cerebro Redes, MOC, Redes 1]
cssclasses: []
---

# 🌐 Cerebro Redes — Mapa de Contenido (MOC)

> [!info] ¿Qué es esto?
> Base de conocimiento del curso **Redes de Computadoras 1** (USAC, Facultad de Ingeniería, 2S-2026). Guarda el contexto de cada proyecto del curso (qué pide el enunciado, qué parámetros me tocan por carné, qué decidí y por qué) y los conceptos de red necesarios para defenderlos. Claude Code se apoya en estas notas para trabajar el proyecto en cualquier máquina.
>
> Estudiante: **Santiago Barrera — carné 201905884**. Repositorio: `Redes1_2S_2026_201905884`.
>
> **20 notas.** Esta carpeta (`Proyecto 1/wiki/`) está **versionada**: viaja con el `git clone`, así que el cerebro es el mismo en todas las máquinas. También está registrada como cerebro diamon `redes` en `C:\mcp\brains.json` de la PC principal.

---

## 🗺️ Mapa del conocimiento

### 00 · Cómo trabajamos
- [[AVANCE]] — **empezá por acá**: en qué paso vamos, decisiones tomadas con su justificación, dudas abiertas
- [[PROTOCOLO-CATEDRA]] — el método de clase guiada (teoría → preguntas → práctica → registro) y la secuencia de los 11 pasos
- [[CONTEXTO-CLAUDE]] — el resumen que Claude Code carga solo al abrir la carpeta
- [[analisis-enunciado]] — análisis completo y autocontenido del PDF oficial, sección por sección

### 01 · Proyecto 1 — SmartCity Tech Park (Capa 1 y Capa 2)
- [[Proyecto 1 - SmartCity Tech Park]] — resumen del enunciado, fechas, rúbrica y estado actual
- [[Parámetros por carné 201905884]] — VLANs, dominio VTP, nativa, LACP/PVST, banner: todo ya sustituido
- [[Requerimientos por área]] — qué exige cada uno de los 4 edificios y cómo pienso resolverlo
- [[Entregables y checklist]] — lo que debe contener el `README.md` y el `.pkt`, con casillas
- [[Ambigüedades y riesgos del enunciado]] — lo que el PDF no dice o dice mal, y qué decidí
- [[Plan de trabajo Proyecto 1]] — el **calendario**: 8 fases con fecha meta (el PDF trae la sección de metodología vacía). La secuencia didáctica va en [[PROTOCOLO-CATEDRA]]

### 02 · Conceptos de Capa 2 (los que se evalúan)
- [[Dominios de colisión y broadcast]] — cómo contarlos por switch, hub y VLAN
- [[VLAN y enlaces troncales 802.1Q]] — segmentación, trunk, VLAN nativa
- [[VTP]] — Server / Client / Transparent y el número de revisión
- [[STP y PVST]] — Root Bridge, BPDU, costo, por qué no hay bucles
- [[EtherChannel LACP]] — agregación de enlaces, modos active/passive
- [[Comandos Cisco IOS del proyecto]] — cheat sheet con mis parámetros ya puestos

### Referencia
- [[Glosario]] — términos del curso en una línea
- [[log]] — bitácora del cerebro (append-only)
- [[README]] — qué es cada archivo de esta carpeta y cómo usarla en otra máquina

---

## 🧭 Cómo usar este cerebro
0. Escribí `/paso` en Claude Code: lee [[AVANCE]] y da la clase del paso que toca.
1. Empezá por [[Proyecto 1 - SmartCity Tech Park]] para saber en qué estamos.
2. Antes de configurar algo, verificá el valor en [[Parámetros por carné 201905884]]: una VLAN mal numerada penaliza del -50 % al -100 %.
3. Toda decisión de diseño se anota en [[Requerimientos por área]] con su justificación, porque la rúbrica exige justificarla en el Manual Técnico.

> 📚 Fuente base: `Proyecto 1/doc/0972_Proyecto_1_2S2026.pdf` (enunciado oficial) y su conversión `.md` en la misma carpeta.
