import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración Pro
st.set_page_config(page_title="BUNKER TAX COMMAND", page_icon="🛡️", layout="wide")

# --- BARRA LATERAL (EL MANDO A DISTANCIA) ---
with st.sidebar:
    st.title("🛡️ BÚNKER CONTROL")
    st.divider()
    menu = st.radio(
        "NAVEGACIÓN",
        ["🕹️ Control de Modelos", "📄 Entrada de Facturas", "📅 Calendario Fiscal"]
    )
    st.divider()
    st.success("Estado: Agente Online 🤖")

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

# --- 2. ENTRADA DE FACTURAS (CON FILTRO Y DRIVE) ---
elif menu == "📄 Entrada de Facturas":
    # 1. IDENTIFICADOR DE EMPRESA (Para que sepas dónde estás)
    st.sidebar.markdown("---")
    empresa_actual = st.sidebar.selectbox(
        "🏢 EMPRESA EN USO:",
        ["001 - BÚNKER TAX S.L.", "002 - ALMUDENA FRANCIA", "003 - PEDRO GESTIÓN"]
    )
    st.sidebar.warning(f"Operando en: **{empresa_actual}**")

    st.header(f"📄 Libro de Registro: {empresa_actual}")

    # 2. FILTRO DE VISTA (Para evitar la redundancia)
    col_v1, col_v2 = st.columns([2, 1])
    with col_v1:
        vista = st.multiselect(
            "Seleccionar campos visibles (Limpiar para ver todo):",
            ["FECHA_FACTURA", "CUENTA_CONTRA", "NIF", "TOTAL", "TIPO_OPERACION", "IVA1", "BI1"],
            default=["FECHA_FACTURA", "CUENTA_CONTRA", "TOTAL", "TIPO_OPERACION"]
        )
    
    with col_v2:
        trimestre = st.radio("Trimestre", ["Todos", "1T", "2T", "3T", "4T"], horizontal=True)

    # DATOS (Tus 28 campos están aquí)
    data = [
        {
            "ID_EMPRESA": "001", "FECHA_APUNTE": "19/02/2026", "FECHA_FACTURA": "15/02/2026", 
            "TRIMESTRE": "1T", "ID_FACTURA": "FR-01", "ID_CUENTA_CONTRA": "4000001", 
            "CUENTA_CONTRA": "ALMUDENA FR", "TIPO_FACTURA": "RECIBIDA", "NIF": "ESA12345678", 
            "TOTAL": 1210.00, "BI1": 1000.00, "IVA1": 21, "Cuota_IVA1": 210, 
            "TIPO_OPERACION": "03 FRANCIA", "CUENTA_BASE": "6000001"
            # ... el resto de campos siguen existiendo en el fondo
        }
    ]
    
    df = pd.DataFrame(data)

    # Lógica de visibilidad: Si no hay nada elegido en 'vista', muestra todo.
    # Si hay algo elegido, filtra las columnas.
    if vista:
        df_display = df[vista]
    else:
        df_display = df

    if trimestre != "Todos":
        df_display = df[df['TRIMESTRE'] == trimestre]

    st.divider()
    
    # 3. LA TABLA RESULTANTE
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Botón rápido para exportar (Lo que le gustará a Pedro)
    st.download_button("📥 Descargar este Libro (Excel)", "datos_bunker.csv", "text/csv")

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
