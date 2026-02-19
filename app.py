import streamlit as st
import pandas as pd
import numpy as np

# 1. CEREBRO CONTABLE (Inicialización a prueba de errores)
if 'base' not in st.session_state: st.session_state.base = 100.00
if 'iva_p' not in st.session_state: st.session_state.iva_p = 21
if 'ret_p' not in st.session_state: st.session_state.ret_p = 0
if 'isp' not in st.session_state: st.session_state.isp = False
if 'org' not in st.session_state: st.session_state.org = "🇪🇺"

def recalcular():
    """Motor de cálculo instantáneo. Sin formularios, sin latencia."""
    st.session_state.c_iva = round(st.session_state.base * (st.session_state.iva_p / 100), 2)
    st.session_state.c_ret = round(st.session_state.base * (st.session_state.ret_p / 100), 2)
    # Lógica ISP: El IVA no se paga al proveedor (autorrepercusión)
    if st.session_state.isp:
        st.session_state.total = round(st.session_state.base - st.session_state.c_ret, 2)
    else:
        st.session_state.total = round(st.session_state.base + st.session_state.c_iva - st.session_state.c_ret, 2)

if 'total' not in st.session_state: recalcular()

# 2. CONFIGURACIÓN VISUAL (LG ULTRAWIDE)
st.set_page_config(layout="wide", page_title="Búnker Pro | Producción")

st.markdown("""
    <style>
    .asiento-table { width: 100%; border-collapse: collapse; font-family: 'Roboto Mono', monospace; font-size: 0.9rem; }
    .asiento-table th { background: #1e293b; color: white; padding: 10px; text-align: left; }
    .asiento-table td { border: 1px solid #e2e8f0; padding: 10px; }
    .debe { color: #2563eb; text-align: right; font-weight: bold; }
    .haber { color: #dc2626; text-align: right; font-weight: bold; }
    .total-row { background: #f1f5f9; font-weight: bold; border-top: 3px solid #3b82f6; padding: 15px 0; margin-top: 5px; }
    .badge { padding: 2px 8px; border-radius: 4px; color: white; font-weight: bold; font-size: 11px; margin-right: 4px; }
    .b-303 { background: #01579b; } .b-349 { background: #166534; } .b-111 { background: #9a3412; }
    .mod-card { background: #f8fafc; border: 1px solid #cbd5e1; padding: 15px; border-radius: 8px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. NAVEGACIÓN CENTRALIZADA
tab_rec, tab_emi, tab_mods, tab_evo = st.tabs(["📥 RECIBIDAS", "📤 EMITIDAS", "📋 MODELOS", "📈 EVOLUCIÓN"])

def render_work_screen(tipo):
    # --- BLOQUE SUPERIOR: FICHA DE ACCIÓN ---
    col_pdf, col_asiento, col_ficha = st.columns([1, 1, 1.2])
    
    with col_pdf:
        st.markdown("### 📄 Documento")
        st.markdown('<div style="background:#334155; height:360px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white;">VISOR PDF (Drive Focus)</div>', unsafe_allow_html=True)

    with col_asiento:
        st.markdown("### ⚙️ Asiento Contable (D/H)")
        isp_row = f"<tr><td>(477) IVA Rep (ISP)</td><td></td><td class='haber'>{st.session_state.c_iva:,.2f}</td></tr>" if st.session_state.isp else ""
        ret_row = f"<tr><td>(475.1) Retención IRPF</td><td></td><td class='haber'>{st.session_state.c_ret:,.2f}</td></tr>" if st.session_state.ret_p > 0 else ""
        
        st.markdown(f"""
        <table class="asiento-table">
            <thead><tr><th>Cuenta / Concepto</th><th>Debe</th><th>Haber</th></tr></thead>
            <tbody>
                <tr><td>(629/700) Base Imponible</td><td class="debe">{st.session_state.base:,.2f}</td><td></td></tr>
                <tr><td>(472) IVA Soportado</td><td class="debe">{st.session_state.c_iva:,.2f}</td><td></td></tr>
                {isp_row} {ret_row}
                <tr style="background:#f8fafc;"><td><b>(410/430) Total Factura</b></td><td></td><td class="haber">{st.session_state.total:,.2f}</td></tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

    with col_ficha:
        st.markdown("### ⚡ Validación Rápida")
        c1, c2, c3 = st.columns([2, 1, 0.5])
        c1.text_input("SUJETO", value="ADOBE SYSTEMS IE", key=f"s_{tipo}")
        c2.text_input("NIF", value="IE6362892H", key=f"n_{tipo}")
        st.session_state.org = c3.selectbox("ORG", ["🇪🇸", "🇪🇺", "🌎"], key=f"o_{tipo}", index=1)

        o1, o2, o3 = st.columns([1.2, 0.8, 1])
        st.session_state.isp = o1.checkbox("ISP (Inversión)", value=st.session_state.isp, on_change=recalcular, key=f"i_{tipo}")
        st.session_state.ret_p = o2.selectbox("RET %", [0, 7, 15, 19], index=0, on_change=recalcular, key=f"r_{tipo}")
        o3.text_input("Nº FACTURA", value="2026-X01", key=f"f_{tipo}")

        st.divider()
        i1, i2, i3 = st.columns(3)
        st.session_state.base = i1.number_input("BASE", value=st.session_state.base, on_change=recalcular, format="%.2f", key=f"b_{tipo}")
        st.session_state.iva_p = i2.selectbox("IVA %", [21, 10, 4, 0], index=0, on_change=recalcular, key=f"v_{tipo}")
        st.session_state.total = i3.number_input("TOTAL (€)", value=st.session_state.total, on_change=recalcular, format="%.2f", key=f"t_{tipo}")
        
        st.button(f"🚀 REGISTRAR {tipo} (ENTER)", use_container_width=True, type="primary", key=f"btn_{tipo}")

    # --- BLOQUE INFERIOR: LIBRO DE REGISTRO ---
    st.write("###")
    st.subheader(f"📋 Libro de {tipo}")
    lc = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    for col, h in zip(lc, ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]):
        col.markdown(f"**{h}**")

    # Fila de ejemplo (Datos de Marina + IA)
    r = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    r[0].write("✅"); r[1].markdown(f"### {st.session_state.org}"); r[2].write("19/02")
    r[3].markdown("ADOBE SYSTEMS IE <br><small>IE6362892H</small>", unsafe_allow_html=True)
    r[4].write(f"{st.session_state.base:,.2f}€"); r[5].write(f"{st.session_state.c_iva:,.2f}€")
    r[6].write(f"{st.session_state.c_ret:,.2f}€" if st.session_state.c_ret > 0 else "-")
    r[7].write(f"**{st.session_state.total:,.2f}€**")
    
    # Auditoría visual de Modelos
    badges = '<span class="badge b-303">303</span>'
    if st.session_state.org == "🇪🇺": badges += '<span class="badge b-349">349</span>'
    if st.session_state.ret_p > 0: badges += '<span class="badge b-111">111</span>'
    r[8].markdown(badges, unsafe_allow_html=True); r[9].button("👁️", key=f"vbtn_{tipo}")

    # TOTALES ALINEADOS VERTICALMENTE
    st.markdown('<div class="total-row">', unsafe_allow_html=True)
    tr = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    tr[3].write("TOTALES CUADRE:"); tr[4].write(f"{st.session_state.base:,.2f}€")
    tr[5].write(f"{st.session_state.c_iva:,.2f}€"); tr[6].write(f"{st.session_state.c_ret:,.2f}€")
    tr[7].write(f"{st.session_state.total:,.2f}€")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_rec: render_work_screen("RECIBIDAS")
