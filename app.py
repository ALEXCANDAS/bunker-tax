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

# --- 2. ENTRADA DE FACTURAS ---
elif menu == "📄 Entrada de Facturas":
    st.header("📄 Gestión de Facturas Entrantes")
    
    # Subida
    archivo = st.file_uploader("Subir nueva factura para procesar", type="pdf")
    if archivo:
        st.toast(f"Procesando {archivo.name}...")
    
    st.divider()
    st.subheader("Bandeja de Entrada")
    # Tabla simulada de SaaS
    data = {
        "Fecha": ["19/02", "18/02", "18/02"],
        "Cliente": ["Almudena", "Pedro", "Almudena"],
        "Tipo": ["Op. 03 Francia", "Nacional", "Op. 03 Francia"],
        "Importe": ["1.250€", "450€", "3.100€"],
        "Estado": ["✅ Procesado", "⏳ Pendiente", "✅ Procesado"]
    }
    st.dataframe(data, use_container_width=True)

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
