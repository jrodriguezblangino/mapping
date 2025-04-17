import os
import folium
import pandas as pd
from processing_database import procesar_datos
import tempfile

def menu_principal():
    """Muestra el menú principal del programa"""
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Seleccionar país y generar mapa")
        print("2. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == '1':
            procesar_datos()  # Ejecuta el procesamiento
            generar_mapa()    # Genera el mapa automáticamente
        elif opcion == '2':
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

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
            
            # Generar mapa
            mapa = folium.Map(
                location=[df['Latitude'].mean(), df['Longitude'].mean()],
                zoom_start=5,
                tiles='CartoDB positron'
            )
            
            for _, row in df.iterrows():
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=f"<b>{row['Store Name']}</b><br>{row['Street Address']}",
                    icon=folium.Icon(color='green', icon='coffee', prefix='fa')
                ).add_to(mapa)
            
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



