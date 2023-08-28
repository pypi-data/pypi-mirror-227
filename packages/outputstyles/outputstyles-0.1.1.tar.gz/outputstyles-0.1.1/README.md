# Output Styles

Aplicarle estilos a la salida por CLI.

## Install

```bash
  pip install outputstyles
```

## Usage/Examples

```py
from outputstyles.msg_print import error, warning, info, success, bold

# Imprimir los diferentes tipos de mensajes
print(error("Error!"))
print(error("Error!", "btn"))
print(error("Error!", "ico"))
print(error("Error!", "btn_ico"))
print("")

print(warning("Warning!"))
print(warning("Warning!", "ico"))
print(warning("Warning!", "btn"))
print(warning("Warning!", "btn_ico"))
print("")

print(success("Success!"))
print(success("Success!", "btn"))
print(success("Success!", "ico"))
print(success("Success!", "btn_ico"))
print("")

print(info("Info!"))
print(info("Info!", "btn"))
print(info("Info!", "ico"))
print(info("Info!", "btn_ico"))
print("")

print(bold("Bold!"))

```

## Screenshots

![output_styles](docs/img/output_styles.png)

## License

[MIT](LICENSE)

## Authors

- [@dunieskysp](https://github.com/dunieskysp)
