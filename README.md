# 📖 Panel de Rendimiento Estudiantil — Dashboard Exploratorio

Aplicación interactiva de visualización para explorar cómo la asistencia, el esfuerzo académico y el contexto socioeducativo se relacionan con el desempeño de los estudiantes.

---

## 📋 Descripción

El dashboard permite filtrar y analizar una población de estudiantes en tiempo real, segmentando por perfil, contexto escolar y hábitos de estudio. Todas las gráficas se actualizan automáticamente al modificar los filtros de la barra lateral.

Los niveles de desempeño se definen así:

| Nivel | Rango de nota | Indicador |
|---|---|---|
| 🔴 Deficiente | ≤ 64 | Requiere atención prioritaria |
| 🟠 Básico | 65 – 74 | Rendimiento intermedio |
| 🟢 Superior | ≥ 75 | Buen desempeño académico |

---

## 📁 Estructura de archivos

```
rendimiento-estudiantes-streamlit/
│
├── app_visualizacion.py        # App del dashboard (este módulo)
├── ui_tema.py                  # Componentes visuales y tema compartido
│
└── data/
    └── StudentPerformance.csv  # Dataset base
```

---

## ⚙️ Requisitos

```txt
streamlit
pandas
numpy
plotly
scipy
statsmodels
```

> **Python requerido: 3.11**

---

## 🚀 Ejecución local

### 1. Instalar dependencias

```bash
pip install streamlit pandas numpy plotly scipy statsmodels
```

### 2. Lanzar la app

```bash
streamlit run app_visualizacion.py
```

---

## 🔍 Filtros disponibles

Desde la barra lateral se puede segmentar la muestra por:

**👤 Perfil**
- Género (Femenino / Masculino)
- Nivel de motivación (Bajo / Medio / Alto)

**🏫 Contexto escolar**
- Acceso a internet (Sí / No)
- Tipo de colegio (Público / Privado)

**📐 Esfuerzo académico**
- Rango de horas de estudio semanales
- Rango de porcentaje de asistencia

---

## 📊 Secciones del análisis

La app está organizada en 4 secciones navegables:

### 1. 📊 Panorama general
Visión global de la muestra filtrada.

| Gráfica | Descripción |
|---|---|
| Histograma de notas | Distribución de los puntajes del examen final |
| Estudiantes por nivel | Conteo por categoría: Deficiente, Básico, Superior |

### 2. 🏷️ Perfil por factores
Comparación de notas según variables de contexto, usando diagramas de caja (box plots).

| Gráfica | Variable comparada |
|---|---|
| Nota según motivación | Bajo / Medio / Alto |
| Nota según tipo de colegio | Público / Privado |
| Nota según acceso a internet | Sí / No |

### 3. 🔗 Relaciones clave
Diagramas de dispersión con líneas de tendencia (OLS) para identificar correlaciones.

| Gráfica | Ejes |
|---|---|
| Horas de estudio vs. nota | X: horas · Y: nota · Tamaño: asistencia |
| Asistencia vs. nota | X: asistencia % · Y: nota |
| Notas anteriores vs. nota | X: historial · Y: nota actual |

### 4. 📋 Tabla de datos
Registros individuales de la muestra filtrada con opción de descarga en CSV.

---

## 📈 Métricas del encabezado

Al inicio de la app se muestran 5 KPIs que se actualizan con cada cambio de filtro:

- **Estudiantes** — total de la muestra activa
- **Nota promedio** — media del examen en la muestra
- **Asistencia media** — promedio del porcentaje de asistencia
- **% Deficiente** — proporción de estudiantes con nota ≤ 64
- **% Superior** — proporción de estudiantes con nota ≥ 75

---

## Equipo (proyecto CDP)

- Nicol Camila Villalobos
- Juan David Caballero
- Camilo Andrés Sánchez
- Juan Sebastián Diaz

