import streamlit as st

# 1. CONFIGURACIÓN Y ESTÉTICA
st.set_page_config(layout="wide", page_title="Búnker Pro | Ultra Speed")

# 2. SIMULACIÓN DE METADATOS (Lo que Gemini ya ha leído de Drive)
if 'indice_actual' not in st.session_state:
    st.session_state.indice_actual = 0

cola_facturas = [
    {"empresa": "ALMUDENA FR", "nif": "FR12345678", "total": 1210.00, "iva": 21, "bandera": "🇫🇷", "modelos": "303+349"},
    {"empresa": "GESTIÓN BCN", "nif": "B66778899", "total": 450.00, "iva": 21, "bandera": "🇪🇸", "modelos": "303"},
    {"empresa": "TRADING LON", "nif": "GB99887766", "total": 2100.00, "iva": 0, "bandera": "🇬🇧", "modelos": "303+347"},
]

# Función para saltar a la siguiente
def contabilizar_y_siguiente():
    if st.session_state.indice_actual < len(cola_facturas) - 1:
        st.session_state.indice_actual += 1
        st.toast(f"✅ Factura {st.session_state.indice_actual} contabilizada. Cargando siguiente...")
    else:
        st.success("🎉 ¡Todas las facturas de la cola han sido procesadas!")

# --- INTERFAZ ---
st.title("🚀 Validación en Cadena (Modo Asesor)")

col_cola, col_ficha = st.columns([1, 2])

# IZQUIERDA: La cola de espera
with col_cola:
    st.subheader("📬 Pendientes")
    for i, f in enumerate(cola_facturas):
        # Resaltamos la que estamos editando ahora
        style = "border: 2px solid #2ecc71;" if i == st.session_state.indice_actual else "opacity: 0.5;"
        st.markdown(f"""
            <div style="background: white; padding: 10px; border-radius: 8px; margin-bottom: 5px; {style}">
                {f['bandera']} <b>{f['empresa']}</b><br>
                <small>{f['total']} € - Mod: {f['modelos']}</small>
            </div>
        """, unsafe_allow_html=True)

# DERECHA: La Ficha Blanca Activa
with col_ficha:
    factura = cola_facturas[st.session_state.indice_actual]
    st.subheader(f"📝 Editando: {factura['empresa']}")
    
    with st.container(border=True):
        c1, c2 = st.columns(2)
        nif_input = c1.text_input("NIF", value=factura['nif'], key=f"nif_{st.session_state.indice_actual}")
        fecha_input = c2.date_input("Fecha Factura", key=f"date_{st.session_state.indice_actual}")
        
        st.divider()
        
        # LÓGICA A3 AUTOMÁTICA
        col_t, col_i = st.columns([2, 1])
        total_f = col_t.number_input("TOTAL FACTURA (€)", value=factura['total'], key=f"tot_{st.session_state.indice_actual}")
        tipo_iva = col_i.selectbox("IVA %", [21, 10, 4, 0], index=0 if factura['iva']==21 else 3)
        
        bi = total_f / (1 + (tipo_iva/100))
        cuota = total_f - bi
        
        # Métricas de confirmación visual
        m1, m2 = st.columns(2)
        m1.metric("Base (BI1)", f"{bi:.2f} €")
        m2.metric("Cuota IVA", f"{cuota:.2f} €")
        
        st.divider()
        
        # BOTÓN DE ACCIÓN (El "Enter" de la contabilidad)
        # En Streamlit, si el foco está en el formulario, al pulsar el botón se dispara la función
        st.button("✅ CONTABILIZAR (ENTER)", 
                  on_click=contabilizar_y_siguiente, 
                  type="primary", 
                  use_container_width=True)

st.caption("⌨️ **Modo Experto:** Revisa los datos y pulsa el botón para pasar a la siguiente factura automáticamente.")
