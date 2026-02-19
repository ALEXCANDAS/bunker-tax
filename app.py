import streamlit as st

# 1. CONFIGURACIÓN ULTRA-WIDE
st.set_page_config(layout="wide", page_title="Búnker Pro | Flujo Optimizado")

# Estilos para eliminar márgenes y mejorar la densidad visual
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    .stMetric { background: #f8fafc; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0; }
    div[data-testid="column"] { padding: 0px 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. INTERFAZ DUAL (PDF Izquierda | Ficha Derecha)
col_pdf, col_ficha = st.columns([1.2, 1])

with col_pdf:
    st.subheader("📄 Documento Fuente")
    # Visor de PDF que ocupa el alto de la pantalla
    st.markdown('<iframe src="https://www.africau.edu/images/default/sample.pdf" width="100%" height="800vh" style="border-radius:10px;"></iframe>', unsafe_allow_html=True)

with col_ficha:
    st.subheader("📝 Registro de Asiento")
    
    with st.container(border=True):
        # --- BLOQUE SUPERIOR: IDENTIFICACIÓN Y CATEGORÍA ---
        st.markdown("##### 🏢 Identificación y Naturaleza")
        r1_c1, r1_c2 = st.columns([2, 1])
        r1_c1.text_input("PROVEEDOR / ACREEDOR", value="RESTAURANTE EL GRIEGO", key="prov")
        # Atajo A3: 410+
        r1_c2.text_input("CTA. TRÁFICO (410+)", value="410.00012", key="cta_traf")
        
        r2_c1, r2_c2, r2_c3 = st.columns([1, 1, 1])
        r2_c1.selectbox("TIPO OPERACIÓN", ["Gasto Corriente", "Bienes de Inversión", "Suplido"])
        r2_c2.text_input("CATEGORÍA GASTO", value="Representación / Comidas")
        r2_c3.text_input("NIF", value="B12345678")

        st.divider()

        # --- BLOQUE CENTRAL: EL GASTO (Referencia arriba) ---
        st.markdown("##### 📂 Imputación del Gasto")
        r3_c1, r3_c2 = st.columns([1, 1])
        r3_c1.text_input("CUENTA DE GASTO", value="629.00000")
        r3_c2.text_input("Nº FACTURA / REFERENCIA", placeholder="Ej: FRA-2024-001")

        st.divider()

        # --- BLOQUE INFERIOR: TOTALES (Total Abajo como disparador final) ---
        st.markdown("##### 💰 Liquidación Económica")
        
        # Fila de Base e IVA (IVA en el medio)
        base_col, iva_col, cuota_col = st.columns([1.2, 0.8, 1])
        # Al meter el Total abajo, estos campos se recalculan
        base_val = base_col.number_input("BASE IMPONIBLE", value=66.34, format="%.2f")
        iva_perc = iva_col.selectbox("IVA (%)", [21, 10, 4, 0], index=1)
        
        cuota_calc = round(base_val * (iva_perc / 100), 2)
        cuota_col.metric("CUOTA IVA", f"{cuota_calc} €")

        # EL TOTAL ABAJO (Punto final antes de contabilizar)
        st.write("###")
        total_fra = st.number_input("💵 TOTAL FACTURA (€)", value=72.97, format="%.2f", 
                                    help="Este es el valor final de cuadre.")

        # Verificador de Cuadre
        dif = round(total_fra - (base_val + cuota_calc), 2)
        if abs(dif) < 0.01:
            st.success("✅ ASIENTO CUADRADO")
        else:
            st.error(f"⚠️ DESCUADRE: {dif} € (Revisa Bases o Suplidos)")

    # BOTONES DE ACCIÓN
    st.button("➕ Añadir Línea (IVA Mixto / Retención)", use_container_width=True)
    
    with st.form("finalizar"):
        if st.form_submit_button("🚀 CONTABILIZAR Y SIGUIENTE (ENTER)", use_container_width=True, type="primary"):
            st.toast("Exportando a TSV compatible con A3...")
