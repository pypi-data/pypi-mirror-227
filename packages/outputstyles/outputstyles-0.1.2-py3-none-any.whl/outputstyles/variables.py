"""
Variables con todos los Estilos que se le pueden aplicar a los textos
y los datos de los diferentes tipos de mensajes
"""

all_styles = {
    # Formatos
    'reset': '\033[0m',
    'bold': '01',
    'disabled': '02',
    'italic': '03',
    'underline': '04',
    'blink': '05',
    'blink2': '06',
    'reverse': '07',
    'invisible': '08',
    'strike_through': '09',

    # Colores del Texto
    'fg_black': '30',
    'fg_red': '31',
    'fg_green': '32',
    'fg_yellow': '33',
    'fg_blue': '34',
    'fg_magenta': '35',
    'fg_cyan': '36',
    'fg_white': '37',
    'fg_black2': '90',
    'fg_red2': '91',
    'fg_green2': '92',
    'fg_yellow2': '93',
    'fg_blue2': '94',
    'fg_magenta2': '95',
    'fg_cyan2': '96',
    'fg_white2': '97',

    # Colores del Fondo
    'bg_black': '40',
    'bg_red': '41',
    'bg_green': '42',
    'bg_yellow': '43',
    'bg_blue': '44',
    'bg_magenta': '45',
    'bg_cyan': '46',
    'bg_white': '47',
    'bg_black2': '100',
    'bg_red2': '101',
    'bg_green2': '102',
    'bg_yellow2': '103',
    'bg_blue2': '104',
    'bg_magenta2': '105',
    'bg_cyan2': '106',
    'bg_white2': '107',
}
"""
Contiene todos los estilos que se le pueden aplicar a los textos:
- Formato (Bold, Underline, etc)
- Color del Texto (Red, Black, Green, etc)
- Color del Fondo (Red, Black, Green, etc)
"""


error_data = {
    "ico_code": "\u2718",
    "color": "red"
}
"""
Datos del Mensaje de tipo 'Error'
- Icono: \u2718
- Color: Red
"""


warning_data = {
    "ico_code": "\u26A0",
    "color": "yellow"
}
"""
Datos del Mensaje de tipo 'Warning'
- Icono: \u26A0
- Color: Yellow
"""


success_data = {
    "ico_code": "\u2714",
    "color": "green"
}
"""
Datos del Mensaje de tipo 'Success'
- Icono: \u2714
- Color: Green
"""


info_data = {
    "ico_code": "\u24D8",
    "color": "blue"
}
"""
Datos del Mensaje de tipo 'Info'
- Icono: \u24D8
- Color: Blue
"""
