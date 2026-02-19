import streamlit as st
import pandas as pd

# Configuración de página estilo SaaS
st.set_page_config(page_title="Búnker Pro | Tax Management", layout="wide")

# 1. MEMORIA DE SESIÓN (PERSISTENCIA TAXDOME)
if 'cols_visibles' not in st.session_state:
    st.session_state.cols_visibles = ["FECHA_FACTURA", "CUENTA_CONTRA", "NIF", "TOTAL", "ESTADO"]

# --- SIDEBAR MINIMALISTA ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/906/906300.png", width=50) # Un logo pro
    st.title("BÚNKER TAX")
    st.session_state.empresa = st.selectbox("Empresa Activa", ["001 - BÚNKER TAX S.L.", "002 - ALMUDENA FR"])
    st.divider()
    menu = st.radio("PRINCIPAL", ["📋 Pipeline", "📄 Facturas (Libro)", "📂 Documentos", "⚙️ Configuración"])

# --- VISTA: LIBRO DE FACTURAS (ESTILO TAXDOME) ---
if menu == "📄 Facturas (Libro)":
    # Cabecera con Acciones Críticas
    col_t, col_a = st.columns([3, 1])
    with col_t:
        st.title(f"📄 Registro de Facturas")
        st.info(f"📍 Operando en: {st.session_state.empresa}")
    
    with col_a:
        st.write("###")
        if st.button("🔄 Sincronizar Google Drive", use_container_width=True, type="primary"):
            st.toast("Conectando con Drive API...")

    # BARRA DE HERRAMIENTAS (El "Esqueleto" Pro)
    t1, t2, t3 = st.tabs(["🔍 Filtros Rápidos", "🛠️ Configurar Columnas", "📊 Exportar"])
    
    with t1:
        c1, c2, c3 = st.columns(3)
        c1.selectbox("Trimestre", ["1T", "2T", "3T", "4T", "Anual"])
        c2.multiselect("Estado", ["Pendiente", "Revisado", "Contabilizado"], default=["Pendiente"])
        c3.text_input("Buscar por NIF o Cliente...")

    with t2:
        # Aquí están tus 28 campos organizados para activar/desactivar con un clic
        campos_taxdome = [
            "FECHA_FACTURA", "CUENTA_CONTRA", "NIF", "TOTAL", "ESTADO",
            "BI1", "IVA1", "TRIMESTRE", "TIPO_OPERACION", "ID_FACTURA",
            "CATEGORIA", "CUENTA_BASE", "RETENCION_€", "CP_TERCERO"
        ]
        st.session_state.cols_visibles = st.multiselect(
            "Selecciona ventanillas de visualización:",
            options=campos_taxdome,
            default=st.session_state.cols_visibles
        )

    # DATOS (La tabla con estilo profesional)
    # Simulamos la carga real
    data_raw = {col: ["---" for _ in range(10)] for col in campos_taxdome}
    df = pd.DataFrame(data_raw)
    
    # Inyectamos algunos datos para que se vea el "vibe"
    df["ESTADO"] = "Pendiente"
    df["FECHA_FACTURA"] = "19/02/2026"
    df["CUENTA_CONTRA"] = "CLIENTE ESTONIA S.A."
    df["TOTAL"] = "1.500,00 €"

    st.divider()

    # Muestra de la tabla con el orden y selección guardados
    if st.session_state.cols_visibles:
        st.dataframe(
            df[st.session_state.cols_visibles], 
            use_container_width=True, 
            hide_index=True
        )
    else:
        st.warning("Selecciona columnas en 'Configurar Columnas' para ver datos.")

# --- FOOTER ---
st.caption("Búnker Pro v2.0 | Inspirado en estándares TaxDome Estonia")
