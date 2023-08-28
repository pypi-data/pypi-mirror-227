"""
Imprimir los diferentes tipos de mensajes
"""

# Importar desde las variables, los datos de los diferentes tipos de mensajes
from outputstyles.variables import error_data, info_data, success_data, warning_data

# Importar desde las apply_styles, la función que devuelve el texto con los estilos aplicados
from outputstyles.apply_styles import print_message


def error(text, msg_format=None, message_data=error_data):
    """
    Mensaje de tipo de Error

    Parameters:
    text (str): Texto al que se le van a aplicar los estilos
    msg_format (str): Formato del tipo de mensaje ('ico', 'btn', 'btn_ico')
    message_data (dic): Datos del tipo de mensaje (error_data)

    Returns:
    srt: Devuelve el texto con los estilos aplicados
    """
    return print_message(text, msg_format, message_data)


def warning(text, msg_format=None, message_data=warning_data):
    """
    Mensaje de tipo de Warning

    Parameters:
    text (str): Texto al que se le van a aplicar los estilos
    msg_format (str): Formato del tipo de mensaje ('ico', 'btn', 'btn_ico')
    message_data (dic): Datos del tipo de mensaje (warning_data)

    Returns:
    srt: Devuelve el texto con los estilos aplicados
    """
    return print_message(text, msg_format, message_data)


def success(text, msg_format=None, message_data=success_data):
    """
    Mensaje de tipo de Success

    Parameters:
    text (str): Texto al que se le van a aplicar los estilos
    msg_format (str): Formato del tipo de mensaje ('ico', 'btn', 'btn_ico')
    message_data (dic): Datos del tipo de mensaje (success_data)

    Returns:
    srt: Devuelve el texto con los estilos aplicados
    """

    return print_message(text, msg_format, message_data)


# Función de  (Recibe el Texto, el formato y se le pasa las propiedades del tipo de mensaje por default)
def info(text, msg_format=None, message_data=info_data):
    """
    Mensaje de tipo de Info

    Parameters:
    text (str): Texto al que se le van a aplicar los estilos
    msg_format (str): Formato del tipo de mensaje ('ico', 'btn', 'btn_ico')
    message_data (dic): Datos del tipo de mensaje (info_data)

    Returns:
    srt: Devuelve el texto con los estilos aplicados
    """

    return print_message(text, msg_format, message_data)


# Función de Bold (Recibe solamente el Texto)
def bold(text):
    """
    Mensaje de tipo de Bold

    Parameters:
    text (str): Texto que se va a poner en Negrita

    Returns:
    srt: Devuelve el texto en Negrita
    """
    return print_message(text)
