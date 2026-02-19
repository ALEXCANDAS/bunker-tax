import streamlit as st

if 'idx' not in st.session_state: st.session_state.idx = 0

# Simulación: Factura con dos bases (Metadatos de Gemini)
cola = [
    {"empresa": "DISTRIBUIDORA ALIMENTOS", "nif": "B12345678", "total": 150.00, "b1": 100.0, "i1": 10, "b2": 50.0, "i2": 4},
    {"empresa": "SUMINISTROS PRO", "nif": "A87654321", "total": 121.00, "b1": 100.0, "i1": 21, "b2": 0.0, "i2": 0},
]

def siguiente():
    if st.session_state.idx < len(cola) - 1:
        st.session_state.idx += 1
    else:
        st.success("✅ ¡Cola terminada!")

st.title("🚀 Registro Multi-Base Alta Velocidad")

if st.session_state.idx < len(cola):
    f = cola[st.session_state.idx]
    
    with st.form("multi_base_form", clear_on_submit=True):
        # CABECERA GOLPE DE OJO
        c1, c2, c3 = st.columns([2,1,1])
        c1.subheader(f"🏢 {f['empresa']}")
        total_real = c2.number_input("TOTAL FACTURA", value=f['total'], format="%.2f")
        c3.metric("Diferencia", f"{total_real - (f['b1']*(1+f['i1']/100) + f['b2']*(1+f['i2']/100)):.2f} €")

        st.divider()

        # BLOQUE DE BASES (Configurables y Tabulables)
        # Base 1
        col1, col2, col3 = st.columns([3, 1, 2])
        b1 = col1.number_input("Base Imponible 1", value=f['b1'])
        i1 = col2.selectbox("% IVA 1", [21, 10, 4, 0], index=1 if f['i1']==10 else 0)
        col3.write(f"Cuota: {b1 * (i1/100):.2f} €")

        # Base 2
        col4, col5, col6 = st.columns([3, 1, 2])
        b2 = col4.number_input("Base Imponible 2", value=f['b2'])
        i2 = col5.selectbox("% IVA 2", [21, 10, 4, 0], index=2 if f['i2']==4 else 3)
        col6.write(f"Cuota: {b2 * (i2/100):.2f} €")
        
        # Base 3 (Opcional, siempre ahí pero no estorba)
        col7, col8, col9 = st.columns([3, 1, 2])
        b3 = col7.number_input("Base Imponible 3", value=0.0)
        i3 = col8.selectbox("% IVA 3", [21, 10, 4, 0], index=3)
        col9.write(f"Cuota: 0.00 €")

        st.divider()
        
        # BOTÓN QUE CAPTURA EL ENTER
        # Al terminar de picar la B2, un Tab más te lleva aquí y Enter salta de factura.
        st.form_submit_button("✅ VALIDAR Y SIGUIENTE (ENTER)", on_click=siguiente, type="primary", use_container_width=True)

st.caption("⌨️ **Truco Asesor:** Usa `Tab` para saltar entre bases. Si la factura solo tiene una base, pulsa `Tab` rápido hasta llegar al botón y dale a `Enter`.")
