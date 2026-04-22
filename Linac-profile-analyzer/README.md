---
editor_options: 
  markdown: 
    wrap: 72
---

# LINAC Profile Analyzer

Aplicación en Python con interfaz gráfica para procesar perfiles de
dosis medidos en un acelerador lineal.

El programa permite cargar archivos de datos experimentales, normalizar
el perfil de dosis y calcular parámetros dosimétricos como:

-   Planitud
-   Simetría
-   Tamaño de campo al 50 %
-   Penumbra 80–20 %
-   Gráfica del perfil normalizado

## Características

-   Interfaz gráfica desarrollada con Tkinter.
-   Lectura de archivos de texto o CSV.
-   Conversión automática de separador decimal con coma.
-   Detección básica de unidades en mm y conversión a cm.
-   Normalización del perfil respecto al eje central.
-   Visualización de resultados y gráfica dentro de la interfaz.

## Formato esperado de los datos

El archivo debe contener al menos dos columnas:

1.  Posición del perfil
2.  Valor de dosis o señal medida
