import streamlit as st

# 1. DEFINICIÓN GLOBAL DE PESTAÑAS (Evita el NameError)
tab_recibidas, tab_emitidas, tab_registro = st.tabs([
    "📥 RECIBIDAS", 
    "📤 EMITIDAS", 
    "📋 REGISTRO Y BANDERAS"
])

# 2. PANEL DE REGISTRO CON FILTROS (Segmentación Total)
with tab_registro:
    st.markdown("### 🔍 Centro de Auditoría")
    
    # Filtros de segmentación (NIF, Trimestre, Modelos)
    f_col1, f_col2, f_col3, f_col4 = st.columns([1, 1, 1, 2])
    f_trimestre = f_col1.selectbox("TRIMESTRE", ["1T", "2T", "3T", "4T"])
    f_modelo = f_col2.selectbox("MODELO", ["303", "111", "347", "190"])
    f_tipo = f_col3.selectbox("TIPO", ["Emitidas", "Recibidas"])
    f_busqueda = f_col4.text_input("BUSCAR POR NIF O NOMBRE", placeholder="Ej: B12345678")

    st.divider()

    # Tabla Maestra con Banderas
    # Aquí es donde verás visualmente si falta el 111 o si el 347 está activo
    st.markdown("""
        | Estado | Fecha | Sujeto / NIF | Total | Banderas | Acción |
        | :--- | :--- | :--- | :--- | :--- | :--- |
        | ✅ | 19/02/2026 | BAR PLAZA | 15,00€ | 🟦 303 | 👁️ |
        | ✅ | 19/02/2026 | ABOGADOS SL | 242,00€ | 🟦 303 🟧 111 | 👁️ |
        | ⚠️ | 15/02/2026 | CLIENTE SL | 1.210,00€ | 🟦 303 🟪 347 | 👁️ |
    """)
