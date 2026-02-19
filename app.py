import streamlit as st

# 1. SETUP DE PANTALLA ULTRA-WIDE
st.set_page_config(layout="wide", page_title="Búnker Pro | Final Build")

# CSS para congelar la estética y evitar que los campos "bailen"
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .stNumberInput, .stTextInput, .stSelectbox { margin-bottom: -10px; }
    /* Evitar que el botón + mueva el formulario */
    .stButton>button { margin-top: 0px; }
    hr { margin-top: 0.8rem; margin-bottom: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

col_pdf, col_ficha = st.columns([1.1, 1])

with col_pdf:
    # Visor estático del PDF
    st.markdown('<iframe src="https://www.africau.edu/images/default/sample.pdf" width="100%" height="850px" style="border-radius:10px; border: 1px solid #d1d5db;"></iframe>', unsafe_allow_html=True)

with col_ficha:
    with st.container(border=True):
        # --- BLOQUE 1: IDENTIFICACIÓN (FIJO ARRIBA) ---
        st.markdown("### 🏢 Identificación")
        r1_c1, r1_c2, r1_c3 = st.columns([2, 1, 1])
        prov = r1_c1.text_input("PROVEEDOR", value="RESTAURANTE EL GRIEGO")
        nif = r1_c2.text_input("NIF", value="B12345678")
        cta_traf = r1_c3.text_input("CTA. TRÁFICO", value="410.00012")

        st.divider()

        # --- BLOQUE 2: CONFIGURACIÓN Y GASTO (CENTRO) ---
        st.markdown("### ⚙️ Configuración del Gasto")
        r2_c1, r2_c2, r2_c3 = st.columns([1, 1, 1])
        tipo_op = r2_c1.selectbox("OPERACIÓN", ["Gasto Corriente", "Bien Inversión"])
        cat_gasto = r2_c2.text_input("CATEGORÍA", value="Comidas")
        cta_gasto = r2_c3.text_input("CTA. GASTO", value="629.00000")

        st.divider()

        # --- BLOQUE 3: IMPORTES (EL NÚCLEO) ---
        st.markdown("### 💰 Importes")
        
        # Fila económica: Base -> IVA (Medio) -> Cuota (Editable)
        r3_c1, r3_c2, r3_c3 = st.columns([1.2, 0.8, 1])
        base = r3_c1.number_input("BASE IMPONIBLE", value=66.34, format="%.2f")
        iva_p = r3_c2.selectbox("IVA (%)", [21, 10, 4, 0], index=1)
        # Cuota editable para corregir el céntimo sin que nada se rompa
        cuota = r3_c3.number_input("CUOTA IVA (Editable)", value=6.63, format="%.2f", step=0.01)

        # Referencia y Total final (Cierre del asiento)
        r4_c1, r4_c2 = st.columns([1, 1])
        ref = r4_c1.text_input("Nº FACTURA / REF", value="FRA-2024-001")
        total_real = r4_c2.number_input("💵 TOTAL FACTURA (€)", value=72.97, format="%.2f")

    # --- BOTONERA DE CONTROL ---
    # El botón + se queda en su esquina para no desplazar el diseño
    c_plus, c_spacer, c_save = st.columns([0.2, 1.3, 2.5])
    c_plus.button("➕", help="Añadir línea extra de IVA o Suplido")
    
    with c_save:
        # Formulario para capturar el ENTER y limpiar para la siguiente
        with st.form("registro_final", clear_on_submit=True):
            if st.form_submit_button("🚀 CONTABILIZAR Y SIGUIENTE (ENTER)", use_container_width=True, type="primary"):
                st.toast("Exportando a TSV compatible con A3...")

    # Notificación de descuadre discreta (abajo del todo para no mover campos)
    dif = round(total_real - (base + cuota), 2)
    if abs(dif) > 0.01:
        st.caption(f"⚠️ Nota: Descuadre de {dif}€ detectado. Se enviará a cuenta de Suplidos por defecto.")
