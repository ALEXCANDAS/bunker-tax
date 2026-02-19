import streamlit as st

# 1. SETUP REACTIVO
if 'total' not in st.session_state: st.session_state.total = 72.97
if 'iva_perc' not in st.session_state: st.session_state.iva_perc = 10

def recalculate():
    st.session_state.base1 = round(st.session_state.total / (1 + (st.session_state.iva_perc / 100)), 2)
    st.session_state.cuota1 = round(st.session_state.total - st.session_state.base1, 2)

if 'base1' not in st.session_state: recalculate()

# --- INTERFAZ ---
st.title("🛡️ Búnker Contable | Validación de Asiento")

with st.container(border=True):
    # FILA 1: CUENTAS DE TRÁFICO Y CABECERA
    c_prov, c_cta_prov, c_tot = st.columns([2, 1, 1])
    
    with c_prov:
        st.text_input("PROVEEDOR", value="RESTAURANTE EL GRIEGO", key="prov")
    
    with c_cta_prov:
        # Cuenta de Tráfico (400/410/210...)
        st.selectbox("CTA. TRÁFICO", ["410.00012", "400.00005", "210.00000", "523.00000"], 
                    help="A3 Vibe: Selecciona la cuenta de acreedor o proveedor.")
    
    with c_tot:
        st.number_input("TOTAL FACTURA", key="total", on_change=recalculate, format="%.2f")

    st.divider()

    # FILA 2: DESGLOSE DE GASTO E IVA
    c_cta_gasto, c_base, c_iva, c_cuota = st.columns([1.5, 1.5, 1, 1])
    
    with c_cta_gasto:
        # Cuenta de Gasto/Ingreso
        st.selectbox("CTA. GASTO", ["629.00000", "600.00000", "623.00000", "210.00000"], 
                    index=0, help="Define la naturaleza del gasto.")
    
    with c_base:
        base_final = st.number_input("BASE IMPONIBLE", key="base1", format="%.2f")
    
    with c_iva:
        st.selectbox("IVA (%)", [21, 10, 4, 0], key="iva_perc", on_change=recalculate, index=1)
    
    with c_cuota:
        cuota_final = round(base_final * (st.session_state.iva_perc / 100), 2)
        st.metric("CUOTA", f"{cuota_final:.2f} €")

    # FILA 3: SUPLIDOS Y CUADRE
    st.write("###")
    suplidos = round(st.session_state.total - (base_final + cuota_final), 2)
    
    c_cta_sup, c_sup_val, c_status = st.columns([1.5, 1.5, 1])
    
    with c_cta_sup:
        st.selectbox("CTA. SUPLIDOS", ["555.00000", "410.00012", "None"], index=0)
    
    with c_sup_val:
        st.number_input("IMPORTE EXENTO/SUPLIDO", value=suplidos, format="%.2f", disabled=True)

    with c_status:
        if abs(suplidos) < 0.01:
            st.success("✅ CUADRADO")
        else:
            st.warning("⚠️ SUPLIDOS")

    # --- BOTÓN DE CIERRE (ENTER) ---
    st.write("###")
    with st.form("registro_final", clear_on_submit=True):
        st.caption("Verifica los 28 campos y pulsa ENTER para exportar al .dat")
        if st.form_submit_button("🚀 CONTABILIZAR Y SIGUIENTE FACTURA", use_container_width=True, type="primary"):
            st.toast("Asiento registrado correctamente.")
