import streamlit as st

# 1. SETUP DE ALTO RENDIMIENTO
st.set_page_config(layout="wide", page_title="Búnker Pro | Gestión Dual")

# Estilos para las pestañas y las banderas
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #f8fafc; border-radius: 5px; padding: 10px; }
    .stTabs [aria-selected="true"] { background-color: #3b82f6 !important; color: white !important; }
    .badge-iva { background-color: #e1f5fe; color: #01579b; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. NAVEGACIÓN POR PESTAÑAS (Para no saturar el largo de pantalla)
tab_recibidas, tab_emitidas, tab_registro = st.tabs(["📥 FACTURAS RECIBIDAS", "📤 FACTURAS EMITIDAS", "📋 REGISTRO GENERAL"])

# --- PESTAÑA 1: RECIBIDAS (ZONA DE COMBATE) ---
with tab_recibidas:
    col_pdf, col_ficha = st.columns([1.1, 1])
    
    with col_pdf:
        st.subheader("🖼️ Visor de Factura")
        # Imagen protegida para que no se rompa el layout
        st.image("https://via.placeholder.com/800x600?text=FACTURA+RECIBIDA+EL+GRIEGO", use_container_width=True)
    
    with col_ficha:
        with st.form("recibida_form"):
            st.markdown("### ⚡ Entrada Rápida")
            with st.container(border=True):
                c1, c2, c3 = st.columns([1, 1.5, 1])
                c1.date_input("FECHA", key="f_rec")
                c2.text_input("PROVEEDOR", value="RESTAURANTE EL GRIEGO")
                c3.text_input("CTA. TRÁFICO", value="410.00012")
                
                st.divider()
                
                # IVA EN EL MEDIO (Eje Exact)
                n1, n2, n3 = st.columns([1.2, 0.8, 1])
                n2.selectbox("IVA (%)", [21, 10, 4, 0], index=1)
                n1.number_input("BASE", value=66.34)
                n3.number_input("CUOTA IVA", value=6.63)
                
                st.number_input("💵 TOTAL FACTURA", value=72.97)
                
            st.form_submit_button("🚀 CONTABILIZAR (ENTER)", use_container_width=True, type="primary")

# --- PESTAÑA 2: EMITIDAS (VENTAS) ---
with tab_emitidas:
    st.subheader("📤 Gestión de Ventas")
    # Aquí la lógica cambia: Cliente (430), Ingresos (700), etc.
    st.info("Módulo de facturación emitida: Sincronizado con tus servicios.")
    st.image("https://via.placeholder.com/800x400?text=GRÁFICO+DE+VENTAS+Y+EMITIDAS", use_container_width=True)

# --- PESTAÑA 3: REGISTRO GENERAL (LA FICHA DE BANDERAS) ---
with tab_registro:
    st.subheader("📋 Control de Modelos y Auditoría")
    
    # Simulación de Tabla de Registro Compacta
    data = [
        {"Fecha": "2026-02-19", "Tipo": "Recibida", "Sujeto": "BAR PLAZA", "Total": "15,00€", "Modelos": "303"},
        {"Fecha": "2026-02-18", "Tipo": "Emitida", "Sujeto": "CLIENTE FINAL SL", "Total": "1.210,00€", "Modelos": "303, 347"},
        {"Fecha": "2026-02-15", "Tipo": "Recibida", "Sujeto": "ASESORÍA NACHO", "Total": "300,00€", "Modelos": "303, 111"}
    ]
    
    header = st.columns([1, 1, 2, 1, 2, 0.5])
    header[0].write("**Fecha**")
    header[1].write("**Tipo**")
    header[2].write("**Sujeto**")
    header[3].write("**Total**")
    header[4].write("**Modelos**")
    header[5].write("**Link**")
    
    for item in data:
        row = st.columns([1, 1, 2, 1, 2, 0.5])
        row[0].write(item["Fecha"])
        row[1].write(item["Tipo"])
        row[2].write(f"**{item['Sujeto']}**")
        row[3].write(item["Total"])
        
        # Banderas Dinámicas
        banderas = ""
        for m in item["Modelos"].split(", "):
            banderas += f'<span class="badge-iva">M-{m}</span> '
        row[4].markdown(banderas, unsafe_allow_html=True)
        
        if row[5].button("👁️", key=item["Sujeto"]):
            st.toast("Cargando factura para revisión...")
