# -*- coding: utf-8 -*-
from unidecode import unidecode
import re

def generateSLUG(_text):
    """Method in charge of transforming a sequence of characters into a string 
    of type slug (without characters that are not alphanumeric and belong to 
    the English alphabet, the space or sequences of these is replaced by a 
    hyphen (-))

    Args:
        _text (str): Character string to be converted to a slug.

    Returns:
        str: Character string of type slug a generated from the one received by
        parameters.
    """
    slug = str(_text)
    slug = unidecode(slug)
    slug = re.sub(r'[^\w\s]', '', slug) 
    slug = slug.lower()  
    slug = re.sub(r"\s+", '-',slug)
    return  slug