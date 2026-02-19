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
    # --- CABECERA ESTILO SAAS ---
    c_tit1, c_tit2 = st.columns([3, 1])
    with c_tit1:
        st.title("📄 Libro de Registro")
        st.caption(f"Visualizando datos en tiempo real para: **{empresa_actual}**")
    with c_tit2:
        st.write("###")
        st.button("🔄 Sincronizar Drive", use_container_width=True)

    # --- ZONA DE CONFIGURACIÓN (Ventanillas estilo Excel Pro) ---
    with st.expander("🛠️ CONFIGURAR PANTALLA DE LECTURA", expanded=False):
        # Aquí definimos la "matriz" de tus 28 campos de forma ultra-organizada
        bloques = {
            "IDENTIFICACIÓN": ["ID_FACTURA", "FECHA_FACTURA", "TRIMESTRE", "TIPO_OPERACION", "FECHA_APUNTE", "ID_EMPRESA"],
            "TERCERO": ["NIF", "CUENTA_CONTRA", "ID_TERCERO", "CP_TERCERO", "ID_CUENTA_CONTRA", "CATEGORIA"],
            "IMPORTES (B1)": ["BI1", "IVA1", "Cuota_IVA1", "TOTAL"],
            "IMPORTES (B2/B3)": ["BI2", "IVA2", "Cuota_IVA2", "BI3", "IVA3", "Cuota_IVA3"],
            "IMPUESTOS/OTROS": ["RETENCION_%", "RETENCION_€", "IMPRESO", "ID_CUENTA_BASE", "CUENTA_BASE"]
        }
        
        cols_ui = st.columns(len(bloques))
        seleccion_final = []

        for i, (nombre_bloque, campos) in enumerate(bloques.items()):
            with cols_ui[i]:
                st.markdown(f"**{nombre_bloque}**")
                for campo in campos:
                    # Definimos cuáles vienen marcadas por defecto para no perder tiempo
                    default_val = campo in ["FECHA_FACTURA", "CUENTA_CONTRA", "NIF", "TOTAL", "TRIMESTRE"]
                    if st.checkbox(campo, value=default_val, key=f"chk_{campo}"):
                        seleccion_final.append(campo)

    # --- MOTOR DE DATOS ---
    # Simulamos la carga de tus 28 campos
    data_saas = {col: ["---"] for col in seleccion_final}
    if "TOTAL" in seleccion_final: data_saas["TOTAL"] = ["1.250,00 €"]
    if "CUENTA_CONTRA" in seleccion_final: data_saas["CUENTA_CONTRA"] = ["ALMUDENA FR"]
    
    df_saas = pd.DataFrame(data_saas)

    # --- EL LIBRO (Limpio y Profesional) ---
    st.divider()
    if seleccion_final:
        st.dataframe(
            df_saas, 
            use_container_width=True, 
            hide_index=True,
            column_config={col: st.column_config.TextColumn(col.replace("_", " ")) for col in seleccion_final}
        )
    else:
        st.info("Utiliza el configurador superior para activar las ventanillas de datos.")

    st.success(f"Vista optimizada con {len(seleccion_final)} campos activos.")
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
