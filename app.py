import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración Pro
st.set_page_config(page_title="BUNKER TAX COMMAND", page_icon="🛡️", layout="wide")

# --- BARRA LATERAL (SIEMPRE VISIBLE) ---
with st.sidebar:
    st.title("🛡️ BÚNKER CONTROL")
    st.divider()
    
    # 1. MOVEMOS AQUÍ LA EMPRESA PARA QUE NO DÉ ERROR
    empresa_actual = st.selectbox(
        "🏢 EMPRESA EN USO:",
        ["001 - BÚNKER TAX S.L.", "002 - ALMUDENA FRANCIA", "003 - PEDRO GESTIÓN"]
    )
    
    st.divider()
    menu = st.radio(
        "NAVEGACIÓN",
        ["🕹️ Control de Modelos", "📄 Entrada de Facturas", "📅 Calendario Fiscal"]
    )
    st.divider()
    st.success(f"Conectado a: {empresa_actual.split(' - ')[1]}")

# --- 1. PANEL DE CONTROL DE MODELOS ---
if menu == "🕹️ Control de Modelos":
    st.header("🕹️ Panel de Control de Inteligencia")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Configuración")
        modelo = st.selectbox("Seleccionar Cerebro", ["Gemini 1.5 Pro", "Gemini 1.5 Flash", "GPT-4o"])
        temperatura = st.slider("Creatividad (Temperatura)", 0.0, 1.0, 0.1)
        st.toggle("Auto-procesar facturas", value=True)
    
    with col2:
        st.subheader("Estado de los Agentes")
        st.info(f"Modelo actual: **{modelo}** optimizado para lectura de NIFs.")
        st.write("Historial de hoy:")
        st.code("09:30 - Lectura OK - Factura_FR_Almudena.pdf\n10:15 - Lectura OK - Factura_Nac_001.pdf")

# --- 2. ENTRADA DE FACTURAS (LIBRO DE REGISTRO CON FICHAS MOVIBLES) ---
elif menu == "📄 Entrada de Facturas":
    st.header(f"📄 Libro de Registro: {empresa_actual}")
    from streamlit_sortables import sort_items

    # 1. LA LISTA MAESTRA DE 28 CAMPOS
    campos_contables = [
        "ID_EMPRESA", "FECHA_APUNTE", "FECHA_FACTURA", "TRIMESTRE", "ID_FACTURA", 
        "ID_CUENTA_CONTRA", "CUENTA_CONTRA", "TIPO_FACTURA", "NIF", "CATEGORIA", 
        "ID_TERCERO", "CP_TERCERO", "BI1", "IVA1", "Cuota_IVA1", "BI2", "IVA2", 
        "Cuota_IVA2", "BI3", "IVA3", "Cuota_IVA3", "RETENCION_%", "RETENCION_€", 
        "TOTAL", "TIPO_OPERACION", "IMPRESO", "ID_CUENTA_BASE", "CUENTA_BASE"
    ]

    # 2. SELECCIÓN DE CAMPOS (Filtro de lectura óptima)
    st.subheader("🛠️ Configuración de Vista")
    seleccionados = st.multiselect(
        "1. Selecciona los campos que necesitas hoy:",
        options=campos_contables,
        default=["FECHA_FACTURA", "CUENTA_CONTRA", "NIF", "TOTAL", "TIPO_OPERACION"]
    )

    # 3. REORDENACIÓN DE CAMPOS (Fichas movibles)
    if seleccionados:
        st.write("2. Arrastra para ordenar las columnas a tu gusto:")
        orden_final = sort_items(seleccionados, direction="horizontal")
    else:
        orden_final = []
        st.warning("Selecciona al menos un campo arriba.")

    # 4. DATOS (Simulación con los 28 campos para que no falte nada)
    data_pro = {col: ["-" for _ in range(1)] for col in campos_contables}
    data_pro["FECHA_FACTURA"][0] = "19/02/2026"
    data_pro["CUENTA_CONTRA"][0] = "ALMUDENA FR"
    data_pro["TOTAL"][0] = "1.250,00 €"
    data_pro["TIPO_OPERACION"][0] = "03 FRANCIA"
    
    df_completo = pd.DataFrame(data_pro)

    st.divider()

    # 5. VISUALIZACIÓN FINAL
    if orden_final:
        st.dataframe(df_completo[orden_final], use_container_width=True, hide_index=True)
    
    if st.button("🚀 Finalizar Configuración"):
        st.balloons()

# --- 3. CALENDARIO DE REQUERIMIENTOS ---
elif menu == "📅 Calendario Fiscal":
    st.header("📅 Calendario de Requerimientos")
    
    col_cal, col_list = st.columns([2, 1])
    
    with col_cal:
        # Un calendario sencillo
        st.date_input("Próximos Vencimientos", datetime.now())
    
    with col_list:
        st.subheader("Alertas")
        st.error("20 Feb: IVA 4º Trimestre")
        st.warning("25 Feb: Requerimiento Cliente 04")
        st.info("01 Mar: Apertura Modelo 347")
