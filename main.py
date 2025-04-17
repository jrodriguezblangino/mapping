import os
import folium
import pandas as pd
from processing_database import procesar_datos
import tempfile
from folium.plugins import FeatureGroupSubGroup
from folium import LayerControl

def menu_principal():
    """Muestra el menú principal del programa"""
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

def generar_mapa():
    """Genera y muestra el mapa con datos temporales"""
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
                tiles='CartoDB positron'
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



