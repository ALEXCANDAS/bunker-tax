import streamlit as st

# 1. SETUP ULTRA-WIDE (Aprovechamiento total LG)
st.set_page_config(layout="wide", page_title="Búnker Pro | Asesoría Real")

# CSS para congelar el diseño, mejorar el foco del Tabulador y las Banderas
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .stNumberInput input, .stTextInput input { font-size: 1.1rem !important; font-weight: bold !important; }
    .total-row { background-color: #f1f5f9; font-weight: bold; border-top: 2px solid #3b82f6; padding: 10px 0; }
    .audit-alert { color: #ef4444; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Lógica IA de detección rápida (Ej: Adobe -> UE -> 21% / Inversión)
def sugerir_datos(nombre):
    if "ADOBE" in nombre.upper():
        return {"nif": "IE6362892H", "iva": 21, "org": "🇪🇺", "cta": "629.00000"}
    return {"nif": "", "iva": 21, "org": "🇪🇸", "cta": "600.00000"}

# --- BLOQUE 1: ENTRADA DE DATOS (ARRIBA - VELOCIDAD PURA) ---
with st.container(border=True):
    col_pdf, col_ficha = st.columns([1.2, 1])
    
    with col_pdf:
        # Visor de documento real
        st.markdown('<iframe src="https://www.africau.edu/images/default/sample.pdf" width="100%" height="450px" style="border-radius:10px;"></iframe>', unsafe_allow_html=True)
    
    with col_ficha:
        st.markdown("### ⚡ Validación Rápida")
        # Fila 1: Identificación (El Tabulador debe fluir aquí)
        c1, c2, c3 = st.columns([2, 1, 0.5])
        prov = c1.text_input("PROVEEDOR", value="ADOBE SYSTEMS IE")
        nif = c2.text_input("NIF / VAT", value="IE6362892H")
        org = c3.markdown(f"## 🇪🇺") # Bandera visual grande de origen

        # Fila 2: Configuración (IA sugiere, tú validas)
        o1, o2, o3 = st.columns([1, 1, 1])
        o1.selectbox("TIPO", ["IVA Soportado", "Inversión", "Profesional"])
        o2.text_input("CAT. GASTO", value="Software")
        o3.text_input("CTA. GASTO", value="629.00000")

        st.divider()

        # Fila 3: El Núcleo (IVA en el centro - Reactividad Total)
        i1, i2, i3 = st.columns([1.2, 0.8, 1])
        base = i1.number_input("BASE IMPONIBLE", value=100.00, format="%.2f")
        iva_p = i2.selectbox("IVA %", [21, 10, 4, 0], index=0) # IA pone el 21%
        cuota = i3.number_input("CUOTA IVA", value=21.00, format="%.2f")
        
        # Fila 4: Cierre
        f1, f2 = st.columns([1, 1])
        f1.text_input("REFERENCIA / FRA", value="FRA-2026-001")
        total = f2.number_input("💵 TOTAL FACTURA (€)", value=121.00, format="%.2f")

        if st.button("🚀 CONTABILIZAR Y SIGUIENTE (ENTER)", use_container_width=True, type="primary"):
            st.toast("Asiento enviado al TSV.")

st.write("###")

# --- BLOQUE 2: LIBRO DE REGISTRO (ABAJO - AUDITORÍA CON BANDERAS) ---
st.subheader("📋 Libro de Registro / Auditoría de Modelos")

# Cabecera Maestra (Alineada con totales)
# Aud | Org | Fecha | Sujeto / NIF | Base | IVA | Ret | Total | Modelos | Ver
h = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
headers = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]
for col, text in zip(h, headers): col.markdown(f"**{text}**")

def fila_audit(audit, flag, fecha, nombre, nif, base, iva, ret, total, modelos):
    r = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    r[0].write("✅" if audit=="ok" else "⚠️")
    r[1].markdown(f"### {flag}") # Bandera grande en el registro
    r[2].write(fecha)
    r[3].markdown(f"**{nombre}** <br><small>{nif}</small>", unsafe_allow_html=True)
    r[4].write(f"{base}€")
    r[5].write(f"{iva}€")
    r[6].write(f"{ret}€" if ret != "-" else "-")
    r[7].write(f"**{total}€**")
    
    # Banderas de Modelos
    b_html = "".join([f'<span style="background:#3b82f6;color:white;padding:2px 4px;border-radius:3px;margin-right:2px;font-size:10px;">M-{m}</span>' for m in modelos])
    r[8].markdown(b_html, unsafe_allow_html=True)
    r[9].button("👁️", key=nombre)

# Ejemplo de Auditoría: Adobe (Intracomunitaria)
fila_audit("ok", "🇪🇺", "19/02", "ADOBE SYSTEMS IE", "IE6362892H", "100.00", "21.00", "-", "121.00", ["303", "349"])
fila_audit("ok", "🇪🇸", "18/02", "BAR EL GRIEGO", "B12345678", "66.34", "6.63", "-", "72.97", ["303"])

# --- LÍNEA DE TOTALES ALINEADA ---
st.markdown('<div class="total-row">', unsafe_allow_html=True)
t = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
t[3].write("TOTALES CUADRE:")
t[4].write("166,34€") # Debajo de BASE
t[5].write("27,63€")  # Debajo de IVA
t[6].write("0,00€")   # Debajo de RET
t[7].write("193,97€") # Debajo de TOTAL
st.markdown('</div>', unsafe_allow_html=True)
