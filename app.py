import streamlit as st

st.set_page_config(layout="wide", page_title="Búnker Pro | Final Edition")

# CSS para que nada "salte" ni se mueva
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .stNumberInput, .stTextInput { margin-bottom: -15px; }
    hr { margin-top: 1rem; margin-bottom: 1rem; }
    </style>
    """, unsafe_allow_html=True)

col_pdf, col_ficha = st.columns([1.2, 1])

with col_pdf:
    # El PDF ocupa su sitio y no se mueve
    st.markdown('<iframe src="https://www.africau.edu/images/default/sample.pdf" width="100%" height="820px" style="border-radius:10px;"></iframe>', unsafe_allow_html=True)

with col_ficha:
    with st.container(border=True):
        # --- BLOQUE 1: IDENTIFICACIÓN (LIMPIO) ---
        st.markdown("### 🏢 Identificación")
        id_c1, id_c2, id_c3 = st.columns([2, 1, 1])
        prov = id_c1.text_input("PROVEEDOR", value="RESTAURANTE EL GRIEGO")
        nif = id_c2.text_input("NIF", value="B12345678")
        cta_traf = id_c3.text_input("CTA. TRÁFICO", value="410.00012", help="Escribe + para nueva")

        st.divider()

        # --- BLOQUE 2: CONFIGURACIÓN (CENTRO) ---
        st.markdown("### ⚙️ Configuración")
        op_c1, op_c2, op_c3 = st.columns([1, 1, 1])
        tipo_op = op_c1.selectbox("OPERACIÓN", ["Gasto Corriente", "Bienes Inv."], label_visibility="collapsed")
        cat_gasto = op_c2.text_input("CATEGORÍA", value="Comidas", label_visibility="collapsed")
        cta_gasto = op_c3.text_input("CTA. GASTO", value="629.00000", label_visibility="collapsed")

        st.divider()

        # --- BLOQUE 3: CUADRE (EL NÚCLEO) ---
        st.markdown("### 💰 Importes")
        
        # Fila Base e IVA (IVA SIEMPRE EN EL MEDIO)
        eco_c1, eco_c2, eco_c3 = st.columns([1.2, 0.8, 1])
        base = eco_c1.number_input("BASE IMPONIBLE", value=66.34, format="%.2f")
        iva_p = eco_c2.selectbox("IVA (%)", [21, 10, 4, 0], index=1)
        # Cuota editable para el céntimo puñetero
        cuota = eco_c3.number_input("CUOTA IVA", value=6.63, format="%.2f")

        # Aquí es donde la IA inyectaría la segunda base si existiera (sin mover lo de arriba)
        # st.session_state.lineas_extra... 
        
        st.write("###")
        # REFERENCIA Y TOTAL (EL CIERRE)
        ref_c1, tot_c1 = st.columns([1, 1])
        ref_c1.text_input("Nº FACTURA / REF", value="FRA-2024-001")
        total_real = tot_c1.number_input("💵 TOTAL FACTURA (€)", value=72.97, format="%.2f")

    # --- BOTONERA DE CONTROL (FUERA DEL CONTENEDOR PARA QUE NO MUEVA NADA) ---
    c_plus, c_save = st.columns([0.5, 2])
    # El signo + para añadir complejidad solo si el humano/IA lo pide
    c_plus.button("➕", help="Añadir Base Extra o Suplido")
    
    with c_save:
        with st.form("validar"):
            if st.form_submit_button("🚀 CONTABILIZAR (ENTER)", use_container_width=True, type="primary"):
                st.success("Enviado al TSV")

    # Si hay descuadre, aparece abajo del todo, como un log, sin joder la ficha
    dif = round(total_real - (base + cuota), 2)
    if abs(dif) > 0.01:
        st.caption(f"⚠️ Nota: Descuadre de {dif}€ detectado. Se gestionará como suplido en el asiento.")
