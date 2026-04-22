"""
Funciones para calcular métricas de perfiles de dosis.

Las funciones trabajan con un DataFrame que contiene, como mínimo, dos columnas:
- Perfil: posición del perfil, preferiblemente en cm.
- Dosis: valor de dosis, señal o lectura asociada al perfil.

La lógica de cálculo conserva el comportamiento del script original.
"""

from __future__ import annotations

from typing import Optional, Tuple

import numpy as np
import pandas as pd


DEFAULT_PROFILE_COLUMN = "Perfil"
DEFAULT_DOSE_COLUMN = "Dosis"


def normalizar(
    datos: pd.DataFrame,
    perfil_col: str = DEFAULT_PROFILE_COLUMN,
    dosis_col: str = DEFAULT_DOSE_COLUMN,
) -> pd.DataFrame:
    """
    Normaliza el perfil respecto al valor ubicado más cerca del eje central.

    El valor central queda normalizado a 100, igual que en el script original.
    """
    datos_limpios = datos.dropna(subset=[perfil_col, dosis_col]).reset_index(drop=True)

    if datos_limpios.empty:
        raise ValueError("No hay datos válidos para normalizar")

    idx_ref = datos_limpios[perfil_col].abs().idxmin()
    valor_ref = datos_limpios.loc[idx_ref, dosis_col]

    normalizados = pd.DataFrame(columns=[perfil_col, dosis_col])
    normalizados[perfil_col] = datos_limpios[perfil_col]
    normalizados[dosis_col] = (datos_limpios[dosis_col] / valor_ref) * 100
    return normalizados


def calcular_planitud(
    datos: pd.DataFrame,
    perfil_col: str = DEFAULT_PROFILE_COLUMN,
    dosis_col: str = DEFAULT_DOSE_COLUMN,
) -> float:
    """
    Calcula la planitud usando el 80 % central del perfil.

    Se conserva el criterio original basado en cuantiles 0,10 y 0,90.
    """
    q_bajo = datos[perfil_col].quantile(0.10)
    q_alto = datos[perfil_col].quantile(0.90)
    df_filtrado = datos[(datos[perfil_col] >= q_bajo) & (datos[perfil_col] <= q_alto)]

    d_max = df_filtrado[dosis_col].max()
    d_min = df_filtrado[dosis_col].min()
    planitud = ((d_max - d_min) / (d_max + d_min)) * 100
    return float(planitud)


def calcular_simetria(
    datos: pd.DataFrame,
    perfil_col: str = DEFAULT_PROFILE_COLUMN,
    dosis_col: str = DEFAULT_DOSE_COLUMN,
) -> Tuple[Optional[float], Optional[tuple]]:
    """
    Calcula la simetría del perfil.

    Devuelve:
    - valor máximo de diferencia porcentual.
    - par de puntos usado para obtener dicha diferencia.

    La comparación se realiza contra el punto opuesto mediante interpolación,
    siguiendo la lógica del script original.
    """
    df = datos.dropna(subset=[perfil_col, dosis_col]).copy()
    df = (
        df.sort_values(by=perfil_col)
        .drop_duplicates(subset=perfil_col, keep="first")
        .reset_index(drop=True)
    )

    if df.empty:
        return None, None

    valor_central = df.loc[df[perfil_col].abs().idxmin(), dosis_col]

    q_bajo = df[perfil_col].quantile(0.10)
    q_alto = df[perfil_col].quantile(0.90)
    df_filtrado = df[(df[perfil_col] >= q_bajo) & (df[perfil_col] <= q_alto)]

    diferencias = []
    pares = []

    perfiles = df_filtrado[perfil_col].to_numpy()
    dosis = df_filtrado[dosis_col].to_numpy()

    for x, y in zip(perfiles, dosis):
        x_op = -x
        if (x_op >= perfiles.min()) and (x_op <= perfiles.max()):
            y_op = np.interp(x_op, perfiles, dosis)
            diff = abs(y - y_op) / valor_central * 100.0
            diferencias.append(diff)
            pares.append(((x, y), (x_op, y_op)))

    if diferencias:
        idx_max = int(np.argmax(diferencias))
        return float(diferencias[idx_max]), pares[idx_max]

    return None, None


