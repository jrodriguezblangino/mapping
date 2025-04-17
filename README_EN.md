# 🌍 Starbucks and World Population Visualizer

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP8-brightgreen.svg)](https://www.python.org/dev/peps/pep-0008/)

[Spanish Version](../README.md) 🇪🇸

## 📝 Description

This project creates an interactive map that combines two datasets:
- Global Starbucks locations
- World population data by country

The resulting map allows you to visualize the distribution of Starbucks stores in relation to the population density of each country.

## ✨ Features

- 🗺️ Interactive map with Folium
- 📍 Markers for each Starbucks location
- 🎨 Population density visualization by country
- 🔍 Location filtering by country
- 📊 Interactive legend
- 🌈 Country classification by population

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/MapProject.git
cd MapProject
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

1. Run the main program:
```bash
python src/main.py
```

2. Select a country from the menu
3. The map will be automatically generated and opened in your browser

## 🛠️ Technologies Used

- Python 3.8+
- Pandas: Data processing
- Folium: Interactive map generation
- NumPy: Numerical calculations

## 📁 Project Structure

```
MapProject/
├── src/ # Source code
├── data/ # Data files
├── docs/ # Documentation
├── tests/ # Unit tests
└── requirements.txt # Dependencies
```