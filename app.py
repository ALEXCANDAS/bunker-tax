import streamlit as st

# 1. SETUP DE PANTALLA
st.set_page_config(layout="wide", page_title="Búnker Pro | Producción")

# 2. COLUMNA LATERAL (EL MOTOR DE MOVIMIENTO)
with st.sidebar:
    st.title("📥 Cola de Drive")
    st.caption("Próximos recortes...")
    # Miniaturas que se mueven hacia arriba conforme contabilizas
    st.image("https://via.placeholder.com/200x100?text=Importe+Recorte+1", caption="Factura #1")
    st.image("https://via.placeholder.com/200x100?text=Importe+Recorte+2", caption="Factura #2")
    st.divider()
    if st.button("🔍 Cambiar a ETAPA DE REVISIÓN", use_container_width=True):
        st.session_state.etapa = "revision"

# 3. CUERPO CENTRAL (LA FICHA DE ACCIÓN)
st.subheader("🚀 Etapa: Contabilización Flash")

col_img, col_val = st.columns([1.2, 1])

with col_img:
    # Recorte enfocado actual
    st.markdown("### 🖼️ Fragmento Actual")
    st.image("https://via.placeholder.com/600x250?text=Fragmento+Factura+Actual+Focus", use_container_width=True)

with col_val:
    with st.container(border=True):
        # ATAJO A3: 410+
        cta = st.text_input("CTA. TRÁFICO (410+ para crear)", value="410.00012")
        
        # EL NÚCLEO: TOTAL -> IVA (CENTRO) -> RESULTADO
        t1, t2, t3 = st.columns([1, 0.8, 1])
        total = t1.number_input("TOTAL (€)", value=72.97)
        iva = t2.selectbox("IVA (%)", [21, 10, 4, 0], index=1) # Auto-detectado 10%
        
        base_calc = total / (1 + (iva/100))
        t3.metric("CUOTA IVA", f"{(total - base_calc):.2f} €")

    # BOTÓN DE ACCIÓN (Check & Vanish)
    if st.button("🚀 GUARDAR Y SIGUIENTE (ENTER)", type="primary", use_container_width=True):
        st.toast("Asiento contabilizado. Cargando siguiente del sidebar...")
        # Lógica para desplazar la cola del sidebar
