import streamlit as st

# 1. SETUP SaaS (LG UltraWide Ready)
st.set_page_config(layout="wide", page_title="Búnker Pro | Auditoría Visual")

# Estilos para banderas, alertas y totales alineados
st.markdown("""
    <style>
    .total-line { background-color: #f1f5f9; font-weight: bold; border-top: 3px solid #3b82f6; padding: 12px 0; margin-top: 5px; }
    .badge-flag { font-size: 1.4rem; cursor: help; }
    .stNumberInput input { font-weight: bold; }
    .audit-alert { color: #ef4444; animation: blinker 2s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL SUPERIOR: ENTRADA Y VISOR ---
with st.container(border=True):
    col_pdf, col_ficha = st.columns([1.2, 1])
    
    with col_pdf:
        st.markdown("### 📄 Visor Documental")
        # Forzamos un visor que no falle y ocupe espacio real
        st.markdown('<div style="background:#e2e8f0; height:450px; border-radius:10px; display:flex; align-items:center; justify-content:center; border: 2px dashed #cbd5e1;">'
                    '<img src="https://img.freepik.com/vector-premium/plantilla-factura-negocios-diseno-plano-moderno_24908-59263.jpg" style="max-height:100%; border-radius:5px;">'
                    '</div>', unsafe_allow_html=True)
    
    with col_ficha:
        st.markdown("### ⚡ Validación de Asiento")
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.text_input("SUJETO / PROVEEDOR", value="ADOBE SYSTEMS IE")
        c2.text_input("NIF / VAT", value="IE6362892H")
        # Iconos directos para no leer letras
        c3.selectbox("ORIGEN", ["🇪🇸 Nacional", "🇪🇺 Intra", "🌎 Ext"], index=1)
        
        o1, o2, o3 = st.columns([1, 1, 1])
        o1.selectbox("OPERACIÓN", ["Soportado", "Inversión", "Suplido"])
        o2.text_input("CAT. GASTO", value="Software")
        o3.text_input("CTA. GASTO", value="629.00000")

        st.divider()
        # IVA EN EL MEDIO (Eje del pensamiento)
        i1, i2, i3 = st.columns([1.1, 0.8, 1.1])
        i1.number_input("BASE IMPONIBLE", value=120.00, format="%.2f")
        i2.selectbox("IVA %", [21, 10, 4, 0], index=3)
        i3.number_input("CUOTA IVA", value=0.00, format="%.2f")
        
        f1, f2 = st.columns([1, 1])
        f1.text_input("Nº FACTURA", value="FRA-2026-001")
        f2.number_input("💵 TOTAL FACTURA (€)", value=120.00, format="%.2f")
        st.button("🚀 CONTABILIZAR (ENTER)", use_container_width=True, type="primary")

st.write("###")

# --- PANEL INFERIOR: LIBRO DE REGISTRO SEGMENTADO ---
# Usamos Tabs para separar Recibidas, Emitidas e Inversiones sin perder espacio
tab_rec, tab_emi, tab_inv = st.tabs(["📥 RECIBIDAS", "📤 EMITIDAS", "⚙️ INVERSIONES"])

def dibujar_libro(tipo_data):
    # Filtros rápidos
    f1, f2, f3 = st.columns([1, 1, 3])
    f1.selectbox("TRIMESTRE", ["1T", "2T", "3T", "4T"], key=f"t_{tipo_data}")
    f2.selectbox("MODELO", ["Todos", "303", "111", "347", "349"], key=f"m_{tipo_data}")
    f3.text_input("🔍 Buscar en el diario...", key=f"s_{tipo_data}")

    # Cabecera Maestra
    h = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    labels = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]
    for col, lab in zip(h, labels): col.markdown(f"**{lab}**")

    # Filas con BANDERAS y AUDITORÍA
    def fila(audit, flag, fecha, nombre, nif, base, iva, ret, total, modelos):
        r = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
        r[0].write("✅" if audit=="ok" else "⚠️")
        r[1].markdown(f'<span class="badge-flag">{flag}</span>', unsafe_allow_html=True)
        r[2].write(fecha)
        r[3].markdown(f"**{nombre}** <br><small>{nif}</small>", unsafe_allow_html=True)
        r[4].write(f"{base}€")
        r[5].write(f"{iva}€")
        r[6].write(f"{ret}€" if ret != "-" else "-")
        r[7].write(f"**{total}€**")
        
        tags = "".join([f'<span style="background:#3b82f6;color:white;padding:2px 5px;border-radius:4px;margin-right:3px;font-size:10px;">M-{m}</span>' for m in modelos])
        r[8].markdown(tags, unsafe_allow_html=True)
        r[9].button("👁️", key=f"{tipo_data}_{nombre}")

    fila("ok", "🇪🇸", "19/02", "BAR EL GRIEGO", "B12345678", "66.34", "6.63", "-", "72.97", ["303"])
    fila("alert", "🇪🇺", "17/02", "ADOBE SYSTEMS", "IE6362892H", "120.00", "0.00", "-", "120.00", ["303", "349"])

    # TOTALES ALINEADOS (Verticalmente debajo de sus columnas)
    st.markdown('<div class="total-line">', unsafe_allow_html=True)
    t = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    t[3].write("TOTALES CUADRE:")
    t[4].write("186.34€") # Base
    t[5].write("6.63€")   # IVA
    t[6].write("0.00€")   # Ret
    t[7].write("192.97€") # Total
    st.markdown('</div>', unsafe_allow_html=True)

with tab_rec: dibujar_libro("REC")
with tab_emi: st.info("Módulo de facturación emitida sincronizado.")
with tab_inv: st.info("Control de amortizaciones y bienes de inversión.")
