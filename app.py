import streamlit as st

# 1. CONFIGURACIÓN LAYOUT "PDF-VIEW"
st.set_page_config(layout="wide", page_title="Búnker Pro | PDF View")

# Estilo para el PDF y el control lateral
st.markdown("""
    <style>
    .pdf-viewer {
        height: 80vh; /* Altura para ver el PDF cómodamente */
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        overflow-y: scroll; /* Si el PDF es largo */
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: white; /* Selects blancos en la ficha */
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SIMULACIÓN DE COLAS (Lo que la IA ya ha clasificado de Drive)
# Mañana esto vendrá de Gemini
if 'facturas_pendientes' not in st.session_state:
    st.session_state.facturas_pendientes = [
        {"id": "f001", "prov": "RESTAURANTE EL GRIEGO", "total": 72.97, "iva": 10, "pdf_path": "https://www.africau.edu/images/default/sample.pdf"},
        {"id": "f002", "prov": "SUMINISTROS INDUSTRIALES", "total": 121.00, "iva": 21, "pdf_path": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"},
    ]
if 'current_factura_idx' not in st.session_state: st.session_state.current_factura_idx = 0

# --- LÓGICA DE NAVEGACIÓN ---
def siguiente_factura():
    if st.session_state.current_factura_idx < len(st.session_state.facturas_pendientes) - 1:
        st.session_state.current_factura_idx += 1
    else:
        st.success("🎉 ¡Todas las facturas procesadas!")

# --- INTERFAZ DUAL (PDF + FICHA) ---
col_pdf, col_ficha = st.columns([1, 1])

# COLUMNA IZQUIERDA: EL PDF CARGADO DESDE DRIVE
with col_pdf:
    st.subheader("📁 Documento Fuente")
    current_pdf = st.session_state.facturas_pendientes[st.session_state.current_factura_idx]
    
    # Aquí cargamos el PDF real
    st.markdown(f"""
        <div class="pdf-viewer">
            <iframe src="{current_pdf['pdf_path']}" width="100%" height="100%" style="border:none;"></iframe>
        </div>
    """, unsafe_allow_html=True)
    st.caption(f"Visualizando: {current_pdf['pdf_path'].split('/')[-1]}")

# COLUMNA DERECHA: LA FICHA BLANCA DE VALIDACIÓN
with col_ficha:
    st.subheader("📝 Ficha de Asiento (Valida los 28 campos)")
    
    with st.container(border=True):
        # FILA 1: DATOS CLAVE
        f_prov, f_cta, f_total = st.columns([2, 1, 1])
        with f_prov: st.text_input("PROVEEDOR", value=current_pdf['prov'])
        with f_cta: st.selectbox("CTA. TRÁFICO", ["410.00012", "400.00005"], key=f"cta_traf_{current_pdf['id']}")
        with f_total: total_input = st.number_input("TOTAL FACTURA", value=current_pdf['total'], format="%.2f", key=f"total_{current_pdf['id']}")

        st.divider()

        # FILA 2: BASES E IVA
        f_cta_gasto, f_base, f_iva, f_cuota = st.columns([1.5, 1.5, 1, 1])
        iva_perc = f_iva.selectbox("IVA (%)", [21, 10, 4, 0], index=[21,10,4,0].index(current_pdf['iva']), key=f"iva_{current_pdf['id']}")
        
        base_calc = round(total_input / (1 + (iva_perc / 100)), 2)
        with f_cta_gasto: st.selectbox("CTA. GASTO", ["629.00000", "600.00000"], key=f"cta_gasto_{current_pdf['id']}")
        with f_base: base_input = st.number_input("BASE IMPONIBLE", value=base_calc, key=f"base_{current_pdf['id']}")
        
        cuota_calc = round(base_input * (iva_perc / 100), 2)
        f_cuota.metric("CUOTA", f"{cuota_calc:.2f} €")

        # FILA 3: SUPLIDOS Y CUADRE
        st.write("###")
        sobrante = round(total_input - (base_input + cuota_calc), 2)
        
        f_cta_sup, f_imp_sup, f_cuadre = st.columns([1.5, 1.5, 1])
        with f_cta_sup: st.selectbox("CTA. SUPLIDOS", options=["", "555.00000", "410.99999"], index=0, key=f"cta_sup_{current_pdf['id']}")
        with f_imp_sup: st.number_input("IMPORTE SUPLIDO", value=sobrante, disabled=True, key=f"suplido_{current_pdf['id']}")
        with f_cuadre:
            if abs(sobrante) < 0.01: st.success("✅ CUADRADO")
            else: st.warning("⚠️ DESCUADRE")

    # BOTÓN DE ACCIÓN (Contabilizar y pasar al siguiente)
    st.write("###")
    with st.form("form_contabilizar"):
        st.form_submit_button("🚀 CONTABILIZAR Y SIGUIENTE", use_container_width=True, type="primary", on_click=siguiente_factura)

# --- NAVEGACIÓN GLOBAL ---
st.sidebar.title("📑 Facturas Pendientes")
for i, f in enumerate(st.session_state.facturas_pendientes):
    is_selected = (i == st.session_state.current_factura_idx)
    button_label = f"#{i+1} {f['prov']}"
    if st.sidebar.button(button_label, use_container_width=True, key=f"nav_{f['id']}"):
        st.session_state.current_factura_idx = i
        st.experimental_rerun() # Para forzar la recarga del PDF si cambia la URL