def calcular_tamano_campo(
    datos: pd.DataFrame,
    perfil_col: str = DEFAULT_PROFILE_COLUMN,
    dosis_col: str = DEFAULT_DOSE_COLUMN,
    nivel: float = 0.5,
) -> Tuple[Optional[float], Tuple[Optional[float], Optional[float]]]:
    """
    Calcula el tamaño de campo al nivel especificado.

    Por defecto usa el nivel del 50 %. Devuelve:
    - ancho del campo.
    - posiciones izquierda y derecha de cruce.
    """
    datos_ordenados = datos.sort_values(by=perfil_col).reset_index(drop=True)
    perfiles = datos_ordenados[perfil_col].to_numpy()
    dosis = datos_ordenados[dosis_col].to_numpy()

    if perfiles.size < 2:
        return None, (None, None)

    idx_centro = int(np.argmin(np.abs(perfiles)))
    valor_central = dosis[idx_centro]
    if valor_central == 0:
        return None, (None, None)

    dosis_norm = dosis / valor_central
    diferencia = dosis_norm - nivel

    cambios = np.where(np.sign(diferencia[:-1]) != np.sign(diferencia[1:]))[0]
    toque_izquierdo = np.where((diferencia[:-1] == 0) & (diferencia[1:] != 0))[0]
    toque_derecho = np.where((diferencia[1:] == 0) & (diferencia[:-1] != 0))[0]
    toque_doble = np.where((diferencia[:-1] == 0) & (diferencia[1:] == 0))[0]

    cruces_idx = np.unique(
        np.concatenate([cambios, toque_izquierdo, toque_derecho, toque_doble])
    )

    if cruces_idx.size == 0:
        return None, (None, None)

    menores = cruces_idx[cruces_idx < idx_centro]
    mayores = cruces_idx[cruces_idx >= idx_centro]
    idx_izq = menores[-1] if menores.size > 0 else None
    idx_der = mayores[0] if mayores.size > 0 else None

    def interpolar_x(i: Optional[int]) -> Optional[float]:
        if i is None:
            return None
        x0, x1 = perfiles[i], perfiles[i + 1]
        y0, y1 = dosis_norm[i], dosis_norm[i + 1]
        if y1 == y0:
            return 0.5 * (x0 + x1)
        t = (nivel - y0) / (y1 - y0)
        return float(x0 + t * (x1 - x0))

    x_izq = interpolar_x(idx_izq)
    x_der = interpolar_x(idx_der)

    if (x_izq is None) or (x_der is None):
        return None, (x_izq, x_der)

    ancho = x_der - x_izq
    return float(ancho), (float(x_izq), float(x_der))


def calcular_penumbra(
    datos: pd.DataFrame,
    perfil_col: str = DEFAULT_PROFILE_COLUMN,
    dosis_col: str = DEFAULT_DOSE_COLUMN,
) -> Tuple[Optional[float], Optional[float]]:
    """
    Calcula la penumbra 80-20 %.

    Devuelve la penumbra izquierda y derecha en mm, asumiendo que el perfil está en cm.
    """
    datos_ordenados = datos.sort_values(by=perfil_col).reset_index(drop=True)
    perfiles = datos_ordenados[perfil_col].to_numpy()
    dosis = datos_ordenados[dosis_col].to_numpy()

    if perfiles.size < 2:
        return None, None

    idx_centro = int(np.argmin(np.abs(perfiles)))
    valor_central = dosis[idx_centro]
    if valor_central == 0:
        return None, None

    dosis_norm = dosis / valor_central
    niveles = (0.8, 0.2)

    def obtener_cruces_indices(y: np.ndarray, nivel: float) -> np.ndarray:
        diferencia = y - nivel
        cambio_signo = np.where(np.sign(diferencia[:-1]) != np.sign(diferencia[1:]))[0]
        toque_izquierdo = np.where((diferencia[:-1] == 0) & (diferencia[1:] != 0))[0]
        toque_derecho = np.where((diferencia[1:] == 0) & (diferencia[:-1] != 0))[0]
        toque_doble = np.where((diferencia[:-1] == 0) & (diferencia[1:] == 0))[0]
        return np.unique(
            np.concatenate([cambio_signo, toque_izquierdo, toque_derecho, toque_doble])
        )

    def interpolar_x(i: Optional[int], x: np.ndarray, y: np.ndarray, nivel: float) -> Optional[float]:
        if i is None:
            return None
        x0, x1 = x[i], x[i + 1]
        y0, y1 = y[i], y[i + 1]
        if y1 == y0:
            return float(0.5 * (x0 + x1))
        t = (nivel - y0) / (y1 - y0)
        return float(x0 + t * (x1 - x0))

    cruces_80 = obtener_cruces_indices(dosis_norm, niveles[0])
    cruces_20 = obtener_cruces_indices(dosis_norm, niveles[1])

    def seleccionar_izquierda_derecha(cruces: np.ndarray) -> Tuple[Optional[int], Optional[int]]:
        if cruces.size == 0:
            return None, None
        menores = cruces[cruces < idx_centro]
        mayores = cruces[cruces >= idx_centro]
        izquierda = menores[-1] if menores.size > 0 else None
        derecha = mayores[0] if mayores.size > 0 else None
        return izquierda, derecha

    i80_izq, i80_der = seleccionar_izquierda_derecha(cruces_80)
    i20_izq, i20_der = seleccionar_izquierda_derecha(cruces_20)

    x80_izq = interpolar_x(i80_izq, perfiles, dosis_norm, niveles[0])
    x20_izq = interpolar_x(i20_izq, perfiles, dosis_norm, niveles[1])
    x80_der = interpolar_x(i80_der, perfiles, dosis_norm, niveles[0])
    x20_der = interpolar_x(i20_der, perfiles, dosis_norm, niveles[1])

    penumbra_izq = None
    penumbra_der = None

    if (x80_izq is not None) and (x20_izq is not None):
        penumbra_izq = abs(x20_izq - x80_izq)
    if (x80_der is not None) and (x20_der is not None):
        penumbra_der = abs(x20_der - x80_der)

    return (
        float(penumbra_izq) * 10 if penumbra_izq is not None else None,
        float(penumbra_der) * 10 if penumbra_der is not None else None,
    )