with tab_emi: render_work_screen("EMITIDAS")

with tab_mods:
    st.header("📋 Estado de Modelos (Trimestre Activo)")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown('<div class="mod-card"><h3>M-303</h3><p style="color:green;">LISTO</p></div>', unsafe_allow_html=True)
    c2.markdown('<div class="mod-card"><h3>M-111</h3><p style="color:orange;">PENDIENTE</p></div>', unsafe_allow_html=True)
    c3.markdown('<div class="mod-card"><h3>M-349</h3><p style="color:green;">LISTO</p></div>', unsafe_allow_html=True)
    c4.markdown('<div class="mod-card"><h3>M-390</h3><p style="color:blue;">ANUAL</p></div>', unsafe_allow_html=True)
    st.divider()
    st.info("💡 IA Sugiere: No olvides revisar las facturas intracomunitarias sin el Modelo 349 marcado.")

with tab_evo:
    st.header("📈 Evolución de la Empresa (BI)")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("Ingresos vs Gastos Mensuales")
        st.line_chart(pd.DataFrame(np.random.randn(12, 2), columns=['Ingresos', 'Gastos']))
    with col_g2:
        st.subheader("Top Proveedores / Clientes")
        st.bar_chart(pd.DataFrame({"Base": [5000, 3200, 1200, 800]}, index=["Cliente A", "Cliente B", "Adobe", "Amazon"]))
