import streamlit as st

# 1. CONFIGURACIÓN DE PANTALLA (Pensado para tu LG con f.lux)
st.set_page_config(layout="wide", page_title="Búnker Pro | Visión Real")

# Estilo para que el PDF se vea grande y la ficha sea limpia
st.markdown("""
    <style>
    .pdf-frame { height: 85vh; border: 1px solid #4a4d50; border-radius: 10px; }
    .stMetric { background: #f8fafc; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE DETECCIÓN (IA Semántica)
def sugerir_iva(proveedor):
    if "RESTAURANTE" in proveedor.upper(): return 10
    return 21

# Simulamos carga de metadatos desde Drive
prov_detectado = "RESTAURANTE EL GRIEGO"
iva_sugerido = sugerir_iva(prov_detectado)

# --- INTERFAZ DUAL ---
col_pdf, col_ficha = st.columns([1.2, 1])

# IZQUIERDA: LA IMAGEN DE LA FACTURA (Visión real)
with col_pdf:
    st.subheader("📁 Factura_Restaurante.pdf")
    # Aquí cargamos el PDF real de tu Drive
    st.markdown(f'<iframe src="https://www.africau.edu/images/default/sample.pdf" class="pdf-frame" width="100%"></iframe>', unsafe_allow_html=True)

# DERECHA: LA FICHA (IVA en el medio para no desvirtuar el pensamiento)
with col_ficha:
    st.subheader("📝 Validación de Asiento")
    
    with st.container(border=True):
        # FILA MAESTRA: El flujo que el humano espera
        c_prov, c_cta = st.columns([2, 1])
        c_prov.text_input("PROVEEDOR", value=prov_detectado)
        c_cta.text_input("CTA. TRÁFICO", value="410.00012")

        st.divider()
        
        # EL NÚCLEO: Total -> IVA (Medio) -> Resultado
        f1, f2, f3 = st.columns([1, 0.8, 1])
        
        total = f1.number_input("TOTAL FACTURA (€)", value=72.97, format="%.2f")
        
        # El IVA en el centro, propuesto por la IA
        iva_val = f2.selectbox("IVA (%)", [21, 10, 4, 0], 
                              index=[21, 10, 4, 0].index(iva_sugerido))
        
        # La cuota y base se muestran como resultado final del flujo
        base_calc = round(total / (1 + (iva_val/100)), 2)
        cuota_calc = round(total - base_calc, 2)
        f3.metric("CUOTA IVA", f"{cuota_calc} €")

        # FILA DE CUENTAS DE GASTO
        st.write("###")
        g1, g2 = st.columns([1, 1])
        g1.text_input("CTA. GASTO", value="629.00000")
        base_final = g2.number_input("BASE IMPONIBLE", value=base_calc)

        # SECCIÓN DE SUPLIDOS (Solo si hay descuadre)
        dif = round(total - (base_final + (base_final * (iva_val/100))), 2)
        if abs(dif) > 0.01:
            st.warning(f"Diferencia detectada: {dif} €")
            st.text_input("CTA. SUPLIDOS (Opcional)", placeholder="555.0...")

    # BOTÓN "+" PARA BASES EXTRAS (Por si la IA detecta facturas mixtas)
    if st.button("➕ Añadir Línea (IVA Mixto / Suplido)"):
        st.info("Añadiendo nueva base de cálculo...")

    st.write("###")
    # BOTÓN DE ACCIÓN FINAL
    with st.form("contabilizar"):
        if st.form_submit_button("🚀 GUARDAR EN TSV Y SIGUIENTE (ENTER)", use_container_width=True, type="primary"):
            st.toast("Asiento cuadrado y exportado.")
