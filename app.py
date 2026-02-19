import streamlit as st

# 1. MOTOR DE CÁLCULO BLINDADO (SIN ERRORES)
# Inicializamos el estado de sesión al principio para evitar el NameError
if 'base' not in st.session_state: st.session_state.base = 100.00
if 'iva_p' not in st.session_state: st.session_state.iva_p = 21
if 'ret_p' not in st.session_state: st.session_state.ret_p = 0
if 'isp' not in st.session_state: st.session_state.isp = False
if 'cuota_iva' not in st.session_state: st.session_state.cuota_iva = 21.00
if 'cuota_ret' not in st.session_state: st.session_state.cuota_ret = 0.00
if 'total' not in st.session_state: st.session_state.total = 121.00

def recalcular():
    # Cálculo con redondeo a 2 decimales
    st.session_state.cuota_iva = round(st.session_state.base * (st.session_state.iva_p / 100), 2)
    st.session_state.cuota_ret = round(st.session_state.base * (st.session_state.ret_p / 100), 2)
    
    # Lógica de Inversión del Sujeto Pasivo (ISP): El IVA no suma al total
    if st.session_state.isp:
        st.session_state.total = round(st.session_state.base - st.session_state.cuota_ret, 2)
    else:
        st.session_state.total = round(st.session_state.base + st.session_state.cuota_iva - st.session_state.cuota_ret, 2)

# 2. CONFIGURACIÓN DE PANTALLA (LG ULTRAWIDE READY)
st.set_page_config(layout="wide", page_title="Búnker Pro | Producción")

st.markdown("""
    <style>
    .asiento-box { background:#f1f5f9; border:1px solid #cbd5e1; border-radius:8px; padding:15px; font-family:monospace; }
    .total-line { background:#f8fafc; font-weight:bold; border-top:3px solid #3b82f6; padding:10px 0; }
    </style>
    """, unsafe_allow_html=True)

# 3. INTERFAZ: PESTAÑAS (DECLARADAS ANTES DE USARLAS PARA EVITAR EL NAMEERROR)
tab_rec, tab_emi, tab_ctrl = st.tabs(["📥 RECIBIDAS", "📤 EMITIDAS", "📋 CONTROL DE MODELOS"])

with tab_rec:
    col_pdf, col_ficha = st.columns([1.1, 1])
    
    with col_pdf:
        st.markdown("### 📄 Visor y Asiento")
        # Cuadro de Asiento Contable (D/H) para auditar el ISP
        st.markdown(f"""
        <div class="asiento-box">
        <b>⚙️ ASIENTO SUGERIDO (D/H):</b><br><br>
        (629) Gasto: {st.session_state.base:,.2f}€ (D)<br>
        (472) IVA Sop: {st.session_state.cuota_iva:,.2f}€ (D)<br>
        {"(477) IVA Rep (ISP): " + str(st.session_state.cuota_iva) + "€ (H)<br>" if st.session_state.isp else ""}
        {"(475) Retención: " + str(st.session_state.cuota_ret) + "€ (H)<br>" if st.session_state.ret_p > 0 else ""}
        (410) Acreedor: {st.session_state.total:,.2f}€ (H)
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.isp: st.warning("⚠️ ISP ACTIVO: IVA Autorepercutido (No suma al total).")

    with col_ficha:
        # FORMULARIO MAESTRO: Sacamos los on_change fuera del form para evitar el error de las capturas
        st.markdown("### ⚡ Validación de Factura")
        
        # Fila 1: Identificación y Bandera Real (🇪🇺 / 🇪🇸)
        c1, c2, c3 = st.columns([2, 1, 0.5])
        c1.text_input("PROVEEDOR", value="ADOBE SYSTEMS IE")
        c2.text_input("NIF", value="IE6362892H")
        c3.markdown("## 🇪🇺")

        # Fila 2: Control de Modelos (ISP y Retención)
        o1, o2, o3 = st.columns([1.2, 0.8, 1])
        st.session_state.isp = o1.checkbox("ISP (Inv. Sujeto Pasivo)", value=st.session_state.isp, on_change=recalcular)
        st.session_state.ret_p = o2.selectbox("RET %", [0, 7, 15, 19], index=[0, 7, 15, 19].index(st.session_state.ret_p), on_change=recalcular)
        o3.text_input("CTA. GASTO", value="629.000")

        st.divider()

        # Fila 3: El Núcleo Económico (IVA AL CENTRO Y REACTIVO)
        i1, i2, i3 = st.columns([1, 0.8, 1])
        st.session_state.base = i1.number_input("BASE IMPONIBLE", value=st.session_state.base, on_change=recalcular, format="%.2f")
        st.session_state.iva_p = i2.selectbox("IVA %", [21, 10, 4, 0], index=[21, 10, 4, 0].index(st.session_state.iva_p), on_change=recalcular)
        st.session_state.total = i3.number_input("TOTAL FACTURA", value=st.session_state.total, format="%.2f")

        st.write("")
        if st.button("🚀 REGISTRAR ASIENTO (ENTER)", use_container_width=True, type="primary"):
            st.success("Contabilizado con éxito.")

# --- PESTAÑA DE CONTROL: BANDERAS Y TOTALES ALINEADOS ---
with tab_ctrl:
    st.subheader("📋 Libro de Registro / Auditoría de Modelos")
    
    h = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    header_lbls = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]
    for col, text in zip(h, header_lbls): col.markdown(f"**{text}**")

    # FILA DE EJEMPLO ALINEADA CON BANDERAS
    r = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    r[0].write("✅")
    r[1].markdown("### 🇪🇺")
    r[2].write("19/02")
    r[3].markdown(f"**ADOBE SYSTEMS IE** <br><small>IE6362892H</small>", unsafe_allow_html=True)
    r[4].write(f"{st.session_state.base:,.2f}€")
    r[5].write(f"{st.session_state.cuota_iva:,.2f}€")
    r[6].write(f"{st.session_state.cuota_ret:,.2f}€" if st.session_state.ret_p > 0 else "-")
    r[7].write(f"**{st.session_state.total:,.2f}€**")
    
    # Banderas de modelos numéricas
    r[8].markdown('<span style="background:#01579b;color:white;padding:2px 5px;border-radius:3px;font-size:11px;">303</span> '
                  '<span style="background:#2e7d32;color:white;padding:2px 5px;border-radius:3px;font-size:11px;">349</span>', unsafe_allow_html=True)
    r[9].button("👁️", key="btn_view")

    # TOTALES ALINEADOS (Verticalmente debajo de sus columnas)
    st.markdown('<div class="total-line">', unsafe_allow_html=True)
    t = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    t[3].write("TOTALES CUADRE:")
    t[4].write(f"{st.session_state.base:,.2f}€")
    t[5].write(f"{st.session_state.cuota_iva:,.2f}€")
    t[6].write(f"{st.session_state.cuota_ret:,.2f}€")
    t[7].write(f"{st.session_state.total:,.2f}€")
    st.markdown('</div>', unsafe_allow_html=True)
