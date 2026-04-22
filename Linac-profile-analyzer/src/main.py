"""
Punto de entrada de la aplicación.

Ejecute este archivo con:

    python src/main.py
"""

from gui import AnalizadorPerfilApp


def main() -> None:
    app = AnalizadorPerfilApp()
    app.ejecutar()


if __name__ == "__main__":
    main()
