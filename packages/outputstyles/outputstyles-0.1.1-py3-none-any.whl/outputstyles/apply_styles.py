"""
Funciones para aplicar los estilos al texto.
"""

# Importar desde las variables, todos los estilos
from outputstyles.variables import all_styles


def add_text_styles(text, styles=[]):
    """
    Aplicarles los estilos al texto.

    Parameters:
    text (str): Texto al que se le van a aplicar los estilos
    styles (list): Lista de estilos que se le van a aplicar al texto

    Returns:
    srt: Devuelve el texto con los estilos aplicados
    """

    # Lista resultante de los estilos que se van a aplicar
    list_styles = []

    # Recorrer todos los estilos pasados como argumentos e ir aplicandolos
    for style in styles:
        # Tratar de asignar el estilo de turno
        try:
            # Agregar el valor del estilo a la lista resultante
            list_styles.append(all_styles[style])

        # En caso de que no exista el estilo, lo imprimimos como un error
        except KeyError:
            print(
                f'No exite el estilo: \033[1;31m{style}{all_styles["reset"]}')

    # Concatenamos los estilos separados por ";" con el texto,
    # además de agregarle "\033[" y "m" para que sea válido el código ANSI
    # Ej: \033[01;91mTexto
    text_with_styles = f'\033[{";".join(list_styles)}m{text}'

    # Retornamos el texto con los estilos aplicados, al inicio y al final de este reseteamos los estilos
    return f'{all_styles["reset"]}{text_with_styles}{all_styles["reset"]}'


def create_arg(color=None, msg_format=None):
    """
    Crear una Lista de los estilos que se le van a aplicar al texto
    en dependencia del tipo de mensaje.

    Parameters:
    color (str): Color del texto (Valor por defecto es 'None')
    msg_format (str): Formato del tipo de mensaje ('ico', 'btn', 'btn_ico')

    Returns:
    list (str): Devuelve una lista con los estilos a aplicar,
    - Si no tiene ningún color, devuelve el estilo en Negrita (bold)
    - Si no tiene formato o es de tipo icono, devuelve Negrita y el color del Texto (bold, fg_color)
    - Si es de tipo Botón o Botón con Icono, devuelve Negrita, color del Texto y del Fondo (bold, fg_color, bg_color)
    """

    # En caso de que no se especifique ningún color
    if not color:
        # Retornamos solamente el estilo en "Negrita"
        return ["bold"]

    # Si el mensaje tiene el Icono inicialmete o es solo el texto
    if msg_format == "ico" or not msg_format:
        # Retornamos el estilo en "Negrita" y el color del texto según el tipo de mensaje
        return ["bold", f'fg_{color}']

    # Si el mensaje es de tipo Botón o de Botón con icono
    elif msg_format == "btn" or msg_format == "btn_ico":
        # Retornamos el estilo en "Negrita", el color del texto en blanco y color de fondo según el tipo de mensaje
        return ["bold", f'fg_white2', f'bg_{color}']


# Función que retorna el código del Texto con los estilos aplicados según su formato
def print_message(text, msg_format=None, message_data=None):
    """
    Retornar el código del texto con los estilos aplicados, según el tipo de mensaje.

    Parameters:
    text (str): Texto al que se le van a aplicar los estilos
    msg_format (str): Formato del tipo de mensaje ('ico', 'btn', 'btn_ico')
    message_data (dic): Datos del tipo de mensaje (error_data, warning_data, success_data, info_data)

    Returns:
    srt: Devuelve el código del texto con los estilos aplicados
    """

    # Si el mensaje tiene el icono inicialmente
    if msg_format == "ico":
        # Concatenamos el texto con el icono inicialmente
        text = f'{message_data["ico_code"]} {text}'

    # Si el mensaje es de tipo botón y con el icono inicialmente
    elif msg_format == "btn_ico":
        # Concatenamos el texto con el icono inicialmente, dejando un espacio al inicio y final
        text = f' {message_data["ico_code"]} {text} '

    # Lista de los estilos que se le van a aplicar al texto, según el tipo de mensaje
    if message_data:
        # Aplicar los estilos según los datos del tipo de mensaje
        list_styles = create_arg(message_data['color'], msg_format)
    else:
        # Solo aplicar el estilo de Negrita al texto
        list_styles = create_arg()

    # Retornamos el código del texto con los estilos aplicados
    return add_text_styles(text, list_styles)
