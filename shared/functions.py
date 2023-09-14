"""Funciones comptartidas"""
import re
from html import unescape

def decode_html_script(script_element) -> str | None:
    """
    Decodificar los textos que se generan a partir de <script></script>
    en las tablas.

    Args:
        script_element: elemento de la tabla que contiene el script tbody->td->tr->script

    Returns:
        str | None: String si consigue decodificar el valor, None si no.
    """
    # Utiliza una expresión regular para extraer el valor codificado
    match = re.search(r'decodificar\("([^"]+)"\)', script_element)

    if match:
        # Obtiene el valor numérico del grupo coincidente
        encoded_value = match.group(1)

        # Decodifica el valor utilizando la función decodificar
        decoded_value = unescape(encoded_value)

        return decoded_value
    else:
        return None
