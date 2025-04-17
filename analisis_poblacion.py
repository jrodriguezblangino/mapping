import json
import pandas as pd
import folium
from folium.plugins import FeatureGroupSubGroup
from folium import LayerControl  # Folium >= 0.14.0
from typing import Tuple, Dict, List
import numpy as np

def cargar_datos_geograficos(ruta_archivo: str) -> pd.DataFrame:
    """Carga y procesa datos geográficos desde un archivo GeoJSON.
    
    Args:
        ruta_archivo: Ruta al archivo GeoJSON con los datos
        
    Returns:
        DataFrame con datos de países y población
    """
    with open(ruta_archivo, 'r', encoding='utf-8-sig') as f:
        datos = json.load(f)
    
    features = datos['features']
    datos_normalizados = []
    
    for feature in features:
        props = feature['properties']
        datos_normalizados.append({
            'pais': props['NAME'],
            'codigo_pais': props['ISO3'],
            'poblacion_2005': props['POP2005'],
            'geometria': feature['geometry']
        })
    
    return pd.DataFrame(datos_normalizados)

def clasificar_poblacion(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Tuple[int, int]]]:
    """Clasifica países usando rangos fijos de población."""
    df = df[df['poblacion_2005'] > 0].copy()
    
    # Definir rangos fijos
    rangos = {
        'baja': (0, 10_000_000),
        'media': (10_000_000, 40_000_000),
        'alta': (40_000_000, df['poblacion_2005'].max())
    }
    
    # Asignar categorías
    condiciones = [
        df['poblacion_2005'] <= rangos['baja'][1],
        df['poblacion_2005'] <= rangos['media'][1],
        df['poblacion_2005'] > rangos['media'][1]
    ]
    
    categorias = ['baja', 'media', 'alta']
    colores = {
        'baja': '#2ca25f',  # Verde
        'media': '#ff7f00',  # Naranja
        'alta': '#e41a1c'    # Rojo
    }
    
    df['categoria_poblacion'] = np.select(condiciones, categorias, default='baja')
    df['color'] = df['categoria_poblacion'].map(colores)
    
    return df, rangos

def estilo_poblacion(feature: Dict) -> Dict:
    """Función de estilo para colorear países según población."""
    return {
        'fillColor': feature['properties']['color'],
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.5
    }

def crear_capa_poblacion(ruta_geojson: str) -> folium.FeatureGroup:
    """Crea una capa de Folium con la densidad poblacional"""
    df = cargar_datos_geograficos(ruta_geojson)
    df_clasificado, _ = clasificar_poblacion(df)
    
    fg = folium.FeatureGroup(name='Densidad Poblacional', show=True)
    
    for _, row in df_clasificado.iterrows():
        folium.GeoJson(
            data=row['geometria'],
            name=row['pais'],
            style_function=lambda x, color=row['color']: {
                'fillColor': color,
                'color': 'black',
                'weight': 0.5,
                'fillOpacity': 0.5
            },
            tooltip=f"Población: {row['poblacion_2005']:,}"
        ).add_to(fg)
    
    return fg

def analizar_y_visualizar_poblacion(ruta_geojson: str) -> None:
    """Flujo completo de análisis y visualización."""
    df = cargar_datos_geograficos(ruta_geojson)
    df_clasificado, rangos = clasificar_poblacion(df)
    
    print("\nClasificación por rangos fijos:")
    print(f"Baja población: ≤ {rangos['baja'][1]:,} habitantes")
    print(f"Media población: {rangos['media'][0]:,} - {rangos['media'][1]:,}")
    print(f"Alta población: > {rangos['alta'][0]:,}")
    
    # Estadísticas de distribución
    conteo = df_clasificado['categoria_poblacion'].value_counts()
    print("\nDistribución de países:")
    print(f"Verdes: {conteo.get('baja', 0)} países")
    print(f"Naranjas: {conteo.get('media', 0)} países")
    print(f"Rojos: {conteo.get('alta', 0)} países")
    
    mapa = crear_capa_poblacion(ruta_geojson)
    folium.LayerControl(collapsed=False).add_to(mapa)
    mapa.save('mapa_poblacion.html')
    return mapa
