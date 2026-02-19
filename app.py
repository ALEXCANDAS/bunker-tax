import streamlit as st

# 1. CONFIGURACIÓN TÉCNICA (LG UltraWide Ready)
st.set_page_config(layout="wide", page_title="Búnker Pro | Producción Final")

# CSS para congelar el diseño y alinear totales verticalmente
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .total-row { background-color: #f1f5f9; font-weight: bold; border-top: 2px solid #3b82f6; padding: 10px 0; margin-top: 5px; }
    .stNumberInput, .stTextInput { margin-bottom: -10px; }
    .badge-iso { font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- BLOQUE SUPERIOR: PANEL DE TRABAJO (ENTRADA RÁPIDA) ---
with st.container(border=True):
    col_pdf, col_ficha = st.columns([1.1, 1])
    
    with col_pdf:
        st.markdown("### 📄 Documento")
        st.image("https://via.placeholder.com/800x350?text=VISOR+PDF+DRIVE", use_container_width=True)
    
    with col_ficha:
        st.markdown("### 📝 Ficha de Entrada")
        # Identificación
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.text_input("PROVEEDOR", value="ADOBE SYSTEMS IE", key="p_name")
        c2.text_input("NIF", value="IE6362892H", key="p_nif")
        c3.selectbox("ORIGEN", ["🇪🇸 España", "🇪🇺 UE", "🌎 Ext"], index=1, key="p_org")
        
        # Configuración Central
        op1, op2, op3 = st.columns([1, 1, 1])
        op1.selectbox("OPERACIÓN", ["Soportado", "Inversión"], key="p_op")
        op2.text_input("CATEGORÍA", value="Software", key="p_cat")
        op3.text_input("CTA. GASTO", value="629.00000", key="p_cta")
        
        st.divider()
        
        # Núcleo Económico (IVA en el centro y Reactivo)
        i1, i2, i3 = st.columns([1, 0.8, 1])
        # Al cambiar TOTAL abajo, estos deben recalcularse (Lógica interna del SaaS)
        i1.number_input("BASE", value=120.00, key="p_base", format="%.2f")
        i2.selectbox("IVA %", [21, 10, 4, 0], index=3, key="p_iva")
        i3.number_input("CUOTA IVA", value=0.00, key="p_cuota", format="%.2f")
        
        # Cierre
        f1, f2 = st.columns([1, 1])
        f1.text_input("Nº FACTURA", value="FRA-2026-001", key="p_ref")
        f2.number_input("💵 TOTAL FACTURA", value=120.00, key="p_total", format="%.2f")
        
        st.button("🚀 CONTABILIZAR Y SIGUIENTE (ENTER)", use_container_width=True, type="primary")

st.write("###")

# --- BLOQUE INFERIOR: LIBRO DE REGISTRO / AUDITORÍA ---
st.subheader("📋 Libro de Registro (Recibidas / Emitidas)")

# Filtros de Segmentación
f_c1, f_c2, f_c3 = st.columns([1, 1, 3])
f_c1.selectbox("LIBRO", ["Recibidas", "Emitidas"], key="f_libro")
f_c2.selectbox("TRIMESTRE", ["1T", "2T", "3T", "4T"], key="f_tri")
f_c3.text_input("🔍 Buscar NIF o Nombre...", key="f_search")

# Cabecera de Auditoría
# Audit | Org | Fecha | Sujeto / NIF | Base | IVA | Ret | Total | Modelos | Ver
h = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
headers = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]
for col, text in zip(h, headers):
    col.markdown(f"**{text}**")

# Línea de ejemplo con bandera y auditoría de IA (Caso Marina)
def row(aud, org, fecha, sujeto, nif, base, iva, ret, total, modelos):
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

row("ok", "🇪🇸", "19/02", "BAR EL GRIEGO", "B12345678", "66.34", "6.63", "-", "72.97", ["303"])
row("alert", "🇪🇺", "17/02", "ADOBE IE", "IE6362892H", "120.00", "0.00", "-", "120.00", ["303", "349"])

# --- TOTALES ALINEADOS (Lo que pedías para el 390/303) ---
st.markdown('<div class="total-row">', unsafe_allow_html=True)
t = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
t[3].write("TOTALES CUADRE:")
t[4].write("186,34€") # Debajo de Base
t[5].write("6,63€")   # Debajo de IVA
t[6].write("0,00€")   # Debajo de Ret
t[7].write("192,97€") # Debajo de Total
st.markdown('</div>', unsafe_allow_html=True)
