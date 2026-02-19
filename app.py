import streamlit as st

# 1. ESTADO DE SESIÓN
if 'indice' not in st.session_state:
    st.session_state.indice = 0

cola = [
    {"empresa": "ALMUDENA FR", "nif": "FR12345678", "total": 1210.00, "iva": 21},
    {"empresa": "GESTIÓN BCN", "nif": "B66778899", "total": 450.00, "iva": 21},
    {"empresa": "TRADING LON", "nif": "GB99887766", "total": 2100.00, "iva": 0},
]

def procesar_asiento():
    # Esta función se dispara al dar al botón O al pulsar ENTER
    if st.session_state.indice < len(cola) - 1:
        st.session_state.indice += 1
    else:
        st.success("🎯 ¡Cola terminada!")

# --- INTERFAZ ---
st.title("🚀 Validación Ultra-Rápida")

if st.session_state.indice < len(cola):
    factura = cola[st.session_state.indice]
    
    col_izq, col_der = st.columns([1, 2])
    
    with col_izq:
        st.markdown(f"### 📬 Siguiente factura\n**{factura['empresa']}**")
        st.caption(f"Registro {st.session_state.indice + 1} de {len(cola)}")

    with col_der:
        # EL TRUCO: Todo dentro de un form para capturar el ENTER
        with st.form("ficha_blanca", clear_on_submit=False):
            st.subheader(f"Ficha: {factura['empresa']}")
            
            # Campos de edición
            nif = st.text_input("NIF", value=factura['nif'])
            total = st.number_input("TOTAL FACTURA (€)", value=factura['total'])
            tipo_iva = st.selectbox("IVA %", [21, 10, 4, 0])
            
            # Cálculos automáticos visibles
            bi = total / (1 + (tipo_iva/100))
            st.write(f"**BI calculada:** {bi:.2f} € | **Cuota:** {(total-bi):.2f} €")
            
            st.divider()
            
            # El botón de "submit" es el que captura el ENTER
            submit = st.form_submit_button("✅ CONTABILIZAR (PULSA ENTER)", 
                                         on_click=procesar_asiento,
                                         use_container_width=True,
                                         type="primary")
else:
    st.balloons()
    st.header("✅ ¡Todo contabilizado!")
    if st.button("Reiniciar cola"):
        st.session_state.indice = 0
        st.rerun()
