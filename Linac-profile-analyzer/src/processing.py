"""
Funciones de lectura, limpieza y preparación de datos para perfiles de dosis.
"""

from __future__ import annotations

from io import StringIO
from typing import Optional

import pandas as pd

from metrics import DEFAULT_DOSE_COLUMN, DEFAULT_PROFILE_COLUMN


def leer_archivo_perfil(
    file_path: str,
    perfil_col: str = DEFAULT_PROFILE_COLUMN,
    dosis_col: str = DEFAULT_DOSE_COLUMN,
) -> pd.DataFrame:
    """
    Lee un archivo de perfil con al menos dos columnas numéricas.

    Se conserva el comportamiento del script original:
    - reemplaza comas decimales por puntos.
    - usa separación por espacios en blanco.
    - toma únicamente las dos primeras columnas.
    - convierte datos no numéricos a NaN y elimina filas inválidas.
    - si el rango del perfil es mayor que 50, asume que estaba en mm y convierte a cm.
    """
    with open(file_path, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().replace(",", ".")

    datos = pd.read_csv(StringIO(contenido), sep=r"\s+", header=None)
    datos = datos.iloc[:, :2]
    datos.columns = [perfil_col, dosis_col]

    datos[perfil_col] = pd.to_numeric(datos[perfil_col], errors="coerce")
    datos[dosis_col] = pd.to_numeric(datos[dosis_col], errors="coerce")

    datos = datos.dropna(subset=[perfil_col, dosis_col]).reset_index(drop=True)

    rango = datos[perfil_col].max() - datos[perfil_col].min()
    if rango > 50:
        datos[perfil_col] = datos[perfil_col] / 10.0

    return datos


def recortar_por_tamano_campo(
    datos: pd.DataFrame,
    campo_size: Optional[float],
    perfil_col: str = DEFAULT_PROFILE_COLUMN,
) -> pd.DataFrame:
    """
    Recorta el perfil según el tamaño de campo nominal ingresado.

    Si no se ingresa tamaño de campo, devuelve los datos sin modificar.
    """
    if campo_size is None:
        return datos

    limite_inf = -campo_size / 2
    limite_sup = campo_size / 2

    datos_recortados = datos[
        (datos[perfil_col] >= limite_inf) & (datos[perfil_col] <= limite_sup)
    ].reset_index(drop=True)

    return datos_recortados
