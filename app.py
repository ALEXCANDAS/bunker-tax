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
    st.header("📄 Libro de Registro de Facturas")
    
    # Barra de herramientas superior
    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    with col_f1:
        busqueda = st.text_input("🔍 Buscar por NIF, Tercero o ID...", "")
    with col_f2:
        trimestre_filtro = st.selectbox("Filtrar Trimestre", ["Todos", "1T", "2T", "3T", "4T"])
    with col_f3:
        st.write("###")
        st.button("🔄 Sincronizar Drive")

    # ESTRUCTURA PROFESIONAL (Tus 28 columnas)
    # He creado un ejemplo real para Almudena
    data = [
        {
            "ID_EMPRESA": "001", "FECHA_APUNTE": "19/02/2026", "FECHA_FACTURA": "15/02/2026", 
            "TRIMESTRE": "1T", "ID_FACTURA": "FR-2026-01", "ID_CUENTA_CONTRA": "4000001", 
            "CUENTA_CONTRA": "ALMUDENA FR", "TIPO_FACTURA": "RECIBIDA", "NIF": "ESA12345678", 
            "CATEGORIA": "COMPRAS", "ID_TERCERO": "T001", "CP_TERCERO": "75001", 
            "BI1": 1000.00, "IVA1": 0, "Cuota_IVA1": 0, "BI2": 0, "IVA2": 0, "Cuota_IVA2": 0, 
            "BI3": 0, "IVA3": 0, "Cuota_IVA3": 0, "RETENCION_%": 0, "RETENCION_€": 0, 
            "TOTAL": 1000.00, "TIPO_OPERACION": "03 FRANCIA", "IMPRESO": "NO", 
            "ID_CUENTA_BASE": "6000001", "CUENTA_BASE": "COMPRAS MERCADERIAS"
        },
        {
            "ID_EMPRESA": "001", "FECHA_APUNTE": "18/02/2026", "FECHA_FACTURA": "10/02/2026", 
            "TRIMESTRE": "1T", "ID_FACTURA": "ESP-999", "ID_CUENTA_CONTRA": "4000002", 
            "CUENTA_CONTRA": "PROVEEDOR ESP", "TIPO_FACTURA": "RECIBIDA", "NIF": "B87654321", 
            "CATEGORIA": "SUMINISTROS", "ID_TERCERO": "T002", "CP_TERCERO": "28001", 
            "BI1": 100.00, "IVA1": 21, "Cuota_IVA1": 21, "BI2": 0, "IVA2": 0, "Cuota_IVA2": 0, 
            "BI3": 0, "IVA3": 0, "Cuota_IVA3": 0, "RETENCION_%": 0, "RETENCION_€": 0, 
            "TOTAL": 121.00, "TIPO_OPERACION": "NACIONAL", "IMPRESO": "NO", 
            "ID_CUENTA_BASE": "6280000", "CUENTA_BASE": "SUMINISTROS"
        }
    ]
    
    df = pd.DataFrame(data)

    # Lógica de filtros
    if busqueda:
        df = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]
    if trimestre_filtro != "Todos":
        df = df[df['TRIMESTRE'] == trimestre_filtro]

    st.divider()
    
    # Mostrar la tabla con scroll horizontal automático
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.caption(f"Mostrando {len(df)} registros del libro de facturas.")

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
