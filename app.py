import streamlit as st

# 1. MEMORIA DE SESIÓN (Para no perder el hilo)
if 'index' not in st.session_state:
    st.session_state.index = 0

# Simulación de lo que Gemini ha leído de tu Drive
cola_facturas = [
    {"empresa": "ALMUDENA FR", "nif": "FR12345678", "total": 1210.0, "iva": 21, "bandera": "🇫🇷"},
    {"empresa": "GESTIÓN BCN", "nif": "B66778899", "total": 450.0, "iva": 21, "bandera": "🇪🇸"},
    {"empresa": "TRADING LON", "nif": "GB99887766", "total": 2100.0, "iva": 0, "bandera": "🇬🇧"},
]

def sig_factura():
    if st.session_state.index < len(cola_facturas) - 1:
        st.session_state.index += 1
    else:
        st.session_state.finalizado = True

# --- INTERFAZ ---
st.title("🚀 Validación Ultra-Rápida")

if 'finalizado' not in st.session_state:
    f = cola_facturas[st.session_state.index]
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 15px; border-left: 10px solid #000;">
                <span style="font-size: 40px;">{f['bandera']}</span><br>
                <b>{f['empresa']}</b><br>
                <small>Pendiente de validar</small>
            </div>
        """, unsafe_allow_html=True)
        st.write(f"📊 Factura {st.session_state.index + 1} de {len(cola_facturas)}")

    with col_b:
        # EL SECRETO: 'st.form' captura el ENTER del teclado automáticamente
        with st.form("ficha_trabajo", clear_on_submit=True):
            st.subheader("📝 Ficha Blanca de Edición")
            
            # Los campos que Gemini ya ha pre-rellenado
            nif_input = st.text_input("NIF (Validar)", value=f['nif'])
            total_input = st.number_input("TOTAL FACTURA (€)", value=f['total'])
            iva_input = st.selectbox("IVA %", [21, 10, 4, 0], index=0 if f['iva'] == 21 else 3)
            
            # Cálculo tipo A3 en tiempo real (informativo)
            bi = total_input / (1 + (iva_input/100))
            st.info(f"Base: {bi:.2f}€ | Cuota: {(total_input-bi):.2f}€")
            
            st.write("---")
            
            # El botón de 'Submit' es el que se activa con el ENTER
            enviar = st.form_submit_button("✅ CONTABILIZAR Y SIGUIENTE (PULSA ENTER)", 
                                         on_click=sig_factura, 
                                         use_container_width=True, 
                                         type="primary")

else:
    st.balloons()
    st.success("🎉 ¡Todas las facturas han sido contabilizadas!")
    if st.button("Reiniciar cola de trabajo"):
        del st.session_state.finalizado
        st.session_state.index = 0
        st.rerun()
