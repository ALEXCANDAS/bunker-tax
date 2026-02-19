import streamlit as st

# 1. CONFIGURACIÓN SaaS (Máximo aprovechamiento LG UltraWide)
st.set_page_config(layout="wide", page_title="Búnker Pro | Recibidas-Emitidas")

# CSS para congelar la estructura: Totales alineados y Banderas con estética SaaS
st.markdown("""
    <style>
    .total-line { background-color: #f8fafc; font-weight: bold; border-top: 3px solid #3b82f6; padding: 12px 0; margin-top: 10px; }
    .stNumberInput input { color: #1e293b; font-weight: bold; }
    .flag-audit { font-size: 1.3rem; margin-right: 5px; }
    .audit-alert { color: #ef4444; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. SELECTOR DE LIBRO (Emitidas / Recibidas)
libro_actual = st.sidebar.radio("📚 SELECCIONAR LIBRO", ["📥 Facturas Recibidas", "📤 Facturas Emitidas"])

# --- BLOQUE SUPERIOR: FICHA DE TRABAJO (IVA AL CENTRO) ---
# Esta es la pantalla de "picar" lo que no entra por metadatos
with st.container(border=True):
    col_pdf, col_ficha = st.columns([1.1, 1])
    with col_pdf:
        st.markdown("### 📄 Visor Documental")
        st.image("https://via.placeholder.com/850x380?text=FACTURA+DRIVE+FOCUS", use_container_width=True)
    
    with col_ficha:
        st.markdown(f"### ⚡ Registro de {libro_actual}")
        # Identificación con Banderas Reales
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.text_input("SUJETO / PROVEEDOR", value="ADOBE SYSTEMS IE")
        c2.text_input("NIF / VAT", value="IE6362892H")
        c3.selectbox("ORIGEN", ["🇪🇸 Nacional", "🇪🇺 Intra", "🌎 Ext"], index=1)
        
        # Tipo de Gasto/Ingreso y Operación (El centro de la ficha)
        o1, o2, o3 = st.columns([1.5, 1, 1.5])
        o1.selectbox("TIPO OPERACIÓN", ["Soportado Corriente", "Profesional", "Inversión"])
        o2.text_input("CTA. GASTO", value="629.00000")
        o3.text_input("Nº FACTURA", value="FRA-2026-X1")

        st.divider()

        # NÚCLEO ECONÓMICO (Reactivo y Alineado)
        i1, i2, i3 = st.columns([1.2, 0.8, 1])
        # Al cambiar TOTAL, la base y cuota saltan solas
        i2.selectbox("IVA %", [21, 10, 4, 0], index=3, key="iva_main")
        i1.number_input("BASE IMPONIBLE", value=120.00, format="%.2f")
        i3.number_input("CUOTA IVA", value=0.00, format="%.2f")
        
        st.number_input("💵 TOTAL FACTURA (€)", value=120.00, format="%.2f")
        st.button("🚀 CONTABILIZAR (ENTER)", use_container_width=True, type="primary")

st.write("###")

# --- BLOQUE INFERIOR: EL LIBRO DE REGISTRO (AUDITORÍA IA) ---
# Aquí es donde se conectan los metadatos y las facturas ya introducidas
st.subheader(f"📋 Libro de Registro de {libro_actual}")

# Filtros de Segmentación (Los "firmes" que pedías)
f1, f2, f3, f4 = st.columns([1, 1, 1, 3])
f_tri = f1.selectbox("TRIMESTRE", ["1T", "2T", "3T", "4T", "Anual"])
f_mod = f2.selectbox("MODELO", ["Todos", "303", "111", "347", "349"])
f_aud = f3.selectbox("AUDITORÍA", ["Todos", "Solo Alertas ⚠️", "Solo OK ✅"])
f_search = f4.text_input("🔍 Filtro rápido (NIF, Nombre, Cuenta...)", placeholder="Busca en el diario...")

# CABECERA MAESTRA (Alineada con totales)
h = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
headers = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "BANDERAS", "VIS"]
for col, text in zip(h, headers): col.markdown(f"**{text}**")

# FILAS DE EJEMPLO (Auditoría Humano-IA activa)
def draw_row(audit, flag, fecha, nombre, nif, base, iva, ret, total, modelos):
    r = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    r[0].write("✅" if audit=="ok" else "⚠️")
    r[1].markdown(f'<span class="flag-audit">{flag}</span>', unsafe_allow_html=True)
    r[2].write(fecha)
    r[3].markdown(f"**{nombre}** <br><small>{nif}</small>", unsafe_allow_html=True)
    r[4].write(f"{base}€")
    r[5].write(f"{iva}€")
    r[6].write(f"{ret}€" if ret != "-" else "-")
    r[7].write(f"**{total}€**")
    
    # Banderas por Colores
    tags = "".join([f'<span style="background:#3b82f6;color:white;padding:2px 5px;border-radius:4px;margin-right:3px;font-size:10px;">M-{m}</span>' for m in modelos])
    r[8].markdown(tags, unsafe_allow_html=True)
    r[9].button("👁️", key=nombre)

draw_row("ok", "🇪🇸", "19/02", "BAR EL GRIEGO", "B12345678", "66.34", "6.63", "-", "72.97", ["303"])
draw_row("alert", "🇪🇺", "17/02", "ADOBE SYSTEMS IE", "IE6362892H", "120.00", "0.00", "-", "120.00", ["303", "349"])

# --- LÍNEA DE TOTALES DE CONTROL (VERTICALMENTE ALINEADA) ---
st.markdown('<div class="total-line">', unsafe_allow_html=True)
t = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
t[3].write("TOTALES CUADRE:")
t[4].write("186,34€") # Debajo de BASE
t[5].write("6,63€")   # Debajo de IVA
t[6].write("0,00€")   # Debajo de RET
t[7].write("192,97€") # Debajo de TOTAL
st.markdown('</div>', unsafe_allow_html=True)
