# QGIS Urban Infrastructure Colombia 🏙️

> Plugin QGIS y scripts Python para análisis de redes de servicios, visualización de infraestructura urbana y gestión de activos viales en municipios colombianos.

[![QGIS](https://img.shields.io/badge/QGIS-3.16+-green)](https://qgis.org)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Colombia](https://img.shields.io/badge/País-Colombia-red)]()

## ¿Qué hace este proyecto?

Herramientas open source para ingenieros civiles del sector público colombiano que gestionan infraestructura crítica urbana: redes de acueducto, alcantarillado, energía, telecomunicaciones y malla vial municipal.

**Impacto directo:** Los municipios colombianos gestionan infraestructura que sirve a más de 30 millones de habitantes en zonas urbanas. Este plugin reduce el tiempo de análisis de redes de horas a minutos y estandariza la gestión de activos viales bajo el esquema INVIAS.

## Herramientas incluidas

| Módulo | Descripción |
|--------|-------------|
| **Análisis de Redes** | Calcula longitud, completitud de datos y tramos críticos por tipo de red (acueducto, alcantarillado, energía, vías) |
| **Visualización Estándar** | Aplica simbología automática por tipo de infraestructura con paleta de colores institucional |
| **Gestión de Activos Viales** | Crea capas con esquema estándar INVIAS: PCI, IRI, costos de mantenimiento, historial |

## Instalación del Plugin QGIS

1. Descarga o clona este repositorio
2. Copia la carpeta `urban_infra_plugin/` a tu directorio de plugins de QGIS:
   - Windows: `C:\Users\{usuario}\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - Linux/Mac: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
3. En QGIS: `Complementos → Administrar e instalar complementos → Instalados`
4. Activa **Urban Infrastructure Colombia**

## Uso de los Scripts Python

```bash
