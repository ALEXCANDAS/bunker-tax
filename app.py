import streamlit as st
import pandas as pd

# 1. SETUP DE ALTA VELOCIDAD
st.set_page_config(layout="wide", page_title="Búnker Pro | Sistema Centralizado")

# Estilos de Auditoría y Banderas
st.markdown("""
    <style>
    .asiento-header { background: #1e293b; color: white; padding: 10px; font-weight: bold; border-radius: 8px 8px 0 0; }
    .asiento-table { width: 100%; border: 1px solid #e2e8f0; border-collapse: collapse; font-family: monospace; }
    .asiento-table td, .asiento-table th { padding: 8px; border: 1px solid #e2e8f0; }
    .debe { color: #2563eb; text-align: right; font-weight: bold; }
    .haber { color: #dc2626; text-align: right; font-weight: bold; }
    .total-row { background: #f1f5f9; font-weight: bold; border-top: 3px solid #3b82f6; padding: 15px 0; }
    .mod-badge { padding: 2px 8px; border-radius: 4px; color: white; font-weight: bold; font-size: 11px; margin-right: 4px; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO (REACTIVO AL TAB)
if 'base' not in st.session_state: st.session_state.base = 1000.00
if 'iva_p' not in st.session_state: st.session_state.iva_p = 21
if 'ret_p' not in st.session_state: st.session_state.ret_p = 0
if 'isp' not in st.session_state: st.session_state.isp = False

def update_finance():
    st.session_state.cuota_iva = round(st.session_state.base * (st.session_state.iva_p / 100), 2)
    st.session_state.cuota_ret = round(st.session_state.base * (st.session_state.ret_p / 100), 2)
    # Si es ISP, el IVA se autorrepercuted (no suma al total a pagar)
    if st.session_state.isp:
        st.session_state.total = round(st.session_state.base - st.session_state.cuota_ret, 2)
    else:
        st.session_state.total = round(st.session_state.base + st.session_state.cuota_iva - st.session_state.cuota_ret, 2)

if 'total' not in st.session_state: update_finance()

# 3. NAVEGACIÓN CENTRALIZADA
nav = st.sidebar.radio("📁 GESTIÓN DE FACTURACIÓN", ["📥 Recibidas", "📤 Emitidas", "📊 Control de Impuestos"])

# --- PANTALLA: RECIBIDAS / EMITIDAS (Diferenciadas por lógica) ---
if nav in ["📥 Recibidas", "📤 Emitidas"]:
    with st.container(border=True):
        col_doc, col_asiento, col_ficha = st.columns([1, 1, 1.2])
        
        with col_doc:
            st.markdown("### 📄 Documento (IA)")
            st.markdown('<div style="background:#334155; height:380px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white;">VISOR PDF (Metadata Activo)</div>', unsafe_allow_html=True)

        with col_asiento:
            st.markdown("### ⚙️ Asiento Contable")
            # Cuadro de asiento largo y aprovechado
            st.markdown('<div class="asiento-header">DIARIO PREVIO</div>', unsafe_allow_html=True)
            isp_html = f"<tr><td>(477) IVA Repercutido (ISP)</td><td></td><td class='haber'>{st.session_state.cuota_iva:,.2f}</td></tr>" if st.session_state.isp else ""
            ret_html = f"<tr><td>(475) Retenciones IRPF</td><td></td><td class='haber'>{st.session_state.cuota_ret:,.2f}</td></tr>" if st.session_state.ret_p > 0 else ""
            
            st.markdown(f"""
            <table class="asiento-table">
                <tr style="background:#f8fafc;"><th>Cuenta / Concepto</th><th>Debe</th><th>Haber</th></tr>
                <tr><td>(629/700) Base Imponible</td><td class="debe">{st.session_state.base:,.2f}</td><td></td></tr>
                <tr><td>(472) IVA Soportado</td><td class="debe">{st.session_state.cuota_iva:,.2f}</td><td></td></tr>
                {isp_html}
                {ret_html}
                <tr style="background:#fff7ed;"><td><b>(410/430) Total Factura</b></td><td></td><td class="haber"><b>{st.session_state.total:,.2f}</b></td></tr>
            </table>
            """, unsafe_allow_html=True)

        with col_ficha:
            st.markdown("### ⚡ Validación")
            c1, c2, c3 = st.columns([2, 1, 0.5])
            c1.text_input("SUJETO", value="ADOBE SYSTEMS IE")
            c2.text_input("NIF", value="IE6362892H")
            c3.markdown("## 🇪🇺") # Bandera visual de auditoría

            o1, o2, o3 = st.columns([1.2, 0.8, 1])
            st.session_state.isp = o1.checkbox("ISP (Inversión)", value=st.session_state.isp, on_change=update_finance)
            st.session_state.ret_p = o2.selectbox("RET %", [0, 7, 15, 19], key="ret_sel", on_change=update_finance)
            o3.text_input("CTA. TRÁFICO", value="410.00012")

            st.divider()
            i1, i2, i3 = st.columns([1.2, 0.8, 1.2])
            st.session_state.base = i1.number_input("BASE", value=st.session_state.base, on_change=update_finance, format="%.2f")
            st.session_state.iva_p = i2.selectbox("IVA %", [21, 10, 4, 0], key="iva_sel", on_change=update_finance)
            st.session_state.total = i3.number_input("TOTAL", value=st.session_state.total, format="%.2f")
            
            st.button("🚀 REGISTRAR (ENTER)", use_container_width=True, type="primary")

    # --- LIBRO DE REGISTRO ---
    st.subheader(f"📋 Libro de {nav}")
    lc = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    h_titles = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]
    for col, t in zip(lc, h_titles): col.markdown(f"**{t}**")

    # Fila de ejemplo con Flags e Iconos
    row = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    row[0].write("✅")
    row[1].markdown("### 🇪🇺")
    row[2].write("19/02")
    row[3].markdown(f"**ADOBE SYSTEMS** <br><small>IE6362892H</small>", unsafe_allow_html=True)
    row[4].write(f"{st.session_state.base:,.2f}€")
    row[5].write(f"{st.session_state.cuota_iva:,.2f}€")
    row[6].write(f"{st.session_state.cuota_ret:,.2f}€" if st.session_state.ret_p > 0 else "-")
    row[7].write(f"**{st.session_state.total:,.2f}€**")
    row[8].markdown('<span class="mod-badge" style="background:#01579b">303</span><span class="mod-badge" style="background:#166534">349</span>', unsafe_allow_html=True)
    row[9].button("👁️", key="vis_rec")

    # TOTALES ALINEADOS
    st.markdown('<div class="total-row">', unsafe_allow_html=True)
    tr = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    tr[3].write("SUMATORIOS CONTROL:")
    tr[4].write(f"{st.session_state.base:,.2f}€")
    tr[5].write(f"{st.session_state.cuota_iva:,.2f}€")
    tr[6].write(f"{st.session_state.cuota_ret:,.2f}€")
    tr[7].write(f"{st.session_state.total:,.2f}€")
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANTALLA: CONTROL DE IMPUESTOS (LA TERCERA PANTALLA) ---
elif nav == "📊 Control de Impuestos":
    st.header("📊 Liquidación y Cuadre de Modelos")
    
    # Resumen por Modelos
    m1, m2, m3 = st.columns(3)
    m1.metric("Modelo 303 (IVA)", f"{st.session_state.cuota_iva:,.2f}€", "A Compensar")
    m2.metric("Modelo 111 (Retenciones)", f"{st.session_state.cuota_ret:,.2f}€", "A Ingresar")
    m3.metric("Modelo 349 (Intra)", f"{st.session_state.base:,.2f}€", "Operaciones")

    st.divider()
    st.subheader("🔍 Punteo por Casillas (Simulación 303)")
    df_303 = pd.DataFrame({
        "Casilla": ["01", "07", "12", "28", "40"],
        "Concepto": ["Régimen General 21%", "Régimen General 10%", "ISP (Inversión Sujeto Pasivo)", "IVA Soportado Interior", "IVA Soportado Importaciones"],
        "Base Imponible": [0.00, 0.00, st.session_state.base if st.session_state.isp else 0, st.session_state.base if not st.session_state.isp else 0, 0.00],
        "Cuota": [0.00, 0.00, st.session_state.cuota_iva if st.session_state.isp else 0, st.session_state.cuota_iva if not st.session_state.isp else 0, 0.00]
    })
    st.table(df_303)
