import json

# Función para leer el archivo JSON y extraer la clave 'traduccion'
def extract_traduccion(json_file, output_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        traducciones = []

        for item in data:
            if 'oracion' in item:
                traducciones.append(item['oracion'])
        
        with open(output_file, 'w', encoding='utf-8') as file:
            for traduccion in traducciones:
                file.write(traduccion + '\n')
        
        print(f"Las traducciones se han guardado en {output_file}")
    
    except FileNotFoundError:
        print(f"El archivo {json_file} no se encontró.")
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Especificar el archivo JSON de entrada y el archivo de texto de salida
json_file = 'test_data.json'
output_file = 'test_oraciones.txt'


def ordenar_oraciones_por_longitud(archivo_entrada, archivo_salida):
    # Leer todas las líneas del archivo de entrada
    with open(archivo_entrada, 'r', encoding='utf-8') as file:
        oraciones = file.readlines()
    
    # Eliminar espacios en blanco al inicio y final de cada oración
    oraciones = [oracion.strip() for oracion in oraciones]
    
    # Ordenar las oraciones por longitud
    oraciones_ordenadas = sorted(oraciones, key=len)
    
    # Escribir las oraciones ordenadas en el archivo de salida
    with open(archivo_salida, 'w', encoding='utf-8') as file:
        for oracion in oraciones_ordenadas:
            file.write(oracion + '\n')

# Uso del programa
archivo_entrada = 'validacion_oraciones.txt'  # Nombre del archivo de entrada
archivo_salida  = 'validacion_ordenadas.txt'  # Nombre del archivo de salida

#extract_traduccion(json_file, output_file)
ordenar_oraciones_por_longitud(archivo_entrada, archivo_salida)

print(f"Las oraciones han sido ordenadas y guardadas en '{archivo_salida}'.")
