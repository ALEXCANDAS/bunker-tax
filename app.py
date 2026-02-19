import streamlit as st

# 1. MOTOR DE CÁLCULO SIN FALLOS (REACTIVO)
if 'base' not in st.session_state: st.session_state.base = 100.00
if 'iva_p' not in st.session_state: st.session_state.iva_p = 21
if 'ret_p' not in st.session_state: st.session_state.ret_p = 0
if 'isp' not in st.session_state: st.session_state.isp = False

def recalcular():
    # Cálculo de cuotas con redondeo contable de 2 decimales
    st.session_state.cuota_iva = round(st.session_state.base * (st.session_state.iva_p / 100), 2)
    st.session_state.cuota_ret = round(st.session_state.base * (st.session_state.ret_p / 100), 2)
    
    # Si es ISP (Inversión Sujeto Pasivo), el IVA no suma al total de la factura
    if st.session_state.isp:
        st.session_state.total = round(st.session_state.base - st.session_state.cuota_ret, 2)
    else:
        st.session_state.total = round(st.session_state.base + st.session_state.cuota_iva - st.session_state.cuota_ret, 2)

# Inicializar cálculos si no existen
if 'cuota_iva' not in st.session_state: recalcular()

# 2. CONFIGURACIÓN DE PANTALLA (SIN NAMEERRORS)
st.set_page_config(layout="wide", page_title="Búnker Pro | Producción")

st.markdown("""
    <style>
    .asiento-box { background:#f1f5f9; border:1px solid #cbd5e1; border-radius:8px; padding:15px; font-family:monospace; font-size: 0.9rem; }
    .total-line { background:#f8fafc; font-weight:bold; border-top:3px solid #3b82f6; padding:10px 0; }
    .flag-icon { font-size: 1.8rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. INTERFAZ: PESTAÑAS PRIMERO PARA EVITAR ERRORES DE DEFINICIÓN
tab_rec, tab_emi, tab_ctrl = st.tabs(["📥 RECIBIDAS", "📤 EMITIDAS", "📋 CONTROL DE MODELOS"])

with tab_rec:
    col_pdf, col_ficha = st.columns([1.1, 1])
    
    with col_pdf:
        st.markdown("### 📄 Visor y Asiento")
        # Visualización dinámica del asiento antes de grabar
        st.markdown(f"""
        <div class="asiento-box">
        <b>⚙️ ASIENTO CONTABLE PREVIO:</b><br><br>
        (629) Gasto: {st.session_state.base:,.2f}€ (D)<br>
        (472) IVA Sop: {st.session_state.cuota_iva:,.2f}€ (D)<br>
        {"(477) IVA Rep (ISP): " + str(st.session_state.cuota_iva) + "€ (H)<br>" if st.session_state.isp else ""}
        {"(475) Retención: " + str(st.session_state.cuota_ret) + "€ (H)<br>" if st.session_state.ret_p > 0 else ""}
        (410) Acreedor: {st.session_state.total:,.2f}€ (H)
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.isp: st.warning("⚠️ INVERSIÓN SUJETO PASIVO: IVA Autorepercutido.")

    with col_ficha:
        # EL FORMULARIO MAESTRO (Captura el ENTER)
        with st.form("form_final", clear_on_submit=False):
            st.markdown("### ⚡ Validación de Metadatos")
            
            # Fila 1: Datos y Bandera (Reconocimiento visual 🇪🇺)
            c1, c2, c3 = st.columns([2, 1, 0.5])
            c1.text_input("PROVEEDOR", value="ADOBE SYSTEMS IE")
            c2.text_input("NIF", value="IE6362892H")
            c3.markdown("## 🇪🇺")

            # Fila 2: Control de Modelos
            o1, o2, o3 = st.columns([1.2, 0.8, 1])
            o1.checkbox("ISP (Inv. Sujeto Pasivo)", key="isp", on_change=recalcular)
            o2.selectbox("RET %", [0, 7, 15, 19], key="ret_p", on_change=recalcular)
            o3.text_input("CTA. GASTO", value="629.000")

            st.divider()

            # Fila 3: El Núcleo Económico (Reactivo al Tabulador)
            i1, i2, i3 = st.columns([1, 0.8, 1])
            i1.number_input("BASE IMPONIBLE", key="base", on_change=recalcular, format="%.2f")
            i2.selectbox("IVA %", [21, 10, 4, 0], key="iva_p", on_change=recalcular)
            i3.number_input("TOTAL FACTURA", key="total", format="%.2f")

            st.write("")
            # Botón que dispara el registro
            if st.form_submit_button("🚀 REGISTRAR (ENTER)", use_container_width=True, type="primary"):
                st.toast("Factura registrada en el libro.")

    # --- LIBRO DE REGISTRO / AUDITORÍA ---
    st.write("###")
    st.subheader("📋 Libro de Registro de Facturas")
    
    h = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    header_labels = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]
    for col, text in zip(h, header_labels): col.markdown(f"**{text}**")

    # Fila de ejemplo auditada con banderas e ISP
    r = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    r[0].write("✅")
    r[1].markdown("### 🇪🇺")
    r[2].write("19/02")
    r[3].markdown(f"**ADOBE SYSTEMS IE** " + ("<br><b>(ISP)</b>" if st.session_state.isp else ""), unsafe_allow_html=True)
    r[4].write(f"{st.session_state.base:,.2f}€")
    r[5].write(f"{st.session_state.cuota_iva:,.2f}€")
    r[6].write(f"{st.session_state.cuota_ret:,.2f}€" if st.session_state.ret_p > 0 else "-")
    r[7].write(f"**{st.session_state.total:,.2f}€**")
    
    # Iconos de modelos (303, 349...)
    r[8].markdown('<span style="background:#01579b;color:white;padding:2px 5px;border-radius:3px;font-size:11px;">303</span> '
                  '<span style="background:#2e7d32;color:white;padding:2px 5px;border-radius:3px;font-size:11px;">349</span>', unsafe_allow_html=True)
    r[9].button("👁️", key="btn_view")

    # TOTALES ALINEADOS (Verticalmente bajo sus columnas)
    st.markdown('<div class="total-line">', unsafe_allow_html=True)
    t = st.columns([0.4, 0.6, 0.8, 2.2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    t[3].write("TOTALES CUADRE:")
    t[4].write(f"{st.session_state.base:,.2f}€")
    t[5].write(f"{st.session_state.cuota_iva:,.2f}€")
    t[6].write(f"{st.session_state.cuota_ret:,.2f}€")
    t[7].write(f"{st.session_state.total:,.2f}€")
    st.markdown('</div>', unsafe_allow_html=True)
