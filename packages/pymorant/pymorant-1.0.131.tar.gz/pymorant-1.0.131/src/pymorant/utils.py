from unidecode import unidecode
import re


def limpiar_texto(texto):

    texto_limpio = texto.replace(',', '')
    texto_limpio = unidecode(texto_limpio)
    texto_limpio = re.sub(r'[^\w\s]', '', texto_limpio)
    texto_limpio = re.sub(r'\s+', ' ', texto_limpio)
    texto_limpio = texto_limpio.strip('\'\n".,[]*- ')
    texto_limpio = texto_limpio.lower()

    return texto_limpio
