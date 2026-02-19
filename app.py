import streamlit as st

# 1. PREDiseño "FICHA BLANCA" (High-End SaaS)
st.set_page_config(layout="wide", page_title="Búnker Pro | Visual Signal")

st.markdown("""
    <style>
    .ficha-blanca {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-left: 5px solid #000;
        margin-bottom: 15px;
    }
    .bandera { font-size: 24px; margin-right: 10px; }
    .modelo-badge {
        background-color: #f1f5f9;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
        color: #475569;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.title("🛡️ Búnker Control Center")
st.write("###")

# --- LA INTERFAZ DE "GOLPE DE OCIO" ---
col_lista, col_detalle = st.columns([1, 2])

with col_lista:
    st.subheader("📥 Entrada")
    # Simulación de las fichas blancas que "hablan"
    fichas = [
        {"empresa": "ALMUDENA FR", "bandera": "🇫🇷", "total": "1.250€", "modelos": ["303", "349"], "estado": "Pendiente"},
        {"empresa": "GESTIÓN BCN", "bandera": "🇪🇸", "total": "450€", "modelos": ["303"], "estado": "OK"},
        {"empresa": "TRADING LON", "bandera": "🇬🇧", "total": "2.100€", "modelos": ["303", "347"], "estado": "Error"}
    ]
    
    for f in fichas:
        with st.container():
            st.markdown(f"""
                <div class="ficha-blanca">
                    <span class="bandera">{f['bandera']}</span> <b>{f['empresa']}</b><br>
                    <span style="font-size: 20px; font-weight: bold;">{f['total']}</span><br>
                    <span class="modelo-badge">MOD {f['modelos'][0]}</span>
                    {"<span class='modelo-badge'>MOD " + f['modelos'][1] + "</span>" if len(f['modelos']) > 1 else ""}
                </div>
            """, unsafe_allow_html=True)

with col_detalle:
    st.subheader("🔍 Validación de los 28 Campos")
    with st.container(border=True):
        # Aquí es donde Gemini "habla" y tú validas rápido
        c1, c2, c3 = st.columns(3)
        c1.text_input("NIF", value="ESA12345678")
        c2.text_input("FECHA", value="19/02/2026")
        c3.text_input("TRIMESTRE", value="1T")
        
        st.divider()
        st.write("**Desglose de Bases (Hacia el .dat)**")
        st.data_editor({
            "Base": ["BI1", "BI2", "BI3"],
            "Importe": [1000.0, 0.0, 0.0],
            "IVA %": [21, 10, 4]
        }, hide_index=True, use_container_width=True)
        
        st.button("✅ VALIDAR Y CONTABILIZAR", type="primary", use_container_width=True)

# --- ACCIÓN GLOBAL ---
st.sidebar.button("🔄 Sincronizar Drive", use_container_width=True)
