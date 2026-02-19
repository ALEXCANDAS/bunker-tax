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
    
    # Importamos la pieza que acabas de añadir en requirements
    from streamlit_sortables import sort_items

    st.subheader("🛠️ Configurador de Panel")
    st.write("Arrastra las fichas para cambiar el orden de las columnas:")

    # Lista de tus campos profesionales
    columnas_base = [
        "FECHA_FACTURA", "CUENTA_CONTRA", "TOTAL", 
        "NIF", "TIPO_OPERACION", "TRIMESTRE"
    ]

    # ESTA ES LA MAGIA: Aparecerán cajitas que se mueven con el ratón
    orden_fichas = sort_items(columnas_base, direction="horizontal")

    # Datos de prueba
    data = [{
        "FECHA_FACTURA": "15/02/2026", "CUENTA_CONTRA": "ALMUDENA FR", 
        "TOTAL": 1210.00, "NIF": "ESA12345678", 
        "TIPO_OPERACION": "03 FRANCIA", "TRIMESTRE": "1T"
    }]
    df = pd.DataFrame(data)

    st.divider()

    # La tabla se ordena sola según dejes las fichas arriba
    st.dataframe(df[orden_fichas], use_container_width=True, hide_index=True)
    # Tu botón de Drive para mañana
    if st.button("🚀 Finalizar Configuración"):
        st.balloons()
        st.success("¡Estructura de hoy guardada con éxito, Alejandro!")

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
