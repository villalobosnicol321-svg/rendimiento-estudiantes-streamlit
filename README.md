# Predicción de rendimiento estudiantil (multiclase)

Aplicación de **Ciencia de Datos** para explorar y predecir el nivel de desempeño académico en tres categorías:

| Nivel | Rango de nota del examen |
|-------|--------------------------|
| **Deficiente** | ≤ 64 |
| **Básico** | 65 – 74 |
| **Superior** | ≥ 75 |

Incluye dos apps **Streamlit** y el entrenamiento de **6 modelos** (sección 13 del proyecto CDP): regresión logística, RL + SMOTE, árbol de decisión, bosque aleatorio, potenciación de gradiente y PCA + K-Means.

**Modelo recomendado:** Potenciación de gradiente (mejor F1-macro en prueba).

## Estructura del repositorio

```
rendimiento_estudiantes_app/
├── app_visualizacion.py    # Dashboard exploratorio
├── app_ml.py               # Predicción multiclase
├── entrenamiento.py        # Entrena y guarda los modelos
├── pca_kmeans_classifier.py
├── ui_tema.py              # Tema visual y traducciones
├── data/
│   └── StudentPerformance.csv
├── models/                 # Generado al ejecutar entrenamiento.py
├── requirements.txt
└── .vscode/tasks.json      # Tareas para VS Code
```

## Requisitos

- Windows 10/11 (o macOS/Linux con comandos equivalentes)
- [Python 3.10+](https://www.python.org/downloads/)
- [Visual Studio Code](https://code.visualstudio.com/) (recomendado)

## Instalación rápida

```powershell
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python entrenamiento.py
```

> **Nota:** `entrenamiento.py` tarda varios minutos (GridSearchCV). Solo hace falta ejecutarlo una vez, o cuando quieras reentrenar.

## Ejecutar las apps

**Visualización (puerto 8501):**

```powershell
python -m streamlit run app_visualizacion.py --server.port 8501
```

**Machine Learning (puerto 8502):**

```powershell
python -m streamlit run app_ml.py --server.port 8502
```

Abre en el navegador: `http://localhost:8501` y `http://localhost:8502`.

### Atajo en VS Code

`Ctrl+Shift+P` → **Tasks: Run Task** → `Streamlit: Ambas apps`

## Dataset

Archivo: `data/StudentPerformance.csv` (6 607 registros).

Origen: [Student Performance Factors](https://github.com/grugg1233/StudentPerformanceFactors) (Kaggle / repositorio público).

## Equipo (proyecto CDP)

- Nicol Camila Villalobos
- Juan David Caballero
- Camilo Andrés Sánchez
- Juan Sebastián Diaz

## Licencia

Uso académico. Consulta el archivo `LICENSE` si aplica distribución.
