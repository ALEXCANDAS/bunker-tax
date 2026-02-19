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

# --- 2. ENTRADA DE FACTURAS ---

elif menu == "📄 Entrada de Facturas":
    st.header(f"📄 Libro de Registro: {empresa_actual}")

    # 1. El Diccionario Maestro (Los 28 campos)
    campos_contables = [
        "FECHA_FACTURA", "CUENTA_CONTRA", "NIF", "TOTAL", "TIPO_OPERACION", "TRIMESTRE",
        "ID_EMPRESA", "FECHA_APUNTE", "ID_FACTURA", "ID_CUENTA_CONTRA", "TIPO_FACTURA",
        "CATEGORIA", "ID_TERCERO", "CP_TERCERO", "BI1", "IVA1", "Cuota_IVA1", "BI2",
        "IVA2", "Cuota_IVA2", "BI3", "IVA3", "Cuota_IVA3", "RETENCION_%", "RETENCION_€",
        "IMPRESO", "ID_CUENTA_BASE", "CUENTA_BASE"
    ]

    # 2. El "Mando a Distancia" (Limpio y en un desplegable)
    with st.expander("⚙️ CONFIGURAR VISTA DEL LIBRO"):
        st.write("Selecciona y ordena las columnas que quieres ver:")
        # Usamos el multiselect que ya conoces, que es el más estable y rápido
        orden_columnas = st.multiselect(
            "Columnas activas (puedes moverlas aquí mismo):",
            options=campos_contables,
            default=["FECHA_FACTURA", "CUENTA_CONTRA", "NIF", "TOTAL"]
        )

    # 3. Lógica de Datos (Simulada)
    data = [{col: "-" for col in campos_contables}]
    data[0].update({"FECHA_FACTURA": "19/02/2026", "CUENTA_CONTRA": "ALMUDENA FR", "TOTAL": "1.250€", "NIF": "ESA1234"})
    df = pd.DataFrame(data)

    st.divider()

    # 4. LA TABLA (Lo que importa)
    if orden_columnas:
        st.dataframe(df[orden_columnas], use_container_width=True, hide_index=True)
    else:
        st.info("Configura las columnas en el menú de arriba para ver los datos.")

    # 5. Botón de éxito (con su espacio correcto)
    if st.button("🚀 Guardar Configuración"):
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
