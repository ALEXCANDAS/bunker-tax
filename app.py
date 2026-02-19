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

# --- 2. ENTRADA DE FACTURAS (LIBRO DE REGISTRO CON FICHAS MOVIBLES) ---
elif menu == "📄 Entrada de Facturas":
    # Identificador de Empresa en la parte superior
    st.header(f"📄 Libro de Registro: {empresa_actual}")
    
    st.info("💡 CONSEJO ANTIGRAVITY: El orden en que selecciones las fichas será el orden de las columnas en la tabla.")

    # EL TRUCO DE LAS FICHAS MOVIBLES:
    # La lista de abajo son todas tus columnas. 
    # Si pinchas primero 'TOTAL' y luego 'NIF', aparecerán en ese orden.
    fichas_disponibles = [
        "ID_FACTURA", "FECHA_FACTURA", "CUENTA_CONTRA", "NIF", "TOTAL", 
        "TIPO_OPERACION", "TRIMESTRE", "BI1", "IVA1", "Cuota_IVA1", 
        "CATEGORIA", "CUENTA_BASE", "CP_TERCERO"
    ]
    
    fichas_seleccionadas = st.multiselect(
        "Configura tu panel (añade y ordena tus fichas):",
        options=fichas_disponibles,
        default=["ID_FACTURA", "FECHA_FACTURA", "CUENTA_CONTRA", "TOTAL"]
    )

    # Datos de ejemplo (Asegúrate de que los nombres coincidan con las fichas)
    data = [
        {
            "ID_FACTURA": "FR-01", "FECHA_FACTURA": "15/02/2026", 
            "CUENTA_CONTRA": "ALMUDENA FR", "NIF": "ESA12345678", 
            "TOTAL": 1210.00, "TIPO_OPERACION": "03 FRANCIA", 
            "TRIMESTRE": "1T", "BI1": 1000.00, "IVA1": 21, 
            "Cuota_IVA1": 210, "CATEGORIA": "COMPRAS", 
            "CUENTA_BASE": "6000001", "CP_TERCERO": "75001"
        }
    ]
    
    df = pd.DataFrame(data)

    # LA MAGIA: Si hay fichas elegidas, filtramos y REORDENAMOS el dataframe
    if fichas_seleccionadas:
        df_display = df[fichas_seleccionadas]
    else:
        # Si borras todas, por defecto te enseña estas 3 para no quedarse en blanco
        df_display = df[["ID_FACTURA", "CUENTA_CONTRA", "TOTAL"]]

    st.divider()
    
    # Dibujamos la tabla con el orden de fichas que hayas elegido
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Tu botón de Drive para mañana
    st.button("🔄 Sincronizar con Google Drive")

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
