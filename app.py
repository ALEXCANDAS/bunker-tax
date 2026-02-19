import streamlit as st
import pandas as pd

# 1. ESTADO DE SESIÓN (La memoria del SaaS)
if 'db' not in st.session_state:
    # Simulamos una base de datos ya cargada con los 28 campos
    st.session_state.db = pd.DataFrame(columns=[
        "FECHA", "NIF", "CLIENTE", "TOTAL", "BI", "IVA", "ESTADO", "TRIMESTRE", "OPERACION"
    ])
if 'cols_active' not in st.session_state:
    st.session_state.cols_active = ["FECHA", "CLIENTE", "TOTAL", "ESTADO"]

# --- UI CONFIGURATION (El Esqueleto) ---
st.set_page_config(layout="wide", page_title="Búnker Tax Pro")

# --- BARRA SUPERIOR DE ACCIONES (Donde todos fallan, aquí acertamos) ---
col_t, col_a = st.columns([2, 1])
with col_t:
    st.title("🛡️ Búnker Control Center")
    st.caption(f"Gestión inteligente de asientos para: **{st.session_state.get('empresa', 'Empresa Demo')}**")

with col_a:
    st.write("###")
    c_btn1, c_btn2 = st.columns(2)
    c_btn1.button("🔄 Sync Drive", type="primary", use_container_width=True)
    if c_btn2.button("➕ Nuevo Asiento", use_container_width=True):
        st.toast("Abriendo entrada rápida...")

# --- PANEL DINÁMICO (El corazón del sistema) ---
tab1, tab2, tab3 = st.tabs(["📋 Libro de Registro", "⚙️ Configuración de Panel", "📊 Análisis"])

with tab2:
    st.subheader("🛠️ Personalización de Ventanillas")
    # Esto es lo que permite que el panel sea DINÁMICO al instante
    all_fields = ["FECHA", "NIF", "CLIENTE", "TOTAL", "BI", "IVA", "ESTADO", "TRIMESTRE", "OPERACION"]
    st.session_state.cols_active = st.multiselect(
        "Elige qué columnas quieres en tu lectura óptima:",
        options=all_fields,
        default=st.session_state.cols_active
    )

with tab1:
    # Datos de ejemplo para que veas el "Vibe"
    data = [
        {"FECHA": "19/02/2026", "NIF": "B12345678", "CLIENTE": "Almudena FR", "TOTAL": 1210.00, "BI": 1000, "IVA": 210, "ESTADO": "Pendiente", "TRIMESTRE": "1T", "OPERACION": "01 Interior"},
        {"FECHA": "20/02/2026", "NIF": "A87654321", "CLIENTE": "Estonia SaaS", "TOTAL": 500.00, "BI": 500, "IVA": 0, "ESTADO": "Revisado", "TRIMESTRE": "1T", "OPERACION": "03 UE"}
    ]
    df_display = pd.DataFrame(data)

    # LA TABLA DINÁMICA (Editable para que la introducción sea como Excel)
    st.data_editor(
        df_display[st.session_state.cols_active],
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic", # ¡ESTO permite añadir asientos rápido!
        key="editor_asientos"
    )

# --- FOOTER ---
st.divider()
st.info("💡 Consejo Antigravity: Puedes editar directamente sobre la tabla para una introducción de asientos ultra-rápida.")
