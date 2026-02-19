import streamlit as st

# 1. MOTOR DE CÁLCULO REACTIVO (TABULADOR READY)
if 'base_val' not in st.session_state: st.session_state.base_val = 100.0
if 'iva_perc' not in st.session_state: st.session_state.iva_perc = 21
if 'cuota_val' not in st.session_state: st.session_state.cuota_val = 21.0
if 'total_val' not in st.session_state: st.session_state.total_val = 121.0

def recalcular_por_base():
    st.session_state.cuota_val = round(st.session_state.base_val * (st.session_state.iva_perc / 100), 2)
    st.session_state.total_val = round(st.session_state.base_val + st.session_state.cuota_val, 2)

def recalcular_por_total():
    st.session_state.base_val = round(st.session_state.total_val / (1 + (st.session_state.iva_perc / 100)), 2)
    st.session_state.cuota_val = round(st.session_state.total_val - st.session_state.base_val, 2)

# 2. INTERFAZ SaaS PROFESIONAL
st.set_page_config(layout="wide", page_title="Búnker Pro | Producción Real")

# Estilos para banderas, totales alineados y alertas
st.markdown("""
    <style>
    .total-row { background-color: #f1f5f9; font-weight: bold; border-top: 2px solid #3b82f6; padding: 12px 0; }
    .badge-flag { font-size: 1.5rem; }
    .stNumberInput input { font-size: 1.1rem !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# SECTOR DE TRABAJO (RECIBIDAS / EMITIDAS)
libro = st.sidebar.radio("LIBRO", ["📥 RECIBIDAS", "📤 EMITIDAS"])

with st.container(border=True):
    col_pdf, col_ficha = st.columns([1.2, 1])
    
    with col_pdf:
        st.markdown("### 📄 Visor Documental")
        # Visor que no falla
        st.markdown('<iframe src="https://www.africau.edu/images/default/sample.pdf" width="100%" height="450px" style="border-radius:10px;"></iframe>', unsafe_allow_html=True)
    
    with col_ficha:
        st.markdown(f"### ⚡ Registro de {libro}")
        # Fila 1: Identificación e Icono de Origen
        c1, c2, c3 = st.columns([2, 1, 0.5])
        c1.text_input("PROVEEDOR", value="ADOBE SYSTEMS IE")
        c2.text_input("NIF / VAT", value="IE6362892H")
        c3.markdown("## 🇪🇺") # Icono visual de origen fiscal

        st.divider()

        # Fila 2: Configuración (IA sugiere, tú validas)
        o1, o2, o3 = st.columns([1, 1, 1])
        o1.selectbox("TIPO", ["IVA Soportado", "Inversión", "Profesional"])
        o2.text_input("CTA. GASTO", value="629.00000")
        o3.text_input("Nº FACTURA", value="FRA-2026-001")

        # Fila 3: El Núcleo Reactivo (IVA EN EL MEDIO)
        i1, i2, i3 = st.columns([1.2, 0.8, 1])
        i1.number_input("BASE IMPONIBLE", key="base_val", on_change=recalcular_por_base, format="%.2f")
        i2.selectbox("IVA %", [21, 10, 4, 0], key="iva_perc", on_change=recalcular_por_base, index=0)
        i3.number_input("CUOTA IVA", key="cuota_val", format="%.2f")
        
        # Fila 4: Total (Cierre)
        st.number_input("💵 TOTAL FACTURA (€)", key="total_val", on_change=recalcular_por_total, format="%.2f")

        if st.button("🚀 CONTABILIZAR (ENTER)", use_container_width=True, type="primary"):
            st.toast("Asiento exportado al TSV correctamente.")

st.write("###")

# --- LIBRO DE REGISTRO CON AUDITORÍA Y TOTALES VERTICALES ---
st.subheader(f"📋 Libro de Registro de {libro}")

# Cabecera Maestra Alineada
h = st.columns([0.4, 0.6, 0.8, 2, 0.8, 0.8, 0.8, 1.5, 0.4])
headers = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "TOTAL", "MODELOS", "VIS"]
for col, text in zip(h, headers): col.markdown(f"**{text}**")

def draw_row(audit, flag, fecha, nombre, nif, base, iva, total, modelos):
    r = st.columns([0.4, 0.6, 0.8, 2, 0.8, 0.8, 0.8, 1.5, 0.4])
    r[0].write("✅" if audit=="ok" else "⚠️")
    r[1].markdown(f"### {flag}") # Bandera grande para auditoría visual
    r[2].write(fecha)
    r[3].markdown(f"**{nombre}** <br><small>{nif}</small>", unsafe_allow_html=True)
    r[4].write(f"{base}€")
    r[5].write(f"{iva}€")
    r[6].write(f"**{total}€**")
    
    tags = "".join([f'<span style="background:#3b82f6;color:white;padding:2px 5px;border-radius:3px;margin-right:2px;font-size:10px;">M-{m}</span>' for m in modelos])
    r[7].markdown(tags, unsafe_allow_html=True)
    r[8].button("👁️", key=nombre)

draw_row("ok", "🇪🇺", "19/02", "ADOBE SYSTEMS IE", "IE6362892H", "100.00", "21.00", "121.00", ["303", "349"])
draw_row("ok", "🇪🇸", "18/02", "BAR EL GRIEGO", "B12345678", "66.34", "6.63", "72.97", ["303"])

# --- LÍNEA DE TOTALES ALINEADA POR COLUMNA ---
st.markdown('<div class="total-row">', unsafe_allow_html=True)
t = st.columns([0.4, 0.6, 0.8, 2, 0.8, 0.8, 0.8, 1.5, 0.4])
t[3].write("TOTALES CUADRE:")
t[4].write(f"{st.session_state.base_val + 66.34}€") # Suma Base
t[5].write(f"{st.session_state.cuota_val + 6.63}€") # Suma IVA
t[6].write(f"{st.session_state.total_val + 72.97}€") # Suma Total
st.markdown('</div>', unsafe_allow_html=True)
