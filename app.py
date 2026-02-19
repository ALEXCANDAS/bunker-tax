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

    # 1. EL DICCIONARIO DE LAS 28 COLUMNAS (La Base de Datos)
    columnas_totales = [
        "ID_EMPRESA", "FECHA_APUNTE", "FECHA_FACTURA", "TRIMESTRE", "ID_FACTURA", 
        "ID_CUENTA_CONTRA", "CUENTA_CONTRA", "TIPO_FACTURA", "NIF", "CATEGORIA", 
        "ID_TERCERO", "CP_TERCERO", "BI1", "IVA1", "Cuota_IVA1", "BI2", "IVA2", 
        "Cuota_IVA2", "BI3", "IVA3", "Cuota_IVA3", "RETENCION_%", "RETENCION_€", 
        "TOTAL", "TIPO_OPERACION", "IMPRESO", "ID_CUENTA_BASE", "CUENTA_BASE"
    ]

    # 2. EL FILTRO DE LECTURA ÓPTIMA
    with st.expander("🛠️ CONFIGURAR VISTA ÓPTIMA (Selecciona qué columnas ver)", expanded=True):
        col_btn1, col_btn2 = st.columns(2)
        
        # Botones rápidos para no tener que marcar una a una
        if col_btn1.button("👁️ Ver Todo (28 campos)"):
            st.session_state.columnas_ver = columnas_totales
        if col_btn2.button("🧹 Vista Rápida (Esencial)"):
            st.session_state.columnas_ver = ["FECHA_FACTURA", "CUENTA_CONTRA", "NIF", "TOTAL", "TIPO_OPERACION"]

        # El selector múltiple que controla la visibilidad
        columnas_visibles = st.multiselect(
            "Columnas activas:",
            options=columnas_totales,
            default=["FECHA_FACTURA", "CUENTA_CONTRA", "NIF", "TOTAL", "TIPO_OPERACION"],
            key="columnas_ver"
        )

    # 3. LÓGICA DE DATOS (Simulación con los 28 campos)
    # Creamos una fila vacía con todos los campos para que la tabla no de error
    data_pro = {col: ["-" for _ in range(1)] for col in columnas_totales}
    # Rellenamos un ejemplo real
    data_pro["FECHA_FACTURA"][0] = "19/02/2026"
    data_pro["CUENTA_CONTRA"][0] = "ALMUDENA FR"
    data_pro["NIF"][0] = "ESA12345678"
    data_pro["TOTAL"][0] = "1.250,00 €"
    data_pro["TIPO_OPERACION"][0] = "03 FRANCIA"
    data_pro["BI1"][0] = "1.250,00 €"
    data_pro["IVA1"][0] = "0%"

    df_completo = pd.DataFrame(data_pro)

    # 4. LA MÁGIA DE LA LECTURA ÓPTIMA
    if columnas_visibles:
        st.divider()
        st.subheader("📊 Datos del Libro")
        # Solo mostramos lo que has filtrado, pero el resto sigue existiendo por detrás
        st.dataframe(df_completo[columnas_visibles], use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Selecciona al menos una columna para visualizar el libro.")

    st.caption(f"Filtro activo: {len(columnas_visibles)} de 28 columnas mostradas.")

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
