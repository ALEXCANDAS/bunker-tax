import streamlit as st
import pandas as pd

# 1. EL "ADN" DEL BÚNKER (Las 28 columnas reales)
CAMPOS_28 = [
    "ID_FACTURA", "FECHA_FACTURA", "NIF", "CUENTA_CONTRA", "TOTAL", 
    "BI1", "IVA1", "Cuota_IVA1", "BI2", "IVA2", "Cuota_IVA2", 
    "BI3", "IVA3", "Cuota_IVA3", "RETENCION_%", "RETENCION_€",
    "TRIMESTRE", "TIPO_OPERACION", "CATEGORIA", "FECHA_APUNTE", 
    "ID_EMPRESA", "TIPO_FACTURA", "ID_TERCERO", "CP_TERCERO", 
    "IMPRESO", "ID_CUENTA_BASE", "CUENTA_BASE", "ESTADO"
]

# 2. MEMORIA ANTIGRAVITY (Para no repetir trabajo)
if 'cols_vistas' not in st.session_state:
    st.session_state.cols_vistas = ["FECHA_FACTURA", "CUENTA_CONTRA", "NIF", "TOTAL", "ESTADO"]

# --- CONFIGURACIÓN DE PANTALLA ---
st.set_page_config(layout="wide", page_title="Búnker Tax Engine")

# --- HEADER PROFESIONAL ---
c1, c2 = st.columns([3, 1])
with c1:
    st.title("📄 Libros de Registro | TaxDome Standard")
    st.caption(f"📍 Empresa: {st.session_state.get('empresa_actual', 'BÚNKER TAX S.L.')}")
with c2:
    st.write("###")
    st.button("🔄 Sincronizar Google Drive", type="primary", use_container_width=True)

# --- EL PANEL DE MANDOS (Tabs de alta velocidad) ---
tab_libro, tab_config, tab_pipeline = st.tabs(["📋 LIBRO DE REGISTRO", "⚙️ CONFIGURACIÓN DE VISTA", "🚀 PIPELINE"])

with tab_config:
    st.subheader("🛠️ Personalizar Ventanillas de Lectura")
    # Aquí tienes las 28 para elegir, pero sin que se rompa nada
    st.session_state.cols_vistas = st.multiselect(
        "Selecciona las columnas para tu pantalla de trabajo:",
        options=CAMPOS_28,
        default=st.session_state.cols_vistas
    )
    st.info("💡 El orden en que las selecciones será el orden de la tabla.")

with tab_libro:
    # 3. EL MOTOR DE INTRODUCCIÓN RÁPIDA (Donde no fallamos)
    # Creamos un DataFrame vacío pero con los 28 campos
    data_pro = {col: ["---"] for col in CAMPOS_28}
    # Ejemplo real
    data_pro["FECHA_FACTURA"] = ["19/02/2026"]
    data_pro["CUENTA_CONTRA"] = ["ALMUDENA FRANCIA"]
    data_pro["TOTAL"] = ["1.250,00 €"]
    data_pro["ESTADO"] = ["Pendiente"]
    
    df = pd.DataFrame(data_pro)

    # LA TABLA EDITABLE (Estilo Excel/TaxDome)
    # Solo mostramos las que has elegido, pero puedes editar los datos
    st.data_editor(
        df[st.session_state.cols_vistas],
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic", # Permite añadir filas dándole al "+"
        key="asientos_pro"
    )

with tab_pipeline:
    st.subheader("🏁 Estado del Trimestre")
    col1, col2, col3 = st.columns(3)
    col1.metric("Pendientes", "14", "2 nuevas")
    col2.metric("Revisadas", "45", "10%")
    col3.metric("Contabilizadas", "120", "OK")

# --- FOOTER ---
st.divider()
st.caption("Búnker Tax v2.0 | Estonia SaaS Framework | Desarrollado con Vibe Coding")
