import streamlit as st

# 1. SETUP
st.set_page_config(layout="wide", page_title="Búnker Pro | IA Predictiva")

# 2. BASE DE DATOS DE PATRONES (Parametrización por Proveedor/Empresa)
# Esto es lo que Gemini actualizará solo al detectar patrones
if 'patrones' not in st.session_state:
    st.session_state.patrones = {
        "RESTAURANTE EL GRIEGO": {"iva_def": 10, "exento_frecuente": False},
        "SUMINISTROS SL": {"iva_def": 21, "exento_frecuente": True},
        "DESCONOCIDO": {"iva_def": 21, "exento_frecuente": False}
    }

if 'total_fac' not in st.session_state: st.session_state.total_fac = 0.0

# --- LÓGICA DE PREDICCIÓN ---
def calcular_propuesta():
    proveedor = st.session_state.get('prov_actual', 'DESCONOCIDO')
    config = st.session_state.patrones.get(proveedor, st.session_state.patrones["DESCONOCIDO"])
    
    # Asignamos el IVA según patrón
    iva_prio = config["iva_def"]
    st.session_state.iva1 = iva_prio
    
    # Calculamos base 1 por defecto
    st.session_state.base1 = st.session_state.total_fac / (1 + (iva_prio / 100))

# --- INTERFAZ REACTIVA ---
st.title("🛡️ Registro con IA y Parametrización")

with st.container(border=True):
    c_prov, c_tot, c_iva_p = st.columns([2, 1, 1])
    
    # Al cambiar el proveedor, la IA ya sabe qué IVA poner
    proveedor = c_prov.selectbox("PROVEEDOR (IA Detect)", 
                               options=list(st.session_state.patrones.keys()),
                               key="prov_actual",
                               on_change=calcular_propuesta)
    
    total = c_tot.number_input("TOTAL FACTURA", 
                             value=st.session_state.total_fac, 
                             key="total_fac", 
                             on_change=calcular_propuesta)
    
    iva_master = c_iva_p.selectbox("IVA Patrón", [21, 10, 4, 0], key="iva1", on_change=calcular_propuesta)

    st.divider()

    # BLOQUE DE BASES DINÁMICAS
    col_b1, col_met1 = st.columns([3, 2])
    b1 = col_b1.number_input("Base Imponible 1", value=st.session_state.get('base1', 0.0), format="%.2f")
    cuota1 = b1 * (iva_master / 100)
    col_met1.metric("Cuota 1", f"{cuota1:.2f} €")

    # CÁLCULO DE DIFERENCIAS (Para Base 2 o Exento)
    restante = total - (b1 + cuota1)
    
    col_b2, col_iva2, col_met2 = st.columns([3, 1, 2])
    # Si queda dinero, la IA propone la siguiente base lógica (ej. al 4%)
    b2 = col_b2.number_input("Base Imponible 2 (Sobrante)", value=restante/1.04 if restante > 0 else 0.0)
    iva2 = col_iva2.selectbox("% IVA 2", [21, 10, 4, 0], index=2)
    cuota2 = b2 * (iva2 / 100)
    col_met2.metric("Cuota 2", f"{cuota2:.2f} €")

    # APARTADO EXENTO (Contasol Style)
    restante_final = total - (b1 + cuota1 + b2 + cuota2)
    col_ex, col_txt = st.columns([3, 3])
    exento = col_ex.number_input("Suplidos / Exento", value=restante_final if restante_final > 0 else 0.0)
    
    # CUADRE FINAL
    diff = total - (b1 + cuota1 + b2 + cuota2 + exento)
    if abs(diff) < 0.01:
        st.success("✅ ASIENTO CUADRADO")
    else:
        st.error(f"❌ DIFERENCIA: {diff:.2f} €")

st.button("🚀 CONTABILIZAR (ENTER)", type="primary", use_container_width=True)
