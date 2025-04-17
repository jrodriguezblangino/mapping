from paises import PAISES_ISO
import pandas as pd
import tempfile

def cargar_datos():
    """Carga y limpia los datos originales"""
    df = pd.read_csv('directory.csv')
    
    # Limpieza básica
    df = df.dropna(subset=['Latitude', 'Longitude'])
    df = df.drop_duplicates(subset=['Store Number'])
    
    return df

def mostrar_paises_disponibles(df):
    """Muestra países con nombres completos y códigos"""
    codigos_paises = sorted(df['Country'].unique())
    
    print("\nPaíses disponibles con locales Starbucks:")
    for i, codigo in enumerate(codigos_paises, 1):
        nombre = PAISES_ISO.get(codigo, f'Código desconocido ({codigo})')
        print(f"{i}. {nombre} ({codigo})")
    
    return codigos_paises

def seleccionar_pais(codigos_paises):
    """Interfaz mejorada para selección de país"""
    while True:
        try:
            seleccion = int(input("\nIngrese el número del país a visualizar: "))
            if 1 <= seleccion <= len(codigos_paises):
                return codigos_paises[seleccion-1]
            print(f"Error: Ingrese un número entre 1 y {len(codigos_paises)}")
        except ValueError:
            print("Error: Debe ingresar un número válido")

def guardar_filtrado(df_filtrado):
    """Guarda el dataframe filtrado temporalmente"""
    df_filtrado.to_csv('filtered_starbucks.csv', index=False)
    print(f"\nBase temporal creada con {len(df_filtrado)} locales.")

def procesar_datos():
    """Flujo principal de procesamiento de datos"""
    print("\n=== PROCESAMIENTO DE DATOS ===")
    df = cargar_datos()
    codigos = mostrar_paises_disponibles(df)
    pais = seleccionar_pais(codigos)
    df_filtrado = df[df['Country'] == pais]
    guardar_filtrado(df_filtrado)
    print("\nDatos procesados correctamente. Generando mapa...")
