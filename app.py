import streamlit as st

# 1. CAROUSEL HORIZONTAL (Flechas Izquierda/Derecha)
if 'idx_fra' not in st.session_state: st.session_state.idx_fra = 0

cola_facturas = [
    {"img": "https://img_fragmento_1.png", "prov": "EL GRIEGO", "nif": "B123...", "sugerida": "410.00012"},
    {"img": "https://img_fragmento_2.png", "prov": "NUEVO TALLER", "nif": "A999...", "sugerida": "410+"}
]

def navegar(direccion):
    if direccion == "next": st.session_state.idx_fra += 1
    else: st.session_state.idx_fra -= 1

# --- INTERFAZ COMPACTA ---
st.title("🛡️ Búnker Pro | Validación Flash")

# Navegación Superior (Flechas)
c_prev, c_info, c_next = st.columns([1, 3, 1])
if c_prev.button("⬅️ Anterior") and st.session_state.idx_fra > 0: navegar("prev")
c_info.markdown(f"<h3 style='text-align: center;'>Factura {st.session_state.idx_fra + 1} de {len(cola_facturas)}</h3>", unsafe_allow_html=True)
if c_next.button("Siguiente ➡️") and st.session_state.idx_fra < len(cola_facturas)-1: navegar("next")

col_img, col_ficha = st.columns([1, 1])

# IZQUIERDA: Fragmento de imagen (Sin scroll)
with col_img:
    st.subheader("🖼️ Recorte Inteligente")
    st.image("https://via.placeholder.com/500x300?text=Fragmento+Factura+Detectado", use_container_width=True)
    st.caption("Gemini ha centrado la vista en el bloque de importes y NIF.")

# DERECHA: Ficha Blanca con "Alta en Caliente"
with col_ficha:
    f = cola_facturas[st.session_state.idx_fra]
    
    with st.container(border=True):
        # El "Atajo A3" para crear cuentas
        c_cta, c_nif = st.columns([1, 1])
        # Si escribes 410+ aquí, el sistema dispara el alta automática
        cta_input = c_cta.text_input("CTA. TRÁFICO (410+ para crear)", value=f['sugerida'])
        
        if "+" in cta_input:
            st.warning(f"✨ Creando nueva cuenta para: {f['prov']}")
            # Aquí la IA buscaría el último número de la serie en el TSV
            cta_final = "410.00013" 
            st.info(f"Sugerida: {cta_final}")
        
        st.divider()
        
        # TOTAL -> IVA (MEDIO) -> RESULTADO
        t1, t2, t3 = st.columns([1, 0.8, 1])
        total = t1.number_input("TOTAL (€)", value=72.97)
        iva = t2.selectbox("IVA (%)", [21, 10, 4, 0], index=1)
        
        base_calc = total / (1 + (iva/100))
        t3.metric("CUOTA IVA", f"{(total - base_calc):.2f} €")

    # BOTÓN DE GUARDADO (Check & Vanish)
    if st.button("🚀 CONTABILIZAR (ENTER)", type="primary", use_container_width=True):
        st.balloons()
        st.toast("Asiento guardado. La imagen desaparece...")
        # Lógica para eliminar de la cola y pasar al siguiente automáticamente
        if st.session_state.idx_fra < len(cola_facturas)-1:
            st.session_state.idx_fra += 1
            st.rerun()
