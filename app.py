import streamlit as st

# 1. SETUP DE PANTALLA
st.set_page_config(layout="wide", page_title="Búnker Pro | Mecánica A3")

# 2. INICIALIZACIÓN DE VALORES (Memoria instantánea)
if 'total_fac' not in st.session_state: st.session_state.total_fac = 0.0
if 'base1' not in st.session_state: st.session_state.base1 = 0.0
if 'iva1' not in st.session_state: st.session_state.iva1 = 21

# --- FUNCIONES DE CÁLCULO (La lógica que corre por debajo) ---
def actualizar_desde_total():
    # Al meter el total, proponemos la Base 1 al IVA seleccionado
    st.session_state.base1 = st.session_state.total_fac / (1 + (st.session_state.iva1 / 100))

# --- INTERFAZ DE ALTA VELOCIDAD ---
st.title("🛡️ Mecánica de Registro Reactiva")
st.caption("Escribe el TOTAL y pulsa TAB. La magia ocurre al instante.")

with st.container(border=True):
    # FILA PRINCIPAL: EL DISPARADOR
    col_t, col_iva, col_vacia = st.columns([2, 1, 2])
    
    total_input = col_t.number_input(
        "TOTAL FACTURA", 
        value=st.session_state.total_fac, 
        format="%.2f", 
        key="total_fac", 
        on_change=actualizar_desde_total
    )
    
    tipo_iva1 = col_iva.selectbox(
        "IVA Principal", 
        [21, 10, 4, 0], 
        key="iva1", 
        on_change=actualizar_desde_total
    )

    st.divider()

    # BLOQUE DE BASES REACTIVAS
    # Fila 1: Calculada automáticamente al meter el total
    c1, c2, c3 = st.columns([3, 1, 2])
    b1 = c1.number_input("Base Imponible 1", value=st.session_state.base1, format="%.2f", key="b1_val")
    cuota1 = b1 * (tipo_iva1 / 100)
    c3.metric("Cuota 1", f"{cuota1:.2f} €")

    # Fila 2: El sobrante (Cálculo automático del resto)
    sobrante = total_input - (b1 + cuota1)
    
    c4, c5, c6 = st.columns([3, 1, 2])
    # Aquí la lógica: si hay sobrante, proponemos base al 10% (o lo que quieras)
    b2 = c4.number_input("Base Imponible 2 (Sobrante)", value=sobrante / 1.10 if abs(sobrante) > 0.01 else 0.0, format="%.2f")
    iva2 = c5.selectbox("% IVA 2", [21, 10, 4, 0], index=1)
    cuota2 = b2 * (iva2 / 100)
    c6.metric("Cuota 2", f"{cuota2:.2f} €")

    # Fila Suplidos / Exentos (El cuadre final tipo Contasol)
    sobrante_final = total_input - (b1 + cuota1 + b2 + cuota2)
    
    c7, c8, c9 = st.columns([3, 1, 2])
    exento = c7.number_input("Suplidos / Tasas / Exento", value=sobrante_final if abs(sobrante_final) > 0.01 else 0.0, format="%.2f")
    c8.write("📦 Sin IVA")
    
    # CUADRE DE SEGURIDAD
    diff = total_input - (b1 + cuota1 + b2 + cuota2 + exento)
    if abs(diff) < 0.01:
        c9.success("✅ CUADRADO")
    else:
        c9.error(f"❌ DIF: {diff:.2f} €")

st.button("🚀 CONTABILIZAR Y SIGUIENTE (ENTER)", type="primary", use_container_width=True)
