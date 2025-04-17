import os
import folium
import pandas as pd
from processing_database import procesar_datos
import tempfile
from folium.plugins import FeatureGroupSubGroup
from folium import LayerControl
from branca.element import Element, MacroElement
from jinja2 import Template
from typing import NoReturn

def menu_principal() -> NoReturn:
    """
    Controla el flujo principal de la aplicación mediante un menú interactivo.
    
    Muestra opciones para generar el mapa o salir del programa, manejando
    las entradas del usuario y ejecutando las funciones correspondientes.
    
    Ejemplo:
        >>> menu_principal()
        === MENÚ PRINCIPAL ===
        1. Seleccionar país y generar mapa
        2. Salir
    """
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Seleccionar país y generar mapa")
        print("2. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == '1':
            procesar_datos()
            generar_mapa()
        elif opcion == '2':
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida, intente nuevamente")

def generar_mapa() -> None:
    """
    Genera un mapa interactivo combinando datos de Starbucks y población.
    
    Proceso:
    1. Crea archivos temporales para el procesamiento
    2. Configura el mapa base con límites y controles de zoom
    3. Añade capas de Starbucks y densidad poblacional
    4. Incluye leyenda interactiva y controles de capas
    5. Guarda y muestra el resultado en el navegador
    
    Maneja excepciones y limpia archivos temporales al finalizar.
    """
    try:
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp_csv:
            temp_csv_name = tmp_csv.name
            temp_html_name = temp_csv_name.replace('.csv', '.html')
            
            # Procesar y guardar datos en temporal
            df = pd.read_csv('filtered_starbucks.csv')
            df.to_csv(temp_csv_name, index=False)
            
            # Crear mapa base
            mapa = folium.Map(
                location=[df['Latitude'].mean(), df['Longitude'].mean()],
                zoom_start=5,
                tiles='CartoDB positron',
                min_zoom=2,  # Zoom mínimo global
                max_zoom=18,  # Zoom máximo
                max_bounds=True,  # Limitar movimiento del mapa
                bounds=[[-90, -180], [90, 180]]  # Límites del mapa
            )
            
            # Capa de Starbucks
            fg_starbucks = folium.FeatureGroup(name='Locales Starbucks', show=True)
            for _, row in df.iterrows():
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=f"<b>{row['Store Name']}</b><br>{row['Street Address']}",
                    icon=folium.Icon(color='green', icon='coffee', prefix='fa')
                ).add_to(fg_starbucks)
            
            # Capa de población (siempre presente)
            from analisis_poblacion import crear_capa_poblacion
            fg_poblacion = crear_capa_poblacion('world.json')
            fg_poblacion.show = True  # Visible por defecto
            
            # Añadir todas las capas
            fg_starbucks.add_to(mapa)
            fg_poblacion.add_to(mapa)
            
            # Control de capas
            LayerControl(collapsed=False).add_to(mapa)
            
            # Añadir leyenda de población
            class Leyenda(MacroElement):
                def __init__(self, colores, etiquetas):
                    super().__init__()
                    self._name = 'Leyenda'
                    self.colores = colores
                    self.etiquetas = etiquetas

                def render(self, **kwargs):
                    self._parent.get_root().header.add_child(
                        folium.Element(
                            f"""
                            <div id='leyenda' style='
                                position: absolute;
                                bottom: 30px;
                                left: 30px;
                                z-index: 9999;
                                background-color: white;
                                padding: 15px;
                                border: 1px solid #cccccc;
                                border-radius: 8px;
                                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                                font-family: "Segoe UI", Arial, sans-serif;
                                font-size: 14px;
                                color: #333333;
                                line-height: 1.5;
                            '>
                                <strong style='
                                    display: block;
                                    font-size: 16px;
                                    margin-bottom: 10px;
                                    color: #2c3e50;
                                    border-bottom: 1px solid #eee;
                                    padding-bottom: 5px;
                                '>Densidad Poblacional</strong>
                                
                                <div style='display: flex; align-items: center; margin: 8px 0;'>
                                    <div style='
                                        width: 24px;
                                        height: 24px;
                                        background: {self.colores['alta']};
                                        border: 1px solid #ffffff;
                                        border-radius: 3px;
                                        margin-right: 10px;
                                    '></div>
                                    <span>{self.etiquetas['alta']}</span>
                                </div>
                                
                                <div style='display: flex; align-items: center; margin: 8px 0;'>
                                    <div style='
                                        width: 24px;
                                        height: 24px;
                                        background: {self.colores['media']};
                                        border: 1px solid #ffffff;
                                        border-radius: 3px;
                                        margin-right: 10px;
                                    '></div>
                                    <span>{self.etiquetas['media']}</span>
                                </div>
                                
                                <div style='display: flex; align-items: center; margin: 8px 0;'>
                                    <div style='
                                        width: 24px;
                                        height: 24px;
                                        background: {self.colores['baja']};
                                        border: 1px solid #ffffff;
                                        border-radius: 3px;
                                        margin-right: 10px;
                                    '></div>
                                    <span>{self.etiquetas['baja']}</span>
                                </div>
                            </div>
                            """
                        )
                    )

            # Definir colores y etiquetas
            leyenda = Leyenda(
                colores={
                    'baja': '#2ca25f',
                    'media': '#ff7f00',
                    'alta': '#e41a1c'
                },
                etiquetas={
                    'baja': 'Baja (<10M)',
                    'media': 'Media (10M-40M)',
                    'alta': 'Alta (>40M)'
                }
            )
            mapa.add_child(leyenda)
            
            mapa.save(temp_html_name)
            print("\nMapa generado exitosamente. Abriendo en navegador...")
            mapa.show_in_browser()
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Limpieza de archivos temporales
        if os.path.exists(temp_csv_name):
            os.remove(temp_csv_name)
        if os.path.exists(temp_html_name):
            os.remove(temp_html_name)
        # Eliminar el archivo filtered original si existe
        if os.path.exists('filtered_starbucks.csv'):
            os.remove('filtered_starbucks.csv')

if __name__ == "__main__":
    menu_principal()



