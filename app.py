import streamlit as st
import pandas as pd

# 1. ARQUITECTURA TAXDOME (Estonia Vibe)
st.set_page_config(layout="wide", page_title="Búnker Pro", initial_sidebar_state="expanded")

# 2. LOS 28 CAMPOS MAESTROS (La base para el .dat)
CAMPOS_DAT = [
    "ID_FACTURA", "FECHA_FACTURA", "NIF", "CUENTA_CONTRA", "TOTAL", 
    "BI1", "IVA1", "CUOTA1", "BI2", "IVA2", "CUOTA2", 
    "BI3", "IVA3", "CUOTA3", "RETENCION_%", "RETENCION_€",
    "TRIMESTRE", "TIPO_OPERACION", "CATEGORIA", "FECHA_APUNTE", 
    "ID_EMPRESA", "TIPO_FACTURA", "ID_TERCERO", "CP_TERCERO", 
    "IMPRESO", "ID_CUENTA_BASE", "CUENTA_BASE", "ESTADO"
]

# 3. MEMORIA DE VISTA (Lo que tú elijes ver)
if 'vision_panel' not in st.session_state:
    # Por defecto, solo lo esencial para trabajar rápido
    st.session_state.vision_panel = ["FECHA_FACTURA", "CUENTA_CONTRA", "NIF", "TOTAL", "ESTADO"]

# --- SIDEBAR: EL FILTRO DE VISIÓN ---
with st.sidebar:
    st.title("🛡️ Búnker Pro")
    st.subheader("🏢 Empresa")
    empresa = st.selectbox("Seleccionar Sociedad", ["001 - BÚNKER TAX S.L.", "002 - ALMUDENA FR"])
    
    st.divider()
    st.subheader("🛠️ FILTRO DE PANEL")
    st.write("Configura tu lectura óptima (el resto se guarda para el .dat):")
    
    # El filtro que separa la visión de la base de datos
    st.session_state.vision_panel = st.multiselect(
        "Columnas activas en panel:",
        options=CAMPOS_DAT,
        default=st.session_state.vision_panel
    )
    
    st.divider()
    if st.button("🔄 SYNC DRIVE", type="primary", use_container_width=True):
        st.success("Sincronizando...")

# --- CUERPO: PANTALLA DE OPERACIONES ---
st.title("📄 Libro de Registro")

tab_asientos, tab_export = st.tabs(["📝 PANEL DE TRABAJO", "📥 EXPORTACIÓN .DAT"])

with tab_asientos:
    # Creamos un DataFrame con los 28 campos vacíos (el .dat completo)
    # Pero en el panel solo inyectamos lo que tú has filtrado
    df_maestro = pd.DataFrame([{c: "" for c in CAMPOS_DAT} for _ in range(10)])
    
    # Datos de ejemplo
    df_maestro.at[0, "FECHA_FACTURA"] = "19/02/2026"
    df_maestro.at[0, "CUENTA_CONTRA"] = "ALMUDENA FR"
    df_maestro.at[0, "TOTAL"] = "1.250,00"
    df_maestro.at[0, "ESTADO"] = "⚡ Pendiente"

    st.write(f"### Mostrando {len(st.session_state.vision_panel)} de 28 campos")
    
    # EL EDITOR: Tú solo ves y tocas lo que has filtrado
    st.data_editor(
        df_maestro[st.session_state.vision_panel],
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        key="editor_pro"
    )

with tab_export:
    st.subheader("Generador de archivos para Hacienda")
    st.write("Aquí el sistema utiliza los 28 campos ocultos para generar el fichero oficial.")
    if st.button("📦 Generar .dat"):
        st.info("Procesando los 28 campos para el formato oficial...")

# --- FOOTER ---
st.divider()
st.caption("Búnker Pro v2.0 | Estonia SaaS Framework | Filtro de Lectura Óptima Activo")
