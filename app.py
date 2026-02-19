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
    st.header("📄 Gestión de Facturas")
    
    # Simulación de conexión a Drive
    st.sidebar.divider()
    drive_status = st.sidebar.status("Conexión Drive: Activa ✅")
    drive_status.write("Carpeta: /BunkerTax/Facturas_2024")
    
    col_f1, col_f2 = st.columns([2, 1])
    
    with col_f1:
        # EL BUSCADOR QUE PEDÍAS
        cliente_buscado = st.text_input("🔍 Filtrar por nombre de cliente o NIF", "")
        
    with col_f2:
        st.write("###")
        if st.button("🔄 Sincronizar Drive"):
            st.toast("Buscando nuevas facturas en Google Drive...")

    # Datos simulados con más clientes
    data = [
        {"Fecha": "19/02", "Cliente": "Almudena", "Tipo": "Op. 03 Francia", "Importe": "1.250€", "Link": "Ver en Drive 📁"},
        {"Fecha": "18/02", "Cliente": "Pedro", "Tipo": "Nacional", "Importe": "450€", "Link": "Ver en Drive 📁"},
        {"Fecha": "17/02", "Cliente": "García S.L.", "Tipo": "Nacional", "Importe": "890€", "Link": "Ver en Drive 📁"},
        {"Fecha": "16/02", "Cliente": "Almudena", "Tipo": "Op. 03 Francia", "Importe": "500€", "Link": "Ver en Drive 📁"}
    ]
    
    df = pd.DataFrame(data)

    # Lógica del filtro
    if cliente_buscado:
        df_filtrado = df[df['Cliente'].str.contains(cliente_buscado, case=False)]
    else:
        df_filtrado = df

    st.divider()
    st.subheader(f"Facturas en el Búnker ({len(df_filtrado)})")
    st.dataframe(df_filtrado, use_container_width=True)

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
