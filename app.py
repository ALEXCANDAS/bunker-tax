import streamlit as st

# 1. MOTOR DE CÁLCULO (Blindado y Reactivo)
if 'base' not in st.session_state: st.session_state.base = 100.00
if 'iva_p' not in st.session_state: st.session_state.iva_p = 21
if 'ret_p' not in st.session_state: st.session_state.ret_p = 0
if 'isp' not in st.session_state: st.session_state.isp = False

def calcular():
    st.session_state.cuota_iva = round(st.session_state.base * (st.session_state.iva_p / 100), 2)
    st.session_state.cuota_ret = round(st.session_state.base * (st.session_state.ret_p / 100), 2)
    # Si es ISP, el IVA no suma al total a pagar
    if st.session_state.isp:
        st.session_state.total = round(st.session_state.base - st.session_state.cuota_ret, 2)
    else:
        st.session_state.total = round(st.session_state.base + st.session_state.cuota_iva - st.session_state.cuota_ret, 2)

if 'cuota_iva' not in st.session_state: calcular()

# 2. INTERFAZ SaaS PROFESIONAL (LG UltraWide)
st.set_page_config(layout="wide", page_title="Búnker Pro | Producción")

st.markdown("""
    <style>
    .asiento-box { background:#1e293b; color:#f8fafc; border-radius:8px; padding:15px; font-family:monospace; border:1px solid #334155; }
    .total-row { background:#f1f5f9; font-weight:bold; border-top:3px solid #3b82f6; padding:10px 0; }
    .mod-badge { background:#01579b; color:white; padding:2px 6px; border-radius:4px; font-weight:bold; font-size:11px; }
    .mod-349 { background:#166534; }
    .mod-111 { background:#9a3412; }
    </style>
    """, unsafe_allow_html=True)

# Pestañas para separar el ruido
tab_rec, tab_emi, tab_auditoria = st.tabs(["📥 RECIBIDAS", "📤 EMITIDAS", "📋 AUDITORÍA Y MODELOS"])

with tab_rec:
    # PANEL DE ACCIÓN
    with st.container(border=True):
        col_pdf, col_ficha = st.columns([1.1, 1])
        
        with col_pdf:
            st.markdown("### 📄 Visor y Asiento")
            st.markdown(f"""
            <div class="asiento-box">
            <b>🔍 PRE-ASIENTO (D/H):</b><br><br>
            (629) Gasto: {st.session_state.base:,.2f}€ (D)<br>
            (472) IVA Sop: {st.session_state.cuota_iva:,.2f}€ (D)<br>
            {"(477) IVA Rep (ISP): " + str(st.session_state.cuota_iva) + "€ (H)<br>" if st.session_state.isp else ""}
            {"(475) Retención: " + str(st.session_state.cuota_ret) + "€ (H)<br>" if st.session_state.ret_p > 0 else ""}
            (410) Acreedor: {st.session_state.total:,.2f}€ (H)
            </div>
            """, unsafe_allow_html=True)
            if st.session_state.isp: st.warning("💡 Inversión del Sujeto Pasivo activa.")

        with col_ficha:
            # Quitamos el FORM para que el on_change sea instantáneo al dar TAB
            st.markdown("### ⚡ Validación")
            c1, c2, c3 = st.columns([2, 1, 0.5])
            c1.text_input("PROVEEDOR", value="ADOBE SYSTEMS IE")
            c2.text_input("NIF / VAT", value="IE6362892H")
            c3.markdown("## 🇪🇺")

            o1, o2, o3 = st.columns([1.2, 0.8, 1])
            st.checkbox("ISP (Inversión)", key="isp", on_change=calcular)
            st.selectbox("RET %", [0, 7, 15, 19], key="ret_p", on_change=calcular)
            o3.text_input("CTA. GASTO", value="629.000")

            st.divider()

            # EL NÚCLEO (IVA EN EL MEDIO)
            i1, i2, i3 = st.columns([1, 0.8, 1])
            i1.number_input("BASE", key="base", on_change=calcular, format="%.2f")
            i2.selectbox("IVA %", [21, 10, 4, 0], key="iva_p", on_change=calcular)
            i3.number_input("CUOTA IVA", value=st.session_state.cuota_iva, format="%.2f")
            
            st.number_input("💵 TOTAL FACTURA", key="total", on_change=calcular, format="%.2f")
            
            if st.button("🚀 CONTABILIZAR ASIENTO (ENTER)", use_container_width=True, type="primary"):
                st.toast("Contabilizado.")

    # LIBRO DE REGISTRO (ABAJO)
    st.write("###")
    st.subheader("📋 Libro de Registro")
    h = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    headers = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]
    for col, text in zip(h, headers): col.markdown(f"**{text}**")

    # Fila de ejemplo con banderas e iconos numéricos
    r = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    r[0].write("✅")
    r[1].markdown("### 🇪🇺")
    r[2].write("19/02")
    r[3].markdown(f"**ADOBE SYSTEMS** <br><small>IE6362892H</small>", unsafe_allow_html=True)
    r[4].write(f"{st.session_state.base:,.2f}€")
    r[5].write(f"{st.session_state.cuota_iva:,.2f}€")
    r[6].write(f"{st.session_state.cuota_ret:,.2f}€" if st.session_state.ret_p > 0 else "-")
    r[7].write(f"**{st.session_state.total:,.2f}€**")
    r[8].markdown('<span class="mod-badge">303</span> <span class="mod-badge mod-349">349</span>', unsafe_allow_html=True)
    r[9].button("👁️", key="btn_view")

    # TOTALES ALINEADOS (DEBAJO DE SUS COLUMNAS)
    st.markdown('<div class="total-row">', unsafe_allow_html=True)
    t = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    t[3].write("TOTALES CUADRE:")
    t[4].write(f"{st.session_state.base:,.2f}€")
    t[5].write(f"{st.session_state.cuota_iva:,.2f}€")
    t[6].write(f"{st.session_state.cuota_ret:,.2f}€")
    t[7].write(f"{st.session_state.total:,.2f}€")
    st.markdown('</div>', unsafe_allow_html=True)
