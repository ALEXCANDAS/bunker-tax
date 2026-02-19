import streamlit as st

# 1. MOTOR DE REDONDEO Y CÁLCULO (Céntimos controlados)
if 'base_val' not in st.session_state: st.session_state.base_val = 100.00
if 'iva_perc' not in st.session_state: st.session_state.iva_perc = 21
if 'cuota_val' not in st.session_state: st.session_state.cuota_val = 21.00
if 'total_val' not in st.session_state: st.session_state.total_val = 121.00

def recalcular_por_base():
    # Redondeo forzado a 2 decimales para evitar colas de céntimos
    st.session_state.cuota_val = round(st.session_state.base_val * (st.session_state.iva_perc / 100), 2)
    st.session_state.total_val = round(st.session_state.base_val + st.session_state.cuota_val, 2)

def recalcular_por_total():
    st.session_state.base_val = round(st.session_state.total_val / (1 + (st.session_state.iva_perc / 100)), 2)
    st.session_state.cuota_val = round(st.session_state.total_val - st.session_state.base_val, 2)

# 2. INTERFAZ ULTRA-WIDE
st.set_page_config(layout="wide", page_title="Búnker Pro | Asesoría Real")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .total-row { background-color: #f1f5f9; font-weight: bold; border-top: 2px solid #3b82f6; padding: 12px 0; }
    /* Estética de software de escritorio, no web aburrida */
    input { font-family: 'Roboto Mono', monospace !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL SUPERIOR: ACCIÓN ---
with st.container(border=True):
    col_pdf, col_ficha = st.columns([1.2, 1])
    
    with col_pdf:
        # Visor blindado (Usando un contenedor con alto fijo para que no baile)
        st.markdown('<div style="background:#334155; height:500px; border-radius:8px; overflow:hidden; border:2px solid #1e293b;">'
                    '<iframe src="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf" '
                    'width="100%" height="100%" style="border:none;"></iframe>'
                    '</div>', unsafe_allow_html=True)
    
    with col_ficha:
        st.markdown("### ⚡ Entrada Flash")
        # Identificación (Icono grande al lado para auditoría visual)
        c1, c2, c3 = st.columns([2, 1, 0.5])
        c1.text_input("PROVEEDOR", value="ADOBE SYSTEMS IE")
        c2.text_input("NIF", value="IE6362892H")
        c3.markdown("## 🇪🇺") # Bandera para chequear 349 al vuelo

        st.divider()

        # Configuración de Cuentas
        o1, o2, o3 = st.columns([1, 1, 1])
        o1.selectbox("TIPO", ["IVA Soportado", "Inversión", "Profesional"])
        o2.text_input("CTA. GASTO", value="629.00000")
        o3.text_input("Nº FRA", value="2026-X1")

        # NÚCLEO REACTIVO (IVA AL CENTRO)
        i1, i2, i3 = st.columns([1.2, 0.8, 1])
        # Al salir de aquí con TAB, todo se redondea y recalcula
        i1.number_input("BASE", key="base_val", on_change=recalcular_por_base, format="%.2f", step=0.01)
        i2.selectbox("IVA %", [21, 10, 4, 0], key="iva_perc", on_change=recalcular_por_base, index=0)
        i3.number_input("CUOTA", key="cuota_val", format="%.2f", step=0.01)
        
        st.number_input("💵 TOTAL FACTURA (€)", key="total_val", on_change=recalcular_por_total, format="%.2f", step=0.01)

        if st.button("🚀 CONTABILIZAR (ENTER)", use_container_width=True, type="primary"):
            st.toast("Contabilizado en ráfaga.")

st.write("###")

# --- PANEL INFERIOR: REGISTRO CON BANDERAS Y TOTALES ALINEADOS ---
st.subheader("📋 Libro de Registro / Auditoría")

# Cabecera alineada con la línea de totales
h = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 1.5, 0.4])
headers = ["AUD", "ORG", "FECHA", "SUJETO", "BASE", "IVA", "TOTAL", "BANDERAS", "VIS"]
for col, text in zip(h, headers): col.markdown(f"**{text}**")

def fila(aud, flag, fecha, sujeto, base, iva, total, modelos):
    r = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 1.5, 0.4])
    r[0].write("✅" if aud=="ok" else "⚠️")
    r[1].markdown(f"### {flag}") # Bandera para detectar intracomunitarias "vagas"
    r[2].write(fecha)
    r[3].markdown(f"**{sujeto}**", unsafe_allow_html=True)
    r[4].write(f"{base:.2f}€")
    r[5].write(f"{iva:.2f}€")
    r[6].write(f"**{total:.2f}€**")
    
    tags = "".join([f'<span style="background:#3b82f6;color:white;padding:2px 5px;border-radius:4px;margin-right:2px;font-size:10px;">M-{m}</span>' for m in modelos])
    r[7].markdown(tags, unsafe_allow_html=True)
    r[8].button("👁️", key=sujeto)

fila("ok", "🇪🇺", "19/02", "ADOBE SYSTEMS", st.session_state.base_val, st.session_state.cuota_val, st.session_state.total_val, ["303", "349"])
fila("ok", "🇪🇸", "18/02", "BAR EL GRIEGO", 66.34, 6.63, 72.97, ["303"])

# TOTALES VERTICALES (Debajo de cada columna)
st.markdown('<div class="total-row">', unsafe_allow_html=True)
t = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 1.5, 0.4])
t[3].write("TOTALES CUADRE:")
t[4].write(f"{st.session_state.base_val + 66.34:.2f}€") # Debajo de BASE
t[5].write(f"{st.session_state.cuota_val + 6.63:.2f}€") # Debajo de IVA
t[6].write(f"{st.session_state.total_val + 72.97:.2f}€") # Debajo de TOTAL
st.markdown('</div>', unsafe_allow_html=True)
