import streamlit as st

# 1. CONFIGURACIÓN SaaS ULTRA-WIDE
st.set_page_config(layout="wide", page_title="Búnker Pro | Libro Maestro")

# CSS para alinear totales y dar estética de software profesional
st.markdown("""
    <style>
    .total-row { background-color: #f1f5f9; font-weight: bold; border-top: 2px solid #3b82f6; padding: 10px 0; }
    .badge-iso { font-size: 1.2rem; }
    .stMetric { background: none; border: none; padding: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- PARTE SUPERIOR: ENTRADA / EDICIÓN (RECIBIDAS) ---
with st.expander("📥 PANEL DE ENTRADA DE FACTURAS", expanded=True):
    col_pdf, col_ficha = st.columns([1.1, 1])
    with col_pdf:
        st.image("https://via.placeholder.com/800x300?text=VISOR+DE+FACTURA+ACTUAL", use_container_width=True)
    with col_ficha:
        # Aquí va tu ficha "Exact" que ya tenemos perfeccionada con el IVA en medio
        st.markdown("### ⚡ Validación Rápida")
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.text_input("PROVEEDOR", value="ADOBE SYSTEMS IE")
        c2.text_input("NIF", value="IE6362892H")
        c3.selectbox("ORG", ["🇪🇸", "🇪🇺", "🌎"], index=1)
        
        # El motor de importes
        i1, i2, i3 = st.columns([1, 0.8, 1])
        i1.number_input("BASE", value=120.00)
        i2.selectbox("IVA %", [21, 10, 4, 0], index=3)
        i3.number_input("CUOTA", value=0.00)
        st.button("🚀 CONTABILIZAR (ENTER)", use_container_width=True, type="primary")

st.divider()

# --- PARTE INFERIOR: LIBRO DE REGISTRO (EMITIDAS Y RECIBIDAS CON FILTRO) ---
st.subheader("📋 Libro de Registro y Auditoría de Modelos")

# Filtros rápidos de segmento
f_c1, f_c2, f_c3 = st.columns([1, 1, 3])
tipo_libro = f_c1.selectbox("LIBRO", ["Recibidas", "Emitidas", "Inversiones"])
tri_libro = f_c2.selectbox("TRIMESTRE", ["1T", "2T", "3T", "4T", "Anual"])
search = f_c3.text_input("🔍 Buscar por NIF, Nombre o Cuenta...")

# CABECERA DEL LIBRO (Alineada con los totales de abajo)
# Est | Org | Fecha | Sujeto / NIF | Base | IVA | Ret | Total | Modelos
h = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
cols = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]
for col, text in zip(h, cols):
    col.markdown(f"**{text}**")

# FILAS DEL REGISTRO (Ejemplos)
def linea_libro(aud, org, fecha, sujeto, nif, base, iva, ret, total, modelos):
    r = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    r[0].write("✅" if aud=="ok" else "⚠️")
    r[1].write(org)
    r[2].write(fecha)
    r[3].markdown(f"**{sujeto}** <br><small>{nif}</small>", unsafe_allow_html=True)
    r[4].write(f"{base}€")
    r[5].write(f"{iva}€")
    r[6].write(f"{ret}€" if ret != "-" else "-")
    r[7].write(f"**{total}€**")
    
    banderas = "".join([f'<span style="background:#3b82f6;color:white;padding:2px 4px;border-radius:3px;margin-right:2px;font-size:10px;">M-{m}</span>' for m in modelos])
    r[8].markdown(banderas, unsafe_allow_html=True)
    r[9].button("👁️", key=sujeto)

linea_libro("ok", "🇪🇸", "19/02", "BAR EL GRIEGO", "B12345678", "66.34", "6.63", "-", "72.97", ["303"])
linea_libro("ok", "🇪🇸", "18/02", "NACHO SEVILLA", "B99887766", "200.00", "42.00", "30.00", "212.00", ["303", "111"])
linea_libro("alert", "🇪🇺", "17/02", "ADOBE IE", "IE6362892H", "120.00", "0.00", "-", "120.00", ["303", "349"])

# --- LA LÍNEA DE TOTALES (DEBAJO DE CADA COLUMNA) ---
st.markdown('<div class="total-row">', unsafe_allow_html=True)
t = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
t[3].write("TOTALES CONTROL:")
t[4].write("386,34€") # Base debajo de Base
t[5].write("48,63€")  # IVA debajo de IVA
t[6].write("30,00€")  # Ret debajo de Ret
t[7].write("404,97€") # Total debajo de Total
st.markdown('</div>', unsafe_allow_html=True)
