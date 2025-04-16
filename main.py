import folium
import pandas as pd
from processing_database import procesar_datos

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
    """Genera el mapa con los datos filtrados"""
    try:
        df = pd.read_csv('filtered_starbucks.csv')
        
        # Configuración dinámica del mapa
        mapa = folium.Map(
            location=[df['Latitude'].mean(), df['Longitude'].mean()],
            zoom_start=5,
            tiles='CartoDB positron'
        )
        
        # Capa de marcadores
        for _, row in df.iterrows():
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=f"<b>{row['Store Name']}</b><br>{row['Street Address']}",
                icon=folium.Icon(color='green', icon='coffee', prefix='fa')
            ).add_to(mapa)
        
        # Guardar y mostrar
        mapa.save('map.html')
        print("\nMapa generado exitosamente. Abriendo en navegador...")
        mapa.show_in_browser()
        
    except FileNotFoundError:
        print("Error: Primero debe seleccionar un país (Opción 1)")
    except pd.errors.EmptyDataError:
        print("Error: No hay datos para mostrar con los filtros actuales")

if __name__ == "__main__":
    menu_principal()



