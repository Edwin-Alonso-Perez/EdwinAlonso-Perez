# Sleep Health Analysis

#### Edwin Alonso Pérez Brees

Proyecto de análisis de datos y aprendizaje automático orientado a la predicción de la calidad del sueño a partir de variables de salud y estilo de vida. Se comparó un modelo Elastic Net con una red neuronal estándar bajo validación cruzada, resultando seleccionado Elastic Net por su mejor desempeño y mayor interpretabilidad. El análisis incluyó exploración de datos, evaluación de asimetría, estudio de correlaciones, interpretación de coeficientes y análisis de contribución relativa de predictores clave.
## Descripción del proyecto



Este proyecto desarrolla un flujo completo de análisis de datos sobre salud del sueño, desde la inspección y limpieza del conjunto de datos hasta la construcción y comparación de modelos predictivos.

El objetivo principal fue **predecir la variable `Quality of Sleep`** a partir de distintos factores fisiológicos y de estilo de vida, y evaluar qué variables muestran mayor influencia relativa sobre dicha respuesta.

Como parte del análisis, se compararon dos enfoques de modelado:

- **Elastic Net Regression**
- **Red neuronal estándar (`MLPRegressor`)**

La comparación se realizó mediante validación cruzada sobre el conjunto de entrenamiento, y posteriormente el mejor modelo se evaluó sobre un conjunto de prueba independiente.

---

## Objetivos

- Explorar la estructura del dataset y la calidad de los datos.
- Identificar valores faltantes, relaciones entre variables y posibles problemas de asimetría.
- Comparar un modelo lineal regularizado con un modelo no lineal.
- Seleccionar el mejor modelo con base en métricas de error y capacidad explicativa.
- Interpretar la contribución relativa de los factores más relevantes en la predicción.

---

## Flujo de trabajo

El análisis siguió las siguientes etapas:

1. **Inspección inicial del dataset**
   - revisión de columnas
   - identificación de datos faltantes
   - eliminación de columnas irrelevantes

2. **Análisis exploratorio**
   - matriz de correlación
   - evaluación de asimetría por variable
   - visualización de distribuciones
   - análisis gráfico de relaciones entre predictores y respuesta

3. **Preprocesamiento**
   - codificación de variables categóricas
   - construcción de variables derivadas
   - preparación del dataset para modelado

4. **Modelado predictivo**
   - separación de datos en entrenamiento y prueba (`80/20`)
   - validación cruzada de 10 folds sobre el conjunto de entrenamiento
   - comparación entre Elastic Net y red neuronal

5. **Interpretación del modelo**
   - extracción de coeficientes
   - análisis de contribución relativa
   - ejemplo de predicción sobre un dato del conjunto de prueba

---

## Modelos evaluados

### 1. Elastic Net Regression
Modelo lineal regularizado que combina penalización tipo L1 y L2.  
Se eligió como alternativa interpretable y robusta ante posibles correlaciones entre predictores.

### 2. Red neuronal estándar
Se utilizó un perceptrón multicapa (`MLPRegressor`) para explorar relaciones no lineales entre las variables explicativas y la calidad del sueño.

---

## Resultado principal

El modelo **Elastic Net** obtuvo mejor desempeño que la red neuronal en la comparación realizada, por lo que fue seleccionado como modelo final del proyecto.

Esto sugiere que, para este dataset, un modelo lineal regularizado ofrece una mejor relación entre:

- capacidad predictiva
- estabilidad
- interpretabilidad

---

## Hallazgos principales

A partir del análisis exploratorio y del modelo final, se observaron los siguientes resultados:

- Existe una **tendencia negativa** entre `Heart Rate` y `Quality of Sleep`: conforme aumenta la frecuencia cardíaca, la calidad del sueño tiende a disminuir.
- No se encontró evidencia suficiente para justificar una transformación formal de `Heart Rate`, ya que la relación con la variable respuesta podía interpretarse razonablemente en su escala original.
- El modelo Elastic Net permitió identificar los factores con mayor peso relativo dentro del ajuste.
- El gráfico de contribuciones mostró que una parte importante de la predicción se concentra en un grupo reducido de variables, lo cual facilita la interpretación del modelo.

### Conclusión analítica
En términos prácticos, el análisis sugiere que la calidad del sueño puede explicarse y predecirse razonablemente a partir de factores fisiológicos y de estilo de vida, y que un enfoque lineal regularizado resulta suficiente para capturar la estructura principal del problema en este conjunto de datos.

---

## Variables más influyentes

Con base en los coeficientes del modelo Elastic Net y el análisis de contribución relativa, las variables más relevantes fueron:

- `Stress Level`
- `Sleep Duration`
- `BMI Category` / variable ordinal asociada
- `Heart Rate` (con efecto negativo)
- otras variables complementarias según el ajuste final

> **Nota:** la contribución relativa se calculó a partir de la magnitud de los coeficientes del modelo, por lo que debe interpretarse como una medida de importancia dentro del ajuste, no como evidencia causal.

---

## Evaluación del modelo

La comparación entre modelos se realizó mediante validación cruzada sobre el conjunto de entrenamiento.  
El modelo final se evaluó luego sobre un **conjunto de prueba independiente (20 % del dataset)**.

### Métricas reportadas

- **RMSE (test):** `0.316`
- **MAE (test):** `0.263`
- **R² (test):** `0.934`

Estas métricas permiten estimar la capacidad de generalización del modelo sobre datos no vistos durante el entrenamiento.

---

## Ejemplo de interpretación

Además de las métricas globales, se analizó una predicción individual usando un dato tomado del conjunto de prueba.  
Esto permitió descomponer la salida del modelo en aportes por variable, mostrando de forma explícita qué factores empujan la predicción hacia arriba o hacia abajo.

Este paso fortalece la interpretabilidad del modelo y hace más claro cómo se traduce el ajuste estadístico en una predicción concreta.

---

## Estructura del repositorio

```text

├── Sleep health analysis.ipynb
├── README.md
├── requirements.txt
└── data/ 