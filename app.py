import streamlit as st

# 1. SETUP DE PANTALLA (Layout Odoo)
st.set_page_config(layout="wide", page_title="Búnker Pro | Validación Dual")

# Estilo para la barra lateral y las fichas
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #f8fafc; min-width: 350px; }
    .stButton>button { border-radius: 5px; }
    .factura-card {
        padding: 10px; border: 1px solid #e2e8f0; border-radius: 8px;
        margin-bottom: 10px; background: white; cursor: pointer;
    }
    .factura-card:hover { border-color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# 2. SIMULACIÓN DE COLA DESDE DRIVE
if 'facturas_drive' not in st.session_state:
    st.session_state.facturas_drive = [
        {"id": "001", "file": "Factura_Griego.pdf", "prov": "RESTAURANTE EL GRIEGO", "total": 72.97, "iva": 10},
        {"id": "002", "file": "Suministros_Feb.pdf", "prov": "SUMINISTROS SL", "total": 121.00, "iva": 21},
        {"id": "003", "file": "Tasa_Registro.pdf", "prov": "REGISTRO MERCANTIL", "total": 50.00, "iva": 0},
    ]
if 'seleccionada' not in st.session_state: st.session_state.seleccionada = st.session_state.facturas_drive[0]

# --- BARRA LATERAL (EL DESPLAZABLE DE ODOO) ---
with st.sidebar:
    st.title("📂 Cola de Drive")
    st.caption("Selecciona una factura para validar")
    
    for f in st.session_state.facturas_drive:
        if st.button(f"{f['file']}\n{f['prov']}", key=f['id'], use_container_width=True):
            st.session_state.seleccionada = f

# --- CUERPO CENTRAL (LA FICHA BLANCA) ---
f = st.session_state.seleccionada
st.subheader(f"📄 Validando: {f['file']}")

with st.container(border=True):
    # FILA 1: CABECERA Y TRÁFICO
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: st.text_input("PROVEEDOR", value=f['prov'])
    with c2: st.selectbox("CTA. TRÁFICO", ["410.00012", "400.00005", "210.00000"])
    with c3: total = st.number_input("TOTAL FACTURA", value=f['total'], format="%.2f")

    st.divider()

    # FILA 2: GASTO E IVA (REACTIVO)
    cg1, cg2, cg3, cg4 = st.columns([1.5, 1.5, 1, 1])
    iva_p = cg3.selectbox("IVA (%)", [21, 10, 4, 0], index=[21, 10, 4, 0].index(f['iva']))
    
    base_calc = round(total / (1 + (iva_p/100)), 2)
    with cg1: st.selectbox("CTA. GASTO", ["629.00000", "600.00000", "210.00000"])
    with cg2: base = st.number_input("BASE IMPONIBLE", value=base_calc)
    
    cuota = round(base * (iva_p/100), 2)
    cg4.metric("CUOTA", f"{cuota:.2f} €")

    # FILA 3: SUPLIDOS (SIN MARCAR POR DEFECTO)
    st.write("###")
    diff = round(total - (base + cuota), 2)
    
    cs1, cs2, cs3 = st.columns([1.5, 1.5, 1])
    with cs1: 
        # Cuenta de suplidos vacía por defecto como pediste
        st.selectbox("CTA. SUPLIDOS", options=["", "555.00000", "410.99999"], index=0, 
                    help="Déjalo vacío si no hay suplidos")
    with cs2: 
        st.number_input("IMPORTE SUPLIDO", value=diff, disabled=True)
    with cs3:
        if abs(diff) < 0.01: st.success("✅ CUADRADO")
        else: st.warning("⚠️ DESCUADRE")

    # BOTÓN FINAL
    st.write("###")
    with st.form("save_asiento"):
        if st.form_submit_button("🚀 CONTABILIZAR Y PASAR AL SIGUIENTE", use_container_width=True, type="primary"):
            st.toast("Asiento enviado al .dat")
