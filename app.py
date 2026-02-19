import streamlit as st

# 1. SIDEBAR ANCLADO (LA COLA DE TRABAJO)
with st.sidebar:
    st.title("📂 Cola de Drive")
    # Miniaturas de lo que viene para que no pierdas el contexto
    st.info("Siguiente: GASOLINERA CEPSA\nTotal: 50.00€")
    st.divider()
    st.caption("Contabilizadas hoy: 14")

# 2. CUERPO CENTRAL: LA FICHA QUE NO PIERDE NADA
st.subheader("📝 Validación de Asiento: Producción Real")

col_img, col_ficha = st.columns([1.2, 1])

with col_img:
    # EL RECORTE DE LA FACTURA (Donde ves el nombre y los datos reales)
    st.markdown("### 🖼️ Fragmento de Factura")
    st.image("https://via.placeholder.com/600x400?text=NOMBRE+PROVEEDOR+Y+DATOS+FISCALES", use_container_width=True)
    st.caption("Pincha en la imagen para ampliar si el recorte se queda corto.")

with col_ficha:
    # --- IDENTIFICACIÓN TOTAL (Lo que no podemos perder) ---
    with st.container(border=True):
        st.markdown("#### 🏢 Identificación")
        c1, c2 = st.columns([2, 1])
        # Nombre y NIF siempre a la vista
        prov_nombre = c1.text_input("PROVEEDOR / ACREEDOR", value="RESTAURANTE EL GRIEGO S.L.")
        prov_nif = c2.text_input("NIF", value="B12345678")
        
        # EL ATAJO A3: 410+ / 400+
        cta_trafico = st.text_input("CTA. TRÁFICO (Escribe 410+ para crear)", value="410.00012")
        
        st.divider()

        # --- EL NÚCLEO CONTABLE (IVA EN EL MEDIO) ---
        st.markdown("#### 💰 Desglose Económico")
        f1, f2, f3 = st.columns([1, 0.8, 1])
        
        total_fra = f1.number_input("TOTAL FRA. (€)", value=72.97, format="%.2f")
        # El cerebro no se desvirtúa: El IVA en el centro
        iva_tipo = f2.selectbox("IVA (%)", [21, 10, 4, 0], index=1) 
        
        # Resultados calculados al vuelo
        base_sugerida = round(total_fra / (1 + (iva_tipo/100)), 2)
        cuota_sugerida = round(total_fra - base_sugerida, 2)
        f3.metric("CUOTA IVA", f"{cuota_sugerida} €")

        # --- GASTO Y SUPLIDOS (La estructura de fondo) ---
        g1, g2 = st.columns([1.2, 1])
        cta_gasto = g1.text_input("CTA. GASTO / INGRESO", value="629.00000")
        base_real = g2.number_input("BASE IMPONIBLE", value=base_sugerida)

        # CÁLCULO DE SUPLIDOS (El apartado Contasol que no se olvida)
        diferencia = round(total_fra - (base_real + (base_real * (iva_tipo/100))), 2)
        if abs(diferencia) > 0.01:
            st.warning(f"⚠️ Suplido/Exento: {diferencia} €")
            st.text_input("CTA. SUPLIDOS", value="555.00000")

    # BOTÓN "+" PARA MULTI-IVA (Flexibilidad moderna)
    st.button("➕ Añadir otra Base / IVA")

    st.write("###")
    # ENVÍO FINAL
    if st.button("🚀 CONTABILIZAR Y SIGUIENTE (ENTER)", type="primary", use_container_width=True):
        st.toast("Guardando en TSV...")
