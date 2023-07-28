from unidecode import unidecode
import re

def generateSLUG(_name):
    slug = str(_name)
    slug = unidecode(slug) #Convertir texto Unicode en ASCII para quitar tildes y eñes
    slug = re.sub(r'[^\w\s]', '', slug) #Elimino todos los caracteres no alfanumericos
    slug = slug.lower() #Convetir a minusculas  
    slug = re.sub(r"\s+", '-',slug) #Sustituir un espacio o una secuencias de espacio por un guion
    return  slug