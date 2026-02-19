import streamlit as st

st.set_page_config(layout="wide", page_title="Búnker Pro | Exact Flow")

# CSS para máxima densidad y f.lux friendly
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .stNumberInput input { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

col_pdf, col_ficha = st.columns([1.1, 1])

with col_pdf:
    st.markdown('<iframe src="https://www.africau.edu/images/default/sample.pdf" width="100%" height="800px" style="border-radius:10px;"></iframe>', unsafe_allow_html=True)

with col_ficha:
    with st.container(border=True):
        # --- BLOQUE 1: IDENTIFICACIÓN (ARRIBA) ---
        st.markdown("### 🏢 Datos Identificativos")
        id_c1, id_c2, id_c3 = st.columns([2, 1, 1])
        prov = id_c1.text_input("PROVEEDOR", value="RESTAURANTE EL GRIEGO")
        nif = id_c2.text_input("NIF", value="B12345678")
        cta_traf = id_c3.text_input("CTA. TRÁFICO (410+)", value="410.00012")

        st.divider()

        # --- BLOQUE 2: NATURALEZA (CENTRO) ---
        st.markdown("### ⚙️ Configuración del Gasto")
        op_c1, op_c2, op_c3 = st.columns([1, 1, 1])
        tipo_op = op_c1.selectbox("TIPO OPERACIÓN", ["Gasto Corriente", "Bien Inversión", "Suplido"])
        cat_gasto = op_c2.text_input("CATEGORÍA", value="Comidas / Representación")
        cta_gasto = op_c3.text_input("CTA. GASTO", value="629.00000")

        st.divider()

        # --- BLOQUE 3: CUADRE ECONÓMICO (IVA EDITABLE) ---
        st.markdown("### 💰 Importes y Cuadre")
        
        # Fila de Base e IVA
        eco_c1, eco_c2, eco_c3 = st.columns([1.2, 0.8, 1])
        base = eco_c1.number_input("BASE IMPONIBLE", value=66.34, format="%.2f")
        iva_p = eco_c2.selectbox("IVA (%)", [21, 10, 4, 0], index=1)
        
        # LA CUOTA EDITABLE (Para corregir el céntimo de Exact)
        cuota_sugerida = round(base * (iva_p / 100), 2)
        cuota_final = eco_c3.number_input("CUOTA IVA (Editable)", value=cuota_sugerida, format="%.2f", step=0.01)

        # Referencia y Total final
        ref_c1, tot_c1 = st.columns([1, 1])
        ref_c1.text_input("Nº FACTURA / REF", value="FRA-2024-001")
        total_real = tot_c1.number_input("💵 TOTAL FACTURA (€)", value=72.97, format="%.2f")

        # Verificador de cuadre con lógica de Suplidos
        diferencia = round(total_real - (base + cuota_final), 2)
        
        if abs(diferencia) < 0.01:
            st.success("✅ ASIENTO CUADRADO")
        else:
            st.warning(f"⚠️ DIFERENCIA: {diferencia} € (Se llevará a Suplidos)")
            st.text_input("CTA. SUPLIDOS", value="555.00000")

    # BOTÓN DE ACCIÓN FINAL
    with st.form("contabilizar"):
        if st.form_submit_button("🚀 CONTABILIZAR Y SIGUIENTE (ENTER)", use_container_width=True, type="primary"):
            st.toast("Exportando a TSV compatible con A3...")
