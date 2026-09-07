---
tags: [redes/proyecto, proyecto1, entregables, checklist]
aliases: ["entregables", "checklist", "README del proyecto", "qué entregar"]
---

# Entregables y checklist del Proyecto 1

Dos archivos dentro de `Proyecto 1/` en el repo, más la parte física en laboratorio.

## A. `Proyecto1_201905884.pkt`
- [ ] Packet Tracer **8.0 o superior**.
- [ ] Las 4 áreas + Core, con los mínimos de [[Requerimientos por área]].
- [ ] Todos los **medios de transmisión etiquetados** en la topología (cobre/fibra por segmento).
- [ ] 100 % de conectividad **intra-VLAN** y aislamiento **inter-VLAN** (objetivo SMART del enunciado).

## B. `README.md` — Manual Técnico (Markdown)
Cada ítem es una sección; la rúbrica los lista uno por uno:
- [ ] Capturas de la **topología completa** y de **cada área**.
- [ ] **Tabla de dominios de colisión**: cuántos genera cada switch (= puertos activos) y cuál es el dominio compartido del hub Legacy. → [[Dominios de colisión y broadcast]]
- [ ] **Tabla de dominios de broadcast**: uno por VLAN activa.
- [ ] **Lista de comandos** usados en **cada dispositivo**. → [[Comandos Cisco IOS del proyecto]]
- [ ] **Tabla de VLANs** (ID, nombre). → [[Parámetros por carné 201905884]]
- [ ] **Tabla de asignación de puertos** por switch (puerto, modo access/trunk, VLAN, dispositivo).
- [ ] Captura + **justificación del switch Server de VTP**.
- [ ] Captura + **justificación del Root Bridge por cada VLAN**.
- [ ] Captura + **justificación de cada EtherChannel**.
- [ ] Evidencia de pruebas: `show spanning-tree`, `show etherchannel summary`, `show interfaces trunk`.
- [ ] **Justificación del medio** de transmisión por segmento (distancia, ancho de banda, buenas prácticas).
- [ ] **Presupuesto** de equipos simulados: switches, módulos de fibra, cableado UTP y fibra.
- [ ] Impacto del segmento Legacy y medidas de contención (lo pide §4.2 explícitamente).
- [ ] (Opcional) Captura de BPDU con Root ID / Bridge ID / costo, y de PDU VTP con domain name / revision number.

## C. Parte física (laboratorio, por pareja)
- [ ] Switch 1 → **VTP Server**; Switch 2 → **VTP Client**.
- [ ] VLANs por carné creadas en el Server y **propagadas** al Client (`show vlan brief` en ambos).
- [ ] Puerto de interconexión en **trunk** con las VLANs permitidas; puertos a PCs en **access**.
- [ ] Coordinar con la pareja: cada uno configura un switch.

## D. Antes de entregar
- [ ] Carpeta se llama exactamente **"Proyecto 1"** en el repo `Redes1_2S_2026_201905884`.
- [ ] Entrega por **UEDI/Classroom** con el enlace al repo.
- [ ] Revisar [[Ambigüedades y riesgos del enunciado]] por si el tutor aclaró algo.

Volver a [[Proyecto 1 - SmartCity Tech Park]].

> 📚 Fuente: enunciado §4.3 "Parte Física", §4.5 "Entregables", §8.1.
