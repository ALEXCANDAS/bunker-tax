import streamlit as st

# 1. CSS PARA ALTA DENSIDAD (Aprovechar cada píxel)
st.set_page_config(layout="wide", page_title="Búnker Pro | Speed Entry")

st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .ficha-blanca {
        background: white;
        padding: 15px;
        border-radius: 8px;
        border-left: 10px solid #2ecc71; /* Verde si Gemini está seguro, Rojo si duda */
        margin-bottom: 10px;
        font-size: 14px;
    }
    .status-agente { font-size: 11px; color: #64748b; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA COMPACTA ---
c_title, c_sync = st.columns([4, 1])
c_title.title("🚀 Validación de Asientos Flash")
if c_sync.button("🔄 Sincronizar Drive", type="primary", use_container_width=True):
    st.toast("Escaneando metadatos...")

# --- INTERFAZ DUAL ---
col_cola, col_entrada = st.columns([1, 2])

with col_cola:
    st.subheader("📥 Cola de Validación")
    # Ficha que "habla" de un vistazo
    st.markdown("""
        <div class="ficha-blanca">
            <b>🇫🇷 ALMUDENA FRANCIA</b> <span style="float:right;">1.210,00 €</span><br>
            <span class="status-agente">Gemini: Confianza 98% (Modelos 303, 349)</span>
        </div>
        <div class="ficha-blanca" style="border-left-color: #e74c3c;">
            <b>🇪🇸 GESTIÓN BCN</b> <span style="float:right;">450,00 €</span><br>
            <span class="status-agente">Gemini: Confianza 60% (Duda en NIF)</span>
        </div>
    """, unsafe_allow_html=True)

with col_entrada:
    st.subheader("📝 Ficha Blanca de Edición (Lógica A3)")
    
    with st.container(border=True):
        # FILA 1: Identificación básica
        f1c1, f1c2, f1c3, f1c4 = st.columns(4)
        f1c1.text_input("NIF", "FR12345678")
        f1c2.date_input("Fecha")
        f1c3.text_input("Cuenta", "400.0001")
        f1c4.selectbox("Modelo", ["303+349", "303", "130"])

        # FILA 2: LÓGICA DE CÁLCULO A3 (Automático)
        st.divider()
        f2c1, f2c2, f2c3, f2c4 = st.columns([2, 1, 1, 1])
        
        total = f2c1.number_input("TOTAL FACTURA (€)", value=1210.00)
        tipo_iva = f2c2.selectbox("IVA %", [21, 10, 4, 0])
        
        # Cálculo en tiempo real
        bi = total / (1 + (tipo_iva/100))
        cuota = total - bi
        
        f2c3.metric("Base (BI1)", f"{bi:.2f} €")
        f2c4.metric("Cuota IVA", f"{cuota:.2f} €")

        # FILA 3: Los 28 campos comprimidos
        with st.expander("⚙️ Metadatos .dat (Campos secundarios)"):
            st.columns(4)[0].text_input("ID Factura", "2026/045")
            st.columns(4)[1].text_input("CP", "08001")
            st.columns(4)[2].text_input("Categoría", "Gasto General")
            st.columns(4)[3].text_input("Cta. Base", "600.0")

        st.button("✅ CONTABILIZAR Y SIGUIENTE (Enter)", use_container_width=True)
