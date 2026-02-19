import streamlit as st
from datetime import date

# 1. LATENCIA CERO: Configuración de alto rendimiento
st.set_page_config(layout="wide", page_title="Búnker Pro | Ultra-Fast Mode")

# Estilo para que parezca una herramienta de terminal profesional (f.lux friendly)
st.markdown("""
    <style>
    .stDateInput input { font-size: 1.1rem; font-weight: bold; }
    .stForm { border: none !important; padding: 0 !important; }
    /* Foco visual en el total */
    input[aria-label="💵 TOTAL FACTURA (€)"] { background-color: #f0f7ff !important; border: 2px solid #3b82f6 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGICA DE REACCIÓN INSTANTÁNEA
if 'total_f' not in st.session_state: st.session_state.total_f = 15.00 # Ese tique pequeño de Holded
if 'iva_p' not in st.session_state: st.session_state.iva_p = 10

def recalcular():
    st.session_state.base_f = round(st.session_state.total_f / (1 + (st.session_state.iva_p / 100)), 2)
    st.session_state.cuota_f = round(st.session_state.total_f - st.session_state.base_f, 2)

if 'base_f' not in st.session_state: recalcular()

# --- INTERFAZ DE TRABAJO ---
col_pdf, col_ficha = st.columns([1.1, 1])

with col_pdf:
    # Imagen de la factura cargada (Fragmento centrado en el tique)
    st.markdown("### 🖼️ Fragmento Focus")
    st.image("https://via.placeholder.com/600x400?text=TIQUE+RAPIDO+15.00€", use_container_width=True)

with col_ficha:
    with st.form("fast_entry"):
        st.markdown("### ⚡ Entrada Rápida")
        
        with st.container(border=True):
            # CABECERA: FECHA Y TRÁFICO (Lo mínimo para A3/Contasol)
            c1, c2, c3 = st.columns([1, 1.5, 1])
            f_contable = c1.date_input("FECHA", value=date.today())
            prov_name = c2.text_input("PROVEEDOR", value="BAR PLAZA")
            # Si pones 410+ aquí, Gemini entiende que hay que crearla en el TSV
            cta_traf = c3.text_input("CTA (410+)", value="410.00015")

            st.divider()

            # CUERPO: GASTO Y OPERACIÓN
            g1, g2, g3 = st.columns([1, 1, 1])
            # Icono dinámico: Si es Bar, sale 🍽️
            g1.markdown("#### 🍽️ Gasto")
            g2.selectbox("OPERACIÓN", ["Soportado", "Inversión"], label_visibility="collapsed")
            g3.text_input("CTA. GASTO", value="629.00000", label_visibility="collapsed")

            st.divider()

            # NÚCLEO: IVA AL CENTRO (Mecánica Exact)
            n1, n2, n3 = st.columns([1.2, 0.8, 1])
            # IVA en el medio: El ojo no salta
            iva_sel = n2.selectbox("IVA (%)", [21, 10, 4, 0], index=1, key="iva_p_form")
            base_in = n1.number_input("BASE", value=st.session_state.base_f, format="%.2f")
            cuota_in = n3.number_input("CUOTA (±0.01)", value=st.session_state.cuota_f, format="%.2f")

            # EL TOTAL: Disparador final
            st.write("###")
            total_in = st.number_input("💵 TOTAL FACTURA (€)", value=st.session_state.total_f, format="%.2f")

        # EL BOTÓN QUE CAPTURA EL ENTER
        if st.form_submit_button("🚀 CONTABILIZAR (ENTER)", use_container_width=True, type="primary"):
            # Aquí se inyecta la línea en el TSV y se limpia la pantalla
            st.toast("¡Pum! Contabilizado. Siguiente factura...")
            # Lógica: Mover factura procesada a "Terminado" y cargar nueva de Drive

# 3. EL "FEED" DE ÉXITO (Para ver que todo fluye)
st.divider()
st.caption("Últimos movimientos en el Registro (TSV)")
st.write("🟢 **18:24** - BAR PLAZA (15.00€) -> Exportado a A3 ✅")
st.write("🟢 **18:22** - GASOLINERA (60.00€) -> Exportado a A3 ✅")
