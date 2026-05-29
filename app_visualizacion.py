"""
Dashboard exploratorio de rendimiento estudiantil — Proyecto CDP.
"""
import pandas as pd
import plotly.express as px
import streamlit as st

from ui_tema import (
    COLORES_NIVEL_NOMBRE,
    COLOR_AZUL,
    COLOR_PRIMARIO,
    COLOR_ACENTO,
    aplicar_tema,
    cerrar_seccion,
    etiqueta_variable,
    estilo_plotly,
    fila_kpis,
    hero,
    preparar_datos_es,
    titulo_seccion,
)

st.set_page_config(
    page_title="Panel de rendimiento estudiantil",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

aplicar_tema()


@st.cache_data
def cargar_datos(ruta: str) -> pd.DataFrame:
    df = pd.read_csv(ruta)
    df = df.dropna()
    df = df[df["Exam_Score"] <= 100].copy()
    df["Nivel"] = pd.cut(
        df["Exam_Score"],
        bins=[-1, 64, 74, 100],
        labels=["Deficiente", "Básico", "Superior"],
    )
    return df


df_raw = cargar_datos("data/StudentPerformance.csv")
df = preparar_datos_es(df_raw)

COL_GENERO = etiqueta_variable("Gender")
COL_MOTIV = etiqueta_variable("Motivation_Level")
COL_INTERNET = etiqueta_variable("Internet_Access")
COL_COLEGIO = etiqueta_variable("School_Type")
COL_HORAS = etiqueta_variable("Hours_Studied")
COL_ASIST = etiqueta_variable("Attendance")
COL_NOTA = etiqueta_variable("Exam_Score")
COL_NIVEL = "Nivel de desempeño"
COL_NOTAS_ANT = etiqueta_variable("Previous_Scores")

MAPA_NIVEL = COLORES_NIVEL_NOMBRE

# ── Barra lateral: solo filtros ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔵 Filtros")
    st.caption("Refina la muestra; los gráficos se actualizan al instante.")

    with st.expander("👤 Perfil", expanded=True):
        genero_opciones = sorted(df[COL_GENERO].dropna().unique())
        genero_sel = st.multiselect(COL_GENERO, genero_opciones, default=genero_opciones)
        motivacion_sel = st.multiselect(
            COL_MOTIV, ["Bajo", "Medio", "Alto"], default=["Bajo", "Medio", "Alto"]
        )

    with st.expander("🏫 Contexto escolar", expanded=True):
        internet_sel = st.multiselect(
            COL_INTERNET,
            sorted(df[COL_INTERNET].dropna().unique()),
            default=list(df[COL_INTERNET].dropna().unique()),
        )
        escuela_sel = st.multiselect(
            COL_COLEGIO,
            sorted(df[COL_COLEGIO].dropna().unique()),
            default=list(df[COL_COLEGIO].dropna().unique()),
        )

    with st.expander("📐 Esfuerzo académico", expanded=True):
        horas_min, horas_max = st.slider(
            COL_HORAS,
            int(df[COL_HORAS].min()),
            int(df[COL_HORAS].max()),
            (int(df[COL_HORAS].min()), int(df[COL_HORAS].max())),
        )
        asist_min, asist_max = st.slider(
            COL_ASIST,
            int(df[COL_ASIST].min()),
            int(df[COL_ASIST].max()),
            (int(df[COL_ASIST].min()), int(df[COL_ASIST].max())),
        )

    st.markdown("---")
    st.caption(f"📊 Base total: **{len(df):,}** estudiantes")

mask = (
    df[COL_GENERO].isin(genero_sel)
    & df[COL_MOTIV].isin(motivacion_sel)
    & df[COL_INTERNET].isin(internet_sel)
    & df[COL_COLEGIO].isin(escuela_sel)
    & df[COL_HORAS].between(horas_min, horas_max)
    & df[COL_ASIST].between(asist_min, asist_max)
)
dff = df[mask]

if len(dff) == 0:
    st.warning("⚠️ No hay estudiantes con esos criterios. Amplía los filtros en la barra lateral.")
    st.stop()

n = len(dff)
pct_deficiente = (dff[COL_NIVEL] == "Deficiente").mean() * 100
pct_superior = (dff[COL_NIVEL] == "Superior").mean() * 100
pct_basico = (dff[COL_NIVEL] == "Básico").mean() * 100

# ── Cabecera compacta ─────────────────────────────────────────────────────────
col_hero, col_resumen = st.columns([2, 1])
with col_hero:
    hero(
        "Panel de rendimiento estudiantil",
        "Explora cómo la asistencia, el estudio y el contexto se relacionan con la nota del examen.",
        "📖",
    )
with col_resumen:
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(160deg, #1E293B, #334155);
            border: 1px solid #475569;
            border-left: 4px solid {COLOR_AZUL};
            border-radius: 14px;
            padding: 1.1rem 1.2rem;
            margin-top: 0.2rem;
        ">
            <p style="color:#94A3B8;margin:0;font-size:0.85rem;">Muestra activa</p>
            <p style="color:#F8FAFC;margin:0.2rem 0 0;font-size:1.75rem;font-weight:700;">{n:,}</p>
            <p style="color:#93C5FD;margin:0.5rem 0 0;font-size:0.88rem;">
                {pct_basico:.0f} % Básico · {pct_deficiente:.0f} % Deficiente · {pct_superior:.0f} % Superior
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if pct_deficiente > 25:
    st.info("📌 Alta proporción de nivel **Deficiente** en esta muestra: prioriza apoyo académico.")

fila_kpis(
    [
        ("👥 Estudiantes", f"{n:,}", ""),
        ("📝 Nota promedio", f"{dff[COL_NOTA].mean():.1f}", ""),
        ("📅 Asistencia media", f"{dff[COL_ASIST].mean():.0f} %", ""),
        ("🔴 % Deficiente", f"{pct_deficiente:.1f} %", ""),
        ("🟢 % Superior", f"{pct_superior:.1f} %", ""),
    ]
)

st.markdown("---")

# ── Navegación por secciones (evita pestañas ilegibles) ─────────────────────
seccion = st.radio(
    "Sección del análisis",
    options=[
        "Panorama general",
        "Perfil por factores",
        "Relaciones clave",
        "Tabla de datos",
    ],
    horizontal=True,
    label_visibility="collapsed",
)

st.caption("Usa las secciones para recorrer el análisis en orden lógico: resumen → factores → relaciones → datos.")

# ── 1. Panorama general ─────────────────────────────────────────────────────
if seccion == "Panorama general":
    titulo_seccion(
        "📊 Panorama general",
        "Distribución de notas y niveles de desempeño en la muestra filtrada.",
    )
    c1, c2 = st.columns(2)
    with c1:
        fig_hist = px.histogram(
            dff,
            x=COL_NOTA,
            nbins=30,
            title=f"Distribución de la nota del examen (n = {n:,})",
            color_discrete_sequence=[COLOR_AZUL],
            labels={COL_NOTA: "Nota", "count": "Cantidad"},
        )
        st.plotly_chart(estilo_plotly(fig_hist), use_container_width=True)
    with c2:
        conteo = dff[COL_NIVEL].value_counts().reset_index()
        conteo.columns = [COL_NIVEL, "Cantidad"]
        fig_bar = px.bar(
            conteo,
            x=COL_NIVEL,
            y="Cantidad",
            title=f"Estudiantes por nivel (n = {n:,})",
            color=COL_NIVEL,
            color_discrete_map=MAPA_NIVEL,
            text="Cantidad",
        )
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(estilo_plotly(fig_bar), use_container_width=True)
    cerrar_seccion()

# ── 2. Perfil por factores ──────────────────────────────────────────────────
elif seccion == "Perfil por factores":
    titulo_seccion(
        "🏷️ Perfil por factores",
        "Comparación de notas según motivación y tipo de colegio.",
    )
    c1, c2 = st.columns(2)
    with c1:
        fig_mot = px.box(
            dff,
            x=COL_MOTIV,
            y=COL_NOTA,
            color=COL_MOTIV,
            title=f"Nota según motivación (n = {n:,})",
            category_orders={COL_MOTIV: ["Bajo", "Medio", "Alto"]},
            color_discrete_map={"Bajo": "#C1121F", "Medio": "#E85D04", "Alto": "#2A9D8F"},
        )
        st.plotly_chart(estilo_plotly(fig_mot), use_container_width=True)
    with c2:
        fig_col = px.box(
            dff,
            x=COL_COLEGIO,
            y=COL_NOTA,
            color=COL_COLEGIO,
            title=f"Nota según tipo de colegio (n = {n:,})",
            color_discrete_sequence=[COLOR_AZUL, COLOR_ACENTO],
        )
        st.plotly_chart(estilo_plotly(fig_col), use_container_width=True)

    fig_int = px.box(
        dff,
        x=COL_INTERNET,
        y=COL_NOTA,
        color=COL_INTERNET,
        title=f"Nota según acceso a internet (n = {n:,})",
        color_discrete_sequence=[COLOR_PRIMARIO, COLOR_AZUL],
    )
    st.plotly_chart(estilo_plotly(fig_int), use_container_width=True)
    cerrar_seccion()

# ── 3. Relaciones clave ───────────────────────────────────────────────────────
elif seccion == "Relaciones clave":
    titulo_seccion(
        "🔗 Relaciones clave",
        "Tendencias entre estudio, asistencia, historial y nota final.",
    )

    fig_estudio = px.scatter(
        dff,
        x=COL_HORAS,
        y=COL_NOTA,
        color=COL_NIVEL,
        size=COL_ASIST,
        hover_data=[COL_GENERO, COL_MOTIV, COL_NOTAS_ANT],
        title=f"Horas de estudio vs. nota (tamaño = asistencia) · n = {n:,}",
        color_discrete_map=MAPA_NIVEL,
        trendline="ols",
    )
    st.plotly_chart(estilo_plotly(fig_estudio), use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        fig_asist = px.scatter(
            dff,
            x=COL_ASIST,
            y=COL_NOTA,
            color=COL_NIVEL,
            title=f"Asistencia vs. nota (n = {n:,})",
            color_discrete_map=MAPA_NIVEL,
            trendline="ols",
        )
        st.plotly_chart(estilo_plotly(fig_asist), use_container_width=True)
    with col_b:
        fig_prev = px.scatter(
            dff,
            x=COL_NOTAS_ANT,
            y=COL_NOTA,
            color=COL_INTERNET,
            title=f"Notas anteriores vs. nota (n = {n:,})",
            trendline="ols",
            color_discrete_sequence=[COLOR_AZUL, COLOR_PRIMARIO],
        )
        st.plotly_chart(estilo_plotly(fig_prev), use_container_width=True)
    cerrar_seccion()

# ── 4. Tabla de datos ─────────────────────────────────────────────────────────
else:
    titulo_seccion(
        "📋 Tabla de datos",
        "Registros de la muestra filtrada; puedes descargarlos en CSV.",
    )
    columnas_mostrar = [
        c
        for c in [
            COL_HORAS,
            COL_ASIST,
            COL_NOTA,
            COL_NIVEL,
            COL_GENERO,
            COL_MOTIV,
            COL_COLEGIO,
            COL_INTERNET,
            COL_NOTAS_ANT,
        ]
        if c in dff.columns
    ]
    st.dataframe(
        dff[columnas_mostrar],
        use_container_width=True,
        height=460,
        hide_index=True,
    )
    csv = dff[columnas_mostrar].to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ Descargar muestra filtrada (CSV)",
        csv,
        "estudiantes_filtrados.csv",
        "text/csv",
        use_container_width=True,
    )
    cerrar_seccion()
