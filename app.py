import streamlit as st

# 1. FORZAR ANCHO COMPLETO Y ELIMINAR MÁRGENES
st.set_page_config(layout="wide", page_title="Búnker Pro | UltraWide Mode")

st.markdown("""
    <style>
    /* Eliminar el padding excesivo de Streamlit */
    .block-container { padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; }
    /* Hacer que los contenedores ocupen todo el espacio */
    [data-testid="stVerticalBlock"] > div:has(div.stFrame) { width: 100% !important; }
    .stMetric { background: #f1f5f9; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

# 2. ESTRUCTURA DE PANTALLA DUAL (50/50 Real)
col_pdf, col_datos = st.columns([1, 1], gap="small")

# --- COLUMNA IZQUIERDA: EL DOCUMENTO (Sin espacios muertos) ---
with col_pdf:
    st.markdown("### 📄 Documento Fuente (Drive)")
    # El visor de PDF ahora ocupa todo el alto disponible
    st.markdown("""
        <iframe src="https://www.africau.edu/images/default/sample.pdf" 
        width="100%" height="850px" style="border:1px solid #ccc; border-radius:8px;"></iframe>
    """, unsafe_allow_html=True)

# --- COLUMNA DERECHA: LA FICHA BLANCA EXPANDIDA ---
with col_datos:
    st.markdown("### 📝 Validación de Asiento: Producción Real")
    
    with st.container(border=True):
        # FILA 1: IDENTIFICACIÓN (Ocupando todo el ancho)
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.text_input("🏢 PROVEEDOR / ACREEDOR", value="RESTAURANTE EL GRIEGO S.L.")
        c2.text_input("🆔 NIF", value="B12345678")
        # Atajo A3: 410+
        c3.text_input("🔢 CTA. TRÁFICO (410+)", value="410.00012")

        st.divider()

        # FILA 2: EL NÚCLEO (IVA en el centro, campos grandes)
        f1, f2, f3 = st.columns([1, 1, 1])
        total = f1.number_input("💰 TOTAL FACTURA (€)", value=72.97, format="%.2f")
        # IVA Centralizado para no desvirtuar el pensamiento
        iva_perc = f2.selectbox("📊 IVA (%)", [21, 10, 4, 0], index=1)
        
        base_sugerida = round(total / (1 + (iva_perc/100)), 2)
        cuota_sugerida = round(total - base_sugerida, 2)
        f3.metric("📈 CUOTA IVA", f"{cuota_sugerida} €")

        # FILA 3: CUENTAS DE GASTO Y BASES (Alineación perfecta)
        g1, g2, g3 = st.columns([1.5, 1.5, 1])
        g1.text_input("📂 CTA. GASTO / INGRESO", value="629.00000")
        base_final = g2.number_input("📝 BASE IMPONIBLE", value=base_sugerida)
        
        # Suplidos automáticos para cuadre (Contasol Style)
        dif = round(total - (base_final + (base_final * (iva_perc/100))), 2)
        with g3:
            if abs(dif) < 0.01: st.success("✅ CUADRADO")
            else: st.error(f"⚠️ DIF: {dif} €")

        # FILA 4: SUPLIDOS (Solo aparece si se necesita, pero no desperdicia espacio)
        if abs(dif) > 0.01:
            s1, s2 = st.columns([2, 2])
            s1.text_input("📎 CTA. SUPLIDOS", value="555.00000")
            s2.number_input("💶 IMPORTE EXENTO", value=dif, disabled=True)

    # BOTÓN "+" DINÁMICO (Para multi-IVA sin romper el layout)
    st.button("➕ Añadir otra Base / IVA / Retención", use_container_width=True)

    st.write("###")
    # EL BOTÓN DE ENVÍO (Grande y claro para el ENTER)
    with st.form("contabilizar_final", clear_on_submit=True):
        if st.form_submit_button("🚀 CONTABILIZAR Y SIGUIENTE (PULSA ENTER)", 
                                 use_container_width=True, type="primary"):
            st.toast("Asiento exportado al TSV de A3")
