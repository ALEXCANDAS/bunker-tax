import streamlit as st

# 1. MOTOR REACTIVO (2 DECIMALES CLAVADOS)
if 'base_val' not in st.session_state: st.session_state.base_val = 100.00
if 'iva_perc' not in st.session_state: st.session_state.iva_perc = 21

def recalcular():
    st.session_state.cuota_val = round(st.session_state.base_val * (st.session_state.iva_perc / 100), 2)
    st.session_state.total_val = round(st.session_state.base_val + st.session_state.cuota_val, 2)

if 'cuota_val' not in st.session_state: recalcular()

# 2. ESTILOS DE ICONOS PROFESIONALES
st.markdown("""
    <style>
    .mod-303 { background-color: #01579b; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .mod-349 { background-color: #2e7d32; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .mod-111 { background-color: #e65100; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .flag-icon { font-size: 1.5rem; }
    .total-line { background-color: #f1f5f9; font-weight: bold; border-top: 3px solid #3b82f6; padding: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL SUPERIOR: ACCIÓN ---
with st.container(border=True):
    col_pdf, col_ficha = st.columns([1.2, 1])
    with col_pdf:
        st.markdown('<iframe src="https://www.africau.edu/images/default/sample.pdf" width="100%" height="450px" style="border:none; border-radius:8px;"></iframe>', unsafe_allow_html=True)
    
    with col_ficha:
        st.markdown("### ⚡ Validación Rápida")
        c1, c2, c3 = st.columns([2, 1, 0.5])
        c1.text_input("PROVEEDOR", value="ADOBE SYSTEMS IE")
        c2.text_input("NIF", value="IE6362892H")
        c3.markdown("## 🇪🇺") # Icono directo, sin letras

        o1, o2, o3 = st.columns([1, 1, 1])
        o1.selectbox("TIPO", ["IVA Soportado", "Inversión", "Profesional"])
        o2.text_input("CAT. GASTO", value="Software")
        o3.text_input("CTA. GASTO", value="629.00000")

        st.divider()
        i1, i2, i3 = st.columns([1.2, 0.8, 1])
        i1.number_input("BASE", key="base_val", on_change=recalcular, format="%.2f")
        i2.selectbox("IVA %", [21, 10, 4, 0], key="iva_perc", on_change=recalcular, index=0)
        i3.number_input("CUOTA", key="cuota_val", format="%.2f")
        
        st.number_input("💵 TOTAL FACTURA (€)", key="total_val", format="%.2f")
        st.button("🚀 CONTABILIZAR (ENTER)", use_container_width=True, type="primary")

# --- PANEL INFERIOR: REGISTRO CON ICONOS NUMÉRICOS ---
st.subheader("📋 Libro de Registro / Auditoría")

h = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 1.5, 0.4])
headers = ["AUD", "ORG", "FECHA", "SUJETO", "BASE", "IVA", "TOTAL", "MODELOS", "VIS"]
for col, text in zip(h, headers): col.markdown(f"**{text}**")

def fila_saas(aud, flag, fecha, sujeto, base, iva, total, modelos):
    r = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 1.5, 0.4])
    r[0].write("✅" if aud=="ok" else "⚠️")
    r[1].markdown(f"### {flag}") # Bandera profesional 🇪🇸 / 🇪🇺
    r[2].write(fecha)
    r[3].markdown(f"**{sujeto}**")
    r[4].write(f"{base:.2f}€")
    r[5].write(f"{iva:.2f}€")
    r[6].write(f"**{total:.2f}€**")
    
    # Iconos con número de modelo (303, 349...)
    m_html = ""
    for m in modelos:
        css_class = f"mod-{m}"
        m_html += f'<span class="{css_class}">{m}</span> '
    r[7].markdown(m_html, unsafe_allow_html=True)
    r[8].button("👁️", key=sujeto)

fila_saas("ok", "🇪🇺", "19/02", "ADOBE SYSTEMS", st.session_state.base_val, st.session_state.cuota_val, st.session_state.total_val, ["303", "349"])
fila_saas("ok", "🇪🇸", "18/02", "BAR EL GRIEGO", 66.34, 6.63, 72.97, ["303"])

# TOTALES VERTICALES
st.markdown('<div class="total-line">', unsafe_allow_html=True)
t = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 1.5, 0.4])
t[3].write("TOTALES CUADRE:")
t[4].write(f"{st.session_state.base_val + 66.34:.2f}€")
t[5].write(f"{st.session_state.cuota_val + 6.63:.2f}€")
t[6].write(f"{st.session_state.total_val + 72.97:.2f}€")
st.markdown('</div>', unsafe_allow_html=True)
