import streamlit as st
import pandas as pd

# 1. SETUP DE PANTALLA (Pensado para tu LG partido)
st.set_page_config(layout="wide", page_title="Búnker Pro | Drive Link")

# Estética oscura/suave (para que combine con tu f.lux)
st.markdown("""
    <style>
    .main { background-color: #1a1c1e; color: #e2e8f0; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #2d2f31; color: white; border: 1px solid #4a4d50;
    }
    .pdf-container {
        height: 85vh; border: 2px solid #3e4246; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXIÓN DRIVE (Simulada con ID de archivos)
# Mañana usaremos st.connection("google_drive") para leer tu carpeta real
if 'cola_drive' not in st.session_state:
    st.session_state.cola_drive = [
        {"id": "DOC_001", "nombre": "Factura_Restaurante.pdf", "drive_url": "https://www.africau.edu/images/default/sample.pdf", "status": "Pendiente"},
        {"id": "DOC_002", "nombre": "Compra_Mercaderias.pdf", "drive_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "status": "Revisar"},
    ]
if 'idx' not in st.session_state: st.session_state.idx = 0

# --- INTERFAZ DUAL (Aprovechando el LG) ---
col_archivo, col_ficha = st.columns([1.2, 1])

# IZQUIERDA: VISOR DE DRIVE (El PDF que Pedro tiene que validar)
with col_archivo:
    factura_actual = st.session_state.cola_drive[st.session_state.idx]
    st.subheader(f"📄 {factura_actual['nombre']}")
    
    # Visor de PDF integrado
    st.markdown(f"""
        <iframe src="{factura_actual['drive_url']}" class="pdf-container" width="100%"></iframe>
    """, unsafe_allow_html=True)

# DERECHA: FICHA BLANCA (Mecánica A3 Reactiva)
with col_ficha:
    st.subheader("📝 Validación del Asiento")
    
    # Lógica de cálculo al vuelo (lo que ya nos gusta)
    with st.container(border=True):
        # Datos Tráfico
        c1, c2 = st.columns([2, 1])
        prov = c1.text_input("PROVEEDOR (IA)", value="RESTAURANTE EL GRIEGO")
        cta_prov = c2.text_input("CTA. 400/410", value="410.00012")
        
        # El Total es el disparador
        total = st.number_input("TOTAL FACTURA", value=72.97, format="%.2f")
        iva_tipo = st.selectbox("IVA (%)", [21, 10, 4, 0], index=1) # 10% por defecto si es Restaurante
        
        st.divider()
        
        # Cálculos automáticos
        base_calc = round(total / (1 + (iva_tipo / 100)), 2)
        cuota_calc = round(total - base_calc, 2)
        
        # Datos Gasto
        cg1, cg2 = st.columns([1, 1])
        cta_gasto = cg1.text_input("CTA. GASTO", value="629.00000")
        base_edit = cg2.number_input("BASE IMPONIBLE", value=base_calc)
        
        st.metric("CUOTA IVA", f"{cuota_calc} €")
        
        # Suplidos automáticos si no cuadra
        suplido = round(total - (base_edit + (base_edit * (iva_tipo/100))), 2)
        if abs(suplido) > 0.01:
            st.warning(f"Suplido/Diferencia: {suplido} €")
            cta_sup = st.text_input("CTA. SUPLIDOS", placeholder="555.0...")

        # BOTÓN ENTER
        st.write("###")
        if st.button("🚀 CONTABILIZAR Y SIGUIENTE (ENTER)", use_container_width=True, type="primary"):
            if st.session_state.idx < len(st.session_state.cola_drive) - 1:
                st.session_state.idx += 1
                st.rerun()
            else:
                st.success("¡Carpeta terminada!")

# NAVEGADOR DE COLA (Abajo para no estorbar el flujo horizontal)
st.divider()
st.caption("Ficha Blanca v2.4 | LG OnScreen Optimized | f.lux Friendly")
