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

# ── Encabezado principal ──────────────────────────────────────────────────────
st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F2440 100%);
        border-bottom: 3px solid {COLOR_AZUL};
        border-radius: 16px;
        padding: 2rem 2.2rem 1.6rem;
        margin-bottom: 1.4rem;
    ">
        <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.4rem;">
            <span style="font-size:2rem;">📖</span>
            <h1 style="color:#F8FAFC; margin:0; font-size:1.9rem; font-weight:800; letter-spacing:-0.5px;">
                Panel de rendimiento estudiantil
            </h1>
        </div>
        <p style="color:#94A3B8; margin:0; font-size:1rem; max-width:680px; line-height:1.5;">
            Explora cómo la asistencia, el esfuerzo y el contexto socioeducativo se relacionan
            con el desempeño académico. Usa los filtros de la barra lateral para segmentar la muestra.
        </p>
        <div style="display:flex; gap:1.5rem; margin-top:1rem; flex-wrap:wrap;">
            <span style="background:#1E3A5F; color:#93C5FD; padding:0.3rem 0.85rem; border-radius:20px; font-size:0.82rem; font-weight:600;">
                📊 {n:,} estudiantes activos
            </span>
            <span style="background:#1A3A2A; color:#6EE7B7; padding:0.3rem 0.85rem; border-radius:20px; font-size:0.82rem; font-weight:600;">
                🟢 Superior: {pct_superior:.1f} %
            </span>
            <span style="background:#3A1A1A; color:#FCA5A5; padding:0.3rem 0.85rem; border-radius:20px; font-size:0.82rem; font-weight:600;">
                🔴 Deficiente: {pct_deficiente:.1f} %
            </span>
            <span style="background:#2A2A1A; color:#FDE68A; padding:0.3rem 0.85rem; border-radius:20px; font-size:0.82rem; font-weight:600;">
                🟠 Básico: {pct_basico:.1f} %
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if pct_deficiente > 25:
    st.info("📌 Alta proporción de nivel **Deficiente** en esta muestra: prioriza apoyo académico.")

# ── Métricas reorganizadas ────────────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
nota_prom = dff[COL_NOTA].mean()
asist_prom = dff[COL_ASIST].mean()
horas_prom = dff[COL_HORAS].mean()

with m1:
    st.markdown(f"""
    <div style="background:#1E293B;border-radius:12px;padding:1rem 1.1rem;border-left:4px solid #60A5FA;text-align:center;">
        <p style="color:#94A3B8;font-size:0.8rem;margin:0;">👥 Estudiantes</p>
        <p style="color:#F8FAFC;font-size:1.6rem;font-weight:700;margin:0.2rem 0 0;">{n:,}</p>
        <p style="color:#64748B;font-size:0.72rem;margin:0.2rem 0 0;">muestra filtrada</p>
    </div>""", unsafe_allow_html=True)
with m2:
    color_nota = "#6EE7B7" if nota_prom >= 75 else "#FDE68A" if nota_prom >= 65 else "#FCA5A5"
    st.markdown(f"""
    <div style="background:#1E293B;border-radius:12px;padding:1rem 1.1rem;border-left:4px solid {color_nota};text-align:center;">
        <p style="color:#94A3B8;font-size:0.8rem;margin:0;">📝 Nota promedio</p>
        <p style="color:{color_nota};font-size:1.6rem;font-weight:700;margin:0.2rem 0 0;">{nota_prom:.1f}</p>
        <p style="color:#64748B;font-size:0.72rem;margin:0.2rem 0 0;">sobre 100 pts</p>
    </div>""", unsafe_allow_html=True)
with m3:
    color_asist = "#6EE7B7" if asist_prom >= 80 else "#FDE68A" if asist_prom >= 65 else "#FCA5A5"
    st.markdown(f"""
    <div style="background:#1E293B;border-radius:12px;padding:1rem 1.1rem;border-left:4px solid {color_asist};text-align:center;">
        <p style="color:#94A3B8;font-size:0.8rem;margin:0;">📅 Asistencia media</p>
        <p style="color:{color_asist};font-size:1.6rem;font-weight:700;margin:0.2rem 0 0;">{asist_prom:.0f} %</p>
        <p style="color:#64748B;font-size:0.72rem;margin:0.2rem 0 0;">promedio del grupo</p>
    </div>""", unsafe_allow_html=True)
