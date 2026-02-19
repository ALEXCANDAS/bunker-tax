import streamlit as st

# Configuración de alta densidad
st.set_page_config(layout="wide", page_title="Búnker Pro | Alta Velocidad")

if 'idx' not in st.session_state: st.session_state.idx = 0

# Simulación de factura detectada por Gemini
factura = {"empresa": "SUMINISTROS INDUSTRIALES S.A.", "total_detectado": 1500.00}

st.title("🛡️ Entrada de Asientos Inteligente")

with st.form("ficha_contasol", clear_on_submit=True):
    # --- CABECERA: TOTAL Y CUADRE ---
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.subheader(f"🏢 {factura['empresa']}")
    with c2:
        total_fac = st.number_input("TOTAL FACTURA", value=factura['total_detectado'], format="%.2f", step=0.01)
    
    st.divider()

    # --- LÓGICA DE 3 BASES + EXENTO (AUTOCALCULABLE) ---
    # Fila 1 (La que propone el sistema por defecto al entrar)
    col1, col2, col3 = st.columns([3, 1, 2])
    base1 = col1.number_input("Base Imponible 1", value=total_fac/1.21, step=0.01, help="Pulsa TAB para saltar")
    iva1 = col2.selectbox("% IVA 1", [21, 10, 4, 0], index=0, key="i1")
    cuota1 = base1 * (iva1/100)
    col3.metric("Cuota 1", f"{cuota1:.2f} €")

    # Fila 2 (Se activa si el asesor modifica la Base 1)
    sobrante_2 = total_fac - (base1 + cuota1)
    col4, col5, col6 = st.columns([3, 1, 2])
    base2 = col4.number_input("Base Imponible 2", value=sobrante_2/1.10 if sobrante_2 > 0 else 0.0, step=0.01)
    iva2 = col5.selectbox("% IVA 2", [21, 10, 4, 0], index=1, key="i2")
    cuota2 = base2 * (iva2/100)
    col6.metric("Cuota 2", f"{cuota2:.2f} €")

    # Fila 3
    sobrante_3 = total_fac - (base1 + cuota1 + base2 + cuota2)
    col7, col8, col9 = st.columns([3, 1, 2])
    base3 = col7.number_input("Base Imponible 3", value=sobrante_3/1.04 if sobrante_3 > 0 else 0.0, step=0.01)
    iva3 = col8.selectbox("% IVA 3", [21, 10, 4, 0], index=2, key="i3")
    cuota3 = base3 * (iva3/100)
    col9.metric("Cuota 3", f"{cuota3:.2f} €")

    # --- APARTADO EXENTO / SUPLIDOS (TIPO CONTASOL) ---
    st.markdown("---")
    sobrante_final = total_fac - (base1 + cuota1 + base2 + cuota2 + base3 + cuota3)
    
    ce1, ce2, ce3 = st.columns([3, 1, 2])
    exento = ce1.number_input("Exento / Suplidos / Tasas", value=sobrante_final if sobrante_final > 0 else 0.0)
    tipo_exento = ce2.selectbox("Concepto", ["Suplido", "Tasa", "Seguro", "Otros"])
    
    # CUADRE FINAL (Debe ser 0.00 para que el asesor esté tranquilo)
    diferencia = total_fac - (base1 + cuota1 + base2 + cuota2 + base3 + cuota3 + exento)
    with ce3:
        if abs(diferencia) < 0.01:
            st.success(f"✅ CUADRADO")
        else:
            st.error(f"❌ DIF: {diferencia:.2f} €")

    # BOTÓN DE ACCIÓN
    st.form_submit_button("💾 CONTABILIZAR ASIENTO (ENTER)", use_container_width=True, type="primary")

st.caption("⌨️ **Instrucciones:** Al modificar una Base, el sistema recalcula automáticamente el resto para cuadrar con el TOTAL.")
