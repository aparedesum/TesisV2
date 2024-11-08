import re
import torch

print(f"AVAILABLE -> {torch.cuda.is_available()}")

def obtener_tokens(oracion):
    resultado = []

    oracion_split = oracion.strip().split(" ")
    n = len(oracion_split)
    print(n)
    
    i = 0
    while i < n:
        elemento = oracion_split[i].strip()
        if elemento.startswith("#"):
            if elemento.endswith("#"):
                resultado.append(elemento)
                i = i + 1
            else:
                j = i + 1
                tmp = elemento
                while j < n and not oracion_split[j].endswith("#"):
                    tmp = f"{tmp} {oracion_split[j].strip()}"
                    j = j + 1
                tmp = f"{tmp} {oracion_split[j].strip()}"
                i = j + 1
                resultado.append(tmp) 
        else:
            tmp = elemento
            j = i + 1
            while j < n and not oracion_split[j].startswith("#"):
                tmp = f"{tmp} {oracion_split[j].strip()}"
                j = j + 1
            i = j
            resultado.append(tmp) 
    return resultado

# Ejemplo de uso
oracion = "#2474#observar# #7029#la# situación #3047#y# #7141#leer#past# #8476#el# #37340#texto#plural#"
oracion = "tipo  #7074#de#  #37340#texto#"
resultado = obtener_tokens(oracion)
print(resultado)
 

