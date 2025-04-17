# 🌍 Visualizador de Starbucks y Población Mundial

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP8-brightgreen.svg)](https://www.python.org/dev/peps/pep-0008/)

[English Version](docs/README_EN.md) 🇺🇸

## 📝 Descripción

Este proyecto crea un mapa interactivo que combina dos conjuntos de datos:
- Ubicaciones globales de Starbucks
- Datos de población mundial por país

El mapa resultante permite visualizar la distribución de las tiendas Starbucks en relación con la densidad poblacional de cada país.

## ✨ Características

- 🗺️ Mapa interactivo con Folium
- 📍 Marcadores para cada ubicación de Starbucks
- 🎨 Visualización de densidad poblacional por países
- 🔍 Filtrado de ubicaciones por país
- 📊 Leyenda interactiva
- 🌈 Clasificación de países por población

## 🚀 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/ProyectoMapa.git
cd ProyectoMapa
```

2. Crea un entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 💻 Uso

1. Ejecuta el programa principal:
```bash
python src/main.py
```

2. Selecciona un país del menú
3. El mapa se generará automáticamente y se abrirá en tu navegador

## 🛠️ Tecnologías Utilizadas

- Python 3.8+
- Pandas: Procesamiento de datos
- Folium: Generación de mapas interactivos
- NumPy: Cálculos numéricos

