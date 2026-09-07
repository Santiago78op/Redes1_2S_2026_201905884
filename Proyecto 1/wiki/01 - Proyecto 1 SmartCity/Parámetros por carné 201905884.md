---
tags: [redes/proyecto, proyecto1, parametros, carne]
aliases: ["parámetros", "valores por carné", "mis VLANs", "Smart_8", "VLAN 94"]
---

# Parámetros derivados del carné 201905884

Carné **2019058 8 4** → penúltimo dígito **# = 8**, último dígito **X = 4** (par).

> [!warning] Regla de oro
> Usar otros valores penaliza del **-50 % al -100 %** del proyecto (§8.1). Verificá contra esta tabla antes de cada `show vlan brief`.

## Tabla de VLANs (crear en el Server, propagar por VTP)
| Ubicación física | VLAN ID | Nombre |
|---|---|---|
| Edificio Corporativo | **14** | Gerencia |
| Centro de I+D | **24** | Investigacion |
| Planta de Producción | **34** | Produccion |
| Centro de Datos | **44** | Servidores |
| Edificio Corporativo (Áreas Comunes) | **54** | Visitantes |
| Nativa de todos los trunks | **94** | (nativa; conviene nombrarla `Nativa`) |

Sobre mayúsculas en el nombre: la tabla dice `Gerencia` y el ejemplo dice "exactamente **GERENCIA**". Decisión pendiente → [[Ambigüedades y riesgos del enunciado]].

## Resto de parámetros
| Ítem | Valor para mí | Regla del enunciado |
|---|---|---|
| Dominio VTP | `Smart_8` | `Smart_#`, # = penúltimo dígito |
| Contraseña VTP | `proyecto12S2026` | fija para todos |
| EtherChannel | **LACP** | LACP si carné par, PAgP si impar |
| STP | **PVST** (`spanning-tree mode pvst`) | PVST si par, Rapid-PVST si impar |
| Banner MOTD (solo distribución) | `Acceso Restringido - TechPark_201905884` | `Acceso Restringido - TechPark_[Carné]` |
| VLAN nativa de trunks | **94** | `9X` |
| Nombre del `.pkt` | `Proyecto1_201905884.pkt` | `Proyecto1_#carnet.pkt` |
| Manual Técnico | `Proyecto 1/README.md` | Markdown dentro de la carpeta |

Los comandos con estos valores ya sustituidos están en [[Comandos Cisco IOS del proyecto]]. Contexto general en [[Proyecto 1 - SmartCity Tech Park]].

> 📚 Fuente: enunciado §4.3 "Alcance obligatorio" y §4.5 "Entregables".
