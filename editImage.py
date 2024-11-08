from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import os

def add_arrow_based_on_filename(linea):
    valores = [elem for elem in linea.split('#') if elem]
    id = valores[0] 
    image_path = f"imagenes_arasaac/{id}.png"
    image = Image.open(image_path)

    if (len(valores) == 1):
        image.save(f"imagenes_procesadas/{id}.png")
        return

    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    overlay = Image.new('RGBA', image.size)
    draw = ImageDraw.Draw(overlay)

    tipo = valores[1]
    
    # Coordenadas de las flechas dependiendo del nombre del archivo
    if 'past' in tipo:
        start = (80, 60)
        end = (20, 60)
        draw.line([start, end], fill="black", width=4)
        draw.polygon([(end[0]-5, end[1]), (end[0]+10, end[1]-10), (end[0]+10, end[1]+10)], fill="black")
    elif 'future' in tipo:
        start = (image.width - 80, 60)
        end = (image.width - 20, 60)
        draw.line([start, end], fill="black", width=4)
        draw.polygon([(end[0]+5, end[1]), (end[0]-10, end[1]-10), (end[0]-10, end[1]+10)], fill="black")
    elif 'plural' in tipo:
        center_x = image.width - 50
        center_y = 40  # 10 puntos por encima de la imagen
        offset = 20
        draw.line([(center_x - offset, center_y), (center_x + offset, center_y)], fill="black", width=5)
        draw.line([(center_x, center_y - offset), (center_x, center_y + offset)], fill="black", width=5)
    
    combined = Image.alpha_composite(image, overlay)

    # Guardar la imagen con flechas
    combined.save(f"imagenes_procesadas/{id}_{tipo}.png")


#image_paths = '#2690#'
#dd_arrow_based_on_filename(image_paths)


with open("ids_arasaac.txt", 'r', encoding='utf-8') as archivo:
    lineas = archivo.readlines()
    for linea in lineas:
        try:
            add_arrow_based_on_filename(linea.strip())
        except Exception as e:
            print(f"Error al procesar el archivo {linea}: {e}")
