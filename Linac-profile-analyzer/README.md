# LINAC Profile Analyzer

Aplicación en Python con interfaz gráfica para procesar perfiles de dosis medidos en un acelerador lineal.

El programa permite cargar archivos de datos experimentales, normalizar el perfil de dosis y calcular parámetros dosimétricos como:

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

El archivo debe contener al menos dos columnas numéricas:

1.  Posición del perfil.
2.  Valor de dosis o señal medida.

El programa puede leer archivos separados por espacios o tabulaciones. También admite valores con coma como separador decimal.

El archivo puede incluir una línea inicial de encabezado con información del perfil, por ejemplo:

``` txt
Depth[mm] = 20,0  Offaxis[mm] = 0,0  Fieldsize[cm x cm] = 10,0 x 10,0  Energy[MV/MeV] = 6,0
```

Ejemplo de datos:

``` txt
-50,000    8,9500E+03
-49,000    1,0750E+04
-48,000    1,1250E+04
...
0,000      1,1700E+04
...
48,000     1,1300E+04
49,000     1,0800E+04
50,000     8,9700E+03
```

## Datos de ejemplo

El repositorio incluye un archivo de muestra en:

``` txt
data/sample_profile_synthetic.txt
```

Este archivo contiene un perfil sintético creado únicamente para probar el funcionamiento del programa.

Los datos incluidos no corresponden a mediciones clínicas reales ni a información institucional.

## Dependencias

El proyecto utiliza las siguientes librerías:

-   Python 3
-   NumPy
-   Pandas
-   Matplotlib
-   Tkinter

## Parámetros calculados

### Planitud

La planitud se calcula a partir de los valores máximo y mínimo de dosis dentro de la región central del perfil.

### Simetría

La simetría se calcula comparando puntos opuestos del perfil respecto al eje central. Cuando no existe un punto exactamente opuesto, el programa utiliza interpolación lineal.

### Tamaño de campo

El tamaño de campo se calcula a partir de los puntos de cruce al 50 % de la dosis central normalizada.

### Penumbra

La penumbra se calcula como la distancia entre los puntos correspondientes al 80 % y 20 % de la dosis normalizada en cada lado del perfil.

## Interfaz gráfica

La aplicación muestra los valores calculados y la gráfica del perfil normalizado dentro de la misma ventana.

<img src="data/images/Intergaz%20grafica_results.png" alt="Interfaz principal" width="450">

## Consideraciones

-   El programa está diseñado para analizar perfiles de dosis de aceleradores lineales.

-   El archivo de entrada debe contener al menos dos columnas numéricas.

-   Si el rango de posiciones supera 50, el programa interpreta que las posiciones están en milímetros y las convierte a centímetros.

-   El archivo de ejemplo es sintético y se incluye solo con fines demostrativos.

-   No se recomienda subir datos clínicos, institucionales o privados al repositorio.
