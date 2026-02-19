import streamlit as st

# 1. MEMORIA REACTIVA (Para que los cálculos fluyan al momento)
if 'total' not in st.session_state: st.session_state.total = 72.97
if 'iva_perc' not in st.session_state: st.session_state.iva_perc = 10

# Función de cálculo instantáneo
def recalculate():
    # Cuando cambia el total o el IVA, calculamos la base 1
    st.session_state.base1 = round(st.session_state.total / (1 + (st.session_state.iva_perc / 100)), 2)
    st.session_state.cuota1 = round(st.session_state.total - st.session_state.base1, 2)

# Ejecutamos el cálculo inicial si no existe
if 'base1' not in st.session_state: recalculate()

# --- INTERFAZ ---
st.title("🛡️ Búnker Speed-Entry")
st.caption("Conexión total: Cambia el importe y mira cómo bailan las bases.")

with st.container(border=True):
    # FILA MAESTRA (Conectada)
    c_nom, c_tot, c_iva = st.columns([2, 1, 1])
    
    with c_nom:
        st.text_input("PROVEEDOR", value="RESTAURANTE EL GRIEGO", key="prov")
    
    with c_tot:
        # Al cambiar este número, se dispara 'recalculate'
        st.number_input("TOTAL FACTURA", key="total", on_change=recalculate, format="%.2f")
    
    with c_iva:
        # Al cambiar el IVA, también se dispara 'recalculate'
        st.selectbox("IVA (%)", [21, 10, 4, 0], key="iva_perc", on_change=recalculate, index=1)

    st.divider()

    # BLOQUE DE TRABAJO (Aquí ves el resultado al instante)
    col_b, col_c, col_s = st.columns([2, 1, 1])
    
    # Base editable (por si quieres ajustarla manualmente)
    base_final = col_b.number_input("BASE IMPONIBLE (Deducible)", key="base1", format="%.2f")
    
    # Cuota calculada al vuelo sobre la base que haya en pantalla
    cuota_final = round(base_final * (st.session_state.iva_perc / 100), 2)
    col_c.metric("CUOTA IVA", f"{cuota_final:.2f} €")
    
    # SUPLIDOS: La diferencia real para que cuadre el TOTAL
    suplidos = round(st.session_state.total - (base_final + cuota_final), 2)
    
    with col_s:
        if abs(suplidos) < 0.01:
            st.success("✅ CUADRADO")
        else:
            st.warning(f"Suplidos: {suplidos:.2f} €")

    st.write("###")
    
    # TRUCO PARA EL INTRO: 
    # En Streamlit, un botón fuera de un form no captura el Enter de texto, 
    # pero podemos usar un pequeño 'formulario de una sola línea' para el envío final.
    with st.form("envio", clear_on_submit=True):
        st.caption("Pulsa ENTER aquí para contabilizar")
        if st.form_submit_button("🚀 CONTABILIZAR ASIENTO", use_container_width=True, type="primary"):
            st.toast("Guardado en el .dat")
            # Aquí pondrías la lógica para cargar la siguiente factura de Drive