with m4:
    st.markdown(f"""
    <div style="background:#1E293B;border-radius:12px;padding:1rem 1.1rem;border-left:4px solid #F87171;text-align:center;">
        <p style="color:#94A3B8;font-size:0.8rem;margin:0;">🔴 Nivel Deficiente</p>
        <p style="color:#F87171;font-size:1.6rem;font-weight:700;margin:0.2rem 0 0;">{pct_deficiente:.1f} %</p>
        <p style="color:#64748B;font-size:0.72rem;margin:0.2rem 0 0;">nota ≤ 64</p>
    </div>""", unsafe_allow_html=True)
with m5:
    st.markdown(f"""
    <div style="background:#1E293B;border-radius:12px;padding:1rem 1.1rem;border-left:4px solid #34D399;text-align:center;">
        <p style="color:#94A3B8;font-size:0.8rem;margin:0;">🟢 Nivel Superior</p>
        <p style="color:#34D399;font-size:1.6rem;font-weight:700;margin:0.2rem 0 0;">{pct_superior:.1f} %</p>
        <p style="color:#64748B;font-size:0.72rem;margin:0.2rem 0 0;">nota ≥ 75</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)

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
        st.markdown(
            """<div style="background:#1E293B;border-left:3px solid #60A5FA;border-radius:8px;
            padding:0.75rem 1rem;margin-top:-0.5rem;">
            <p style="color:#94A3B8;font-size:0.82rem;margin:0;line-height:1.6;">
            📖 <b style="color:#CBD5E1;">Cómo leerlo:</b> cada barra agrupa a los estudiantes cuya nota
            cae en ese rango. Una curva desplazada a la izquierda indica predominio de notas bajas.
            Los umbrales clave son <b style="color:#FCA5A5;">64</b> (límite Deficiente) y
            <b style="color:#FDE68A;">74</b> (límite Básico/Superior).
            </p></div>""",
            unsafe_allow_html=True,
        )
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
        st.markdown(
            """<div style="background:#1E293B;border-left:3px solid #A78BFA;border-radius:8px;
            padding:0.75rem 1rem;margin-top:-0.5rem;">
            <p style="color:#94A3B8;font-size:0.82rem;margin:0;line-height:1.6;">
            📖 <b style="color:#CBD5E1;">Cómo leerlo:</b> compara la cantidad de estudiantes en cada categoría.
            <b style="color:#FCA5A5;">Deficiente</b> (≤ 64), <b style="color:#FDE68A;">Básico</b> (65–74) y
            <b style="color:#6EE7B7;">Superior</b> (≥ 75). Una barra de Básico mucho más alta refleja el
            desbalance típico de esta población.
            </p></div>""",
            unsafe_allow_html=True,
        )
    cerrar_seccion()

# ── 2. Perfil por factores ──────────────────────────────────────────────────
elif seccion == "Perfil por factores":
    titulo_seccion(
        "🏷️ Perfil por factores",
        "Comparación de notas según motivación y tipo de colegio.",
    )
    st.markdown(
        """<div style="background:#1E293B;border-left:3px solid #60A5FA;border-radius:8px;
        padding:0.65rem 1rem;margin-bottom:0.8rem;">
        <p style="color:#94A3B8;font-size:0.82rem;margin:0;line-height:1.6;">
        📖 <b style="color:#CBD5E1;">Cómo leer los diagramas de caja:</b>
        la <b style="color:#F8FAFC;">línea central</b> es la mediana (nota típica del grupo).
        La <b style="color:#F8FAFC;">caja</b> abarca el 50 % central de los estudiantes.
        Los <b style="color:#F8FAFC;">bigotes</b> muestran el rango general; los puntos aislados son casos atípicos.
        Cajas más altas = notas más altas en ese grupo.
        </p></div>""",
        unsafe_allow_html=True,
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
        st.markdown(
            """<div style="background:#1E293B;border-left:3px solid #2A9D8F;border-radius:8px;
            padding:0.65rem 1rem;margin-top:-0.5rem;">
            <p style="color:#94A3B8;font-size:0.82rem;margin:0;line-height:1.5;">
            ¿La caja verde (Alto) está claramente por encima de la roja (Bajo)?
            Eso indica que la motivación sí influye en el rendimiento.
            </p></div>""",
            unsafe_allow_html=True,
        )
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
        st.markdown(
            """<div style="background:#1E293B;border-left:3px solid #F59E0B;border-radius:8px;
            padding:0.65rem 1rem;margin-top:-0.5rem;">
            <p style="color:#94A3B8;font-size:0.82rem;margin:0;line-height:1.5;">
            Si las cajas de Público y Privado se solapan mucho, el tipo de colegio no es
            determinante por sí solo. Cajas separadas indican una brecha real.
            </p></div>""",
            unsafe_allow_html=True,
        )

    fig_int = px.box(
        dff,
        x=COL_INTERNET,
        y=COL_NOTA,
        color=COL_INTERNET,
        title=f"Nota según acceso a internet (n = {n:,})",
        color_discrete_sequence=[COLOR_PRIMARIO, COLOR_AZUL],
    )
    st.plotly_chart(estilo_plotly(fig_int), use_container_width=True)
    st.markdown(
        """<div style="background:#1E293B;border-left:3px solid #818CF8;border-radius:8px;
        padding:0.65rem 1rem;margin-top:-0.5rem;">
        <p style="color:#94A3B8;font-size:0.82rem;margin:0;line-height:1.5;">
        📖 <b style="color:#CBD5E1;">Acceso a internet:</b> compara la distribución de notas entre
        quienes tienen acceso y quienes no. Una caja más alta en "Sí" sugiere que la conectividad
        está asociada a mejores resultados académicos.
        </p></div>""",
        unsafe_allow_html=True,
    )
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
    st.markdown(
        """<div style="background:#1E293B;border-left:3px solid #60A5FA;border-radius:8px;
        padding:0.75rem 1rem;margin-top:-0.5rem;margin-bottom:1rem;">
        <p style="color:#94A3B8;font-size:0.82rem;margin:0;line-height:1.6;">
        📖 <b style="color:#CBD5E1;">Cómo leerlo:</b> cada punto es un estudiante.
        El <b style="color:#F8FAFC;">eje X</b> muestra las horas de estudio semanales y el
        <b style="color:#F8FAFC;">eje Y</b> la nota del examen. El <b style="color:#F8FAFC;">tamaño</b>
        del punto refleja el % de asistencia (puntos más grandes = más asistencia).
        El <b style="color:#F8FAFC;">color</b> indica el nivel de desempeño.
        La <b style="color:#F8FAFC;">línea de tendencia</b> muestra si más horas de estudio
        se asocian con mejores notas. Pasa el cursor sobre un punto para ver más detalles.
        </p></div>""",
        unsafe_allow_html=True,
    )

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
        st.markdown(
            """<div style="background:#1E293B;border-left:3px solid #34D399;border-radius:8px;
            padding:0.65rem 1rem;margin-top:-0.5rem;">
            <p style="color:#94A3B8;font-size:0.82rem;margin:0;line-height:1.5;">
            📖 <b style="color:#CBD5E1;">Asistencia vs. nota:</b> si la línea sube hacia la derecha,
            mayor asistencia se asocia con mejores resultados. Una nube muy dispersa indica
            que la asistencia sola no explica el rendimiento.
            </p></div>""",
            unsafe_allow_html=True,
        )
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
        st.markdown(
            """<div style="background:#1E293B;border-left:3px solid #F59E0B;border-radius:8px;
            padding:0.65rem 1rem;margin-top:-0.5rem;">
            <p style="color:#94A3B8;font-size:0.82rem;margin:0;line-height:1.5;">
            📖 <b style="color:#CBD5E1;">Historial académico:</b> una tendencia positiva confirma
            que el rendimiento pasado predice el futuro. El color distingue si el estudiante
            tiene acceso a internet o no.
            </p></div>""",
            unsafe_allow_html=True,
        )
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
