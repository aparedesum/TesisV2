import json
import warnings
import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

warnings.filterwarnings('ignore')

def cargar_pictogramas():
    nombre_archivo = 'pictogramasArasaac.json'
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo_json:
            # Carga el contenido del archivo JSON en un diccionario
            datos_dict = json.load(archivo_json)
            lista_pictogramas_ids = []
            set_existente = set()
            dataset_basico = []
            for element in datos_dict:
                id = element.get('_id')
                keywords = element.get('keywords', [])
                j = 100000
                #lista_pictogramas_ids.append(f"#{id}#")
                for keyword in keywords:
                    palabra = keyword.get("keyword")
                    
                    if keyword.get("plural"):
                        key_plural = f"#{id}#{palabra}#plural#"
                        key_singular = f"#{id}#{palabra}#"
                        if key_plural not in set_existente:
                            set_existente.add(key_plural)
                            lista_pictogramas_ids.append(key_singular)
                            lista_pictogramas_ids.append(key_plural)
                            dataset_basico.append({"id": j, "oracion" : palabra , "traduccion": key_singular})
                            j = j + 1
                            dataset_basico.append({"id": j, "oracion" : keyword.get("plural") , "traduccion": key_plural})
                            j = j + 1
                    elif keyword.get("type") == 3:
                        key = f"#{id}#{palabra}"
                        if f"{key}#past#" not in set_existente:
                            set_existente.add(f"{key}#past#")
                            lista_pictogramas_ids.append(f"{key}#")
                            dataset_basico.append({"id": j, "oracion" : palabra , "traduccion": key})
                            j = j + 1
                            lista_pictogramas_ids.append(f"{key}#pasado#")
                            lista_pictogramas_ids.append(f"{key}#futuro#")
                    else:
                        lista_pictogramas_ids.append(f"#{id}#{palabra}#")                  
            
            with open("ids_arasaac.txt", 'w', encoding='utf-8') as archivo:
                for ids in lista_pictogramas_ids:
                    archivo.write(ids + '\n')

            dataset_basico_json = json.dumps(dataset_basico,ensure_ascii=False,indent=2)

            with open('traduccion_pictogramas_arasaac.json', 'w', encoding='utf-8') as file:
                file.write(dataset_basico_json)

        return lista_pictogramas_ids
    except FileNotFoundError:
        print(f'El archivo {nombre_archivo} no se encuentra.')
    except json.JSONDecodeError as e:
        print(f'Error al decodificar el archivo JSON: {e}')
    except Exception as e:
        print(f'Error durante la carga del archivo JSON: {e}')


def download_image(picto_id, download_directory):
    

    url = f'https://api.arasaac.org/api/pictograms/{picto_id}?download=false'
    response = requests.get(url)
    if response.status_code == 200:
        image_path = os.path.join(download_directory, f'{picto_id}.png')
        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f'Imagen {picto_id} descargada con éxito.')
    else:
        print(f'Error al descargar la imagen {picto_id}. Status code: {response.status_code}')

def download_images(ids, download_directory, max_workers=10):
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_image_with_delay, picto_id, download_directory): picto_id for picto_id in ids}
        for future in as_completed(futures):
            try:
                print(future.result())
            except Exception as e:
                print(f'Error: {e}')

def download_image_with_delay(picto_id, download_directory):
    result = download_image(picto_id, download_directory)
    time.sleep(1)  # Delay de 1 segundo entre solicitudes
    return result

def download_ids():
    nombre_archivo = 'pictogramasArasaac.json'
    ids = []
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo_json:
            datos_dict = json.load(archivo_json)
            for element in datos_dict:
                ids.append(element.get('_id'))
    except Exception as e:
        print(f'Error: {e}')
    return ids

   
lista_pictogramas_ids=cargar_pictogramas()

##Descomentar para descargar imagenes
#download_images(download_ids(), "imagenes_arasaac")
print(len(lista_pictogramas_ids))