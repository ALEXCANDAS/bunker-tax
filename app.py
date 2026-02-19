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
    st.
