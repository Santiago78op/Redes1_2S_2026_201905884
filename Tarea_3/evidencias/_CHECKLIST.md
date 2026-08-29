# Checklist de capturas

Guardá cada captura en esta carpeta con el nombre EXACTO de la izquierda.
Si respetás los nombres, las imágenes aparecen solas en `Manual_Tecnico.md`.

| # | Archivo | Qué capturar | Dónde |
|---|---|---|---|
| 1 | `01-topologia.png` | Los 10 dispositivos renombrados, enlaces en verde | Área de trabajo de PT |
| 2 | `02-trunks-switch0.png` | `show interfaces trunk` | CLI de `Switch0` |
| 3 | `03-ip-pc1.png` | Ventana IP Configuration | `PC1` → Desktop → IP Configuration |
| 4 | `04-vtp-status-switch0.png` | `show vtp status` | CLI de `Switch0` |
| 5 | `05-vtp-status-admin.png` | `show vtp status` | CLI de `ADMIN` |
| 6 | `06-vtp-status-merca.png` | `show vtp status` | CLI de `MERCA` |
| 7 | `07-vtp-status-ventas.png` | `show vtp status` | CLI de `VENTAS` |
| 8 | `08-vlan-brief-switch0.png` | `show vlan brief` | CLI de `Switch0` |
| 9 | `09-vlan-brief-admin.png` | `show vlan brief` | CLI de `ADMIN` |
| 10 | `10-vlan-brief-merca.png` | `show vlan brief` | CLI de `MERCA` |
| 11 | `11-vlan-brief-ventas.png` | `show vlan brief` | CLI de `VENTAS` |
| 12 | `12-ping-ok-vlan10.png` | `ping 192.168.10.60` con reply | `PC1` → Desktop → Command Prompt |
| 13 | `13-ping-ok-vlan20.png` | `ping 192.168.20.30` con reply | `PC2` → Command Prompt |
| 14 | `14-ping-ok-vlan30.png` | `ping 192.168.30.50` con reply | `PC4` → Command Prompt |
| 15 | `15-ping-fail-mismo-switch.png` | `ping 192.168.20.20` con 100% loss | `PC1` → Command Prompt |
| 16 | `16-ping-fail-distinto-switch.png` | `ping 192.168.20.30` con 100% loss | `PC1` → Command Prompt |
| 17 | `17-ping-fail-misma-subred.png` | *(opcional)* `ping 192.168.10.99` con 100% loss | `PC1` → Command Prompt |

**Tip:** en macOS, `Cmd + Shift + 4` y luego barra espaciadora captura una ventana completa;
sin la barra espaciadora capturás el área que arrastres. Recortá para que se lea el texto.

Antes de entregar: borrá este archivo si no querés que aparezca en el repo.
