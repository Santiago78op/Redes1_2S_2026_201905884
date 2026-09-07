---
tags: [redes/proyecto, proyecto1, riesgos, decisiones]
aliases: ["ambigüedades", "riesgos", "dudas del enunciado", "preguntas al tutor"]
---

# Ambigüedades y riesgos del enunciado

Lo que el PDF **no dice, dice a medias o dice mal**, con la decisión tomada o la pregunta pendiente. Cada decisión cerrada debe reflejarse también en el Manual Técnico.

| # | Hallazgo | Riesgo | Decisión / acción |
|---|---|---|---|
| 1 | **El PDF está incompleto**: el índice anuncia §8.2 *Detalle de la Calificación* (pág. 12) y §8.3 *Comentarios Generales* (pág. 15), pero el archivo termina en la pág. 11. Se verificó que la numeración del índice va corrida una página **y** que los textos "8.2", "8.3" y sus títulos aparecen únicamente en la página del índice. La §6 *Metodología* está vacía (página rasterizada para confirmarlo). | No sé cómo se reparten los 22 pts ni qué pesa más. | **Pedir el PDF completo** al tutor / Classroom. Mientras, priorizar según la lista de entregables. |
| 2 | Nombre de VLAN: la tabla dice `Gerencia`, el ejemplo dice "exactamente **GERENCIA**". | Rúbrica puede pedir coincidencia exacta. | ✍️ Preguntar. Si no hay respuesta, usar **MAYÚSCULAS** (es lo que el texto enfatiza con "exactamente"). |
| 3 | El repo debe llamarse `Redes1_1S_2026_Carnet` según §8.1, pero el curso es **2S** y la práctica ya vive en `Redes1_2S_2026_201905884`. | Ninguno real: el texto dice "el mismo repositorio de la práctica". | Mantener el repo actual. Es un error tipográfico del enunciado. |
| 4 | "Aislar completamente el tráfico **y la administración de VLANs**" en Áreas Comunes, pero la VLAN 54 debe crearse en el Server y propagarse. | Contradicción aparente entre VTP y aislamiento. | Switch de Áreas Comunes en **VTP Transparent** con la VLAN 54 creada localmente; justificar que Transparent reenvía anuncios sin adoptarlos ([[VTP]]). |
| 5 | Banner MOTD "en todos los switches de **distribución**": ¿incluye el Core y los de acceso? | Perder un ítem de seguridad básica. | Ponerlo en distribución **y** en el Core (no penaliza tener más). ✍️ Decidir si también en acceso. |
| 6 | "Enlace que concentra un alto volumen de tráfico" hacia servidores vs. el de I+D "mayor demanda que el resto de los troncales". | Confundir cuál es el enlace de mayor capacidad. | Servidores: EtherChannel (redundancia + capacidad). I+D: el trunk **más ancho del campus** (EtherChannel o fibra Gigabit). Justificar ambos por separado. |
| 7 | STP: PVST en Cisco IOS es realmente **PVST+**; el enunciado lo llama "PVST". | Ninguno; el comando es `spanning-tree mode pvst`. | Mencionar en el Manual que PVST+ es la implementación Cisco de PVST. |
| 8 | Alcance opcional sin puntaje declarado. | Invertir tiempo sin retorno. | Hacerlo solo si sobra tiempo tras cerrar lo obligatorio; sirve para la defensa. |
| 9 | Parte física por pareja: no dice fecha ni si se documenta en el README. | Llegar al lab sin coordinar. | Confirmar fecha de lab y pareja; incluir fotos/`show` en el README por si acaso. |
| 10 | Presupuesto "de los equipos físicos simulados" sin moneda ni fuente. | Rúbrica desconocida (ver #1). | Cotizar en USD con referencias públicas (Cisco/distribuidores), como en la Práctica 1. |

## Cómo mantener esta nota
Cuando el tutor aclare algo, reemplazá el ✍️ por la decisión y agregá una línea al [[log]]. Las decisiones cerradas se propagan a [[Requerimientos por área]] y al Manual.

Volver a [[Proyecto 1 - SmartCity Tech Park]].

> 📚 Fuente: lectura completa del PDF (11 páginas reales vs. 15 anunciadas en el índice).
