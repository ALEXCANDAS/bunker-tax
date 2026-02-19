import streamlit as st
import pandas as pd

# 1. MOTOR DE ESTADO (Cerebro Central - Sin errores de carga)
if 'base' not in st.session_state: st.session_state.base = 1000.00
if 'iva_p' not in st.session_state: st.session_state.iva_p = 21
if 'ret_p' not in st.session_state: st.session_state.ret_p = 0
if 'isp' not in st.session_state: st.session_state.isp = False
if 'org' not in st.session_state: st.session_state.org = "🇪🇺 UE"

def sync_finances():
    """Cálculo instantáneo al pulsar TAB o cambiar valores."""
    st.session_state.cuota_iva = round(st.session_state.base * (st.session_state.iva_p / 100), 2)
    st.session_state.cuota_ret = round(st.session_state.base * (st.session_state.ret_p / 100), 2)
    if st.session_state.isp:
        # Lógica ISP: IVA Autorrepercuted (no suma al total a pagar)
        st.session_state.total = round(st.session_state.base - st.session_state.cuota_ret, 2)
    else:
        st.session_state.total = round(st.session_state.base + st.session_state.cuota_iva - st.session_state.cuota_ret, 2)

if 'total' not in st.session_state: sync_finances()

# 2. CONFIGURACIÓN VISUAL (LG UltraWide)
st.set_page_config(layout="wide", page_title="Búnker Pro | Auditoría Real")

st.markdown("""
    <style>
    /* Tabla de Asiento Profesional */
    .asiento-table { width: 100%; border-collapse: collapse; font-family: 'Roboto Mono', monospace; font-size: 0.9rem; margin-bottom: 20px; }
    .asiento-table th { background: #1e293b; color: white; padding: 10px; text-align: left; border: 1px solid #334155; }
    .asiento-table td { padding: 10px; border: 1px solid #e2e8f0; }
    .debe { color: #2563eb; text-align: right; font-weight: bold; width: 80px; }
    .haber { color: #dc2626; text-align: right; font-weight: bold; width: 80px; }
    
    /* Badges de Modelos y Auditoría */
    .badge { padding: 3px 8px; border-radius: 4px; color: white; font-weight: bold; font-size: 11px; margin-right: 5px; }
    .badge-303 { background: #01579b; }
    .badge-349 { background: #166534; }
    .badge-111 { background: #9a3412; }
    .total-row { background: #f1f5f9; font-weight: bold; border-top: 3px solid #3b82f6; padding: 15px 0; }
    </style>
    """, unsafe_allow_html=True)

# 3. INTERFAZ: PESTAÑAS (Recibidas, Emitidas, Modelos, Evolución)
tab_rec, tab_emi, tab_ctrl, tab_evo = st.tabs(["📥 RECIBIDAS", "📤 EMITIDAS", "📋 MODELOS", "📈 EVOLUCIÓN"])

def render_form(tipo):
    col_pdf, col_asiento, col_ficha = st.columns([1, 1, 1.2])
    
    with col_pdf:
        st.markdown("### 📄 Visor")
        st.markdown('<div style="background:#334155; height:360px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white;">VISOR PDF (Focus Activo)</div>', unsafe_allow_html=True)

    with col_asiento:
        st.markdown("### ⚙️ Asiento Contable (D/H)")
        # Lógica de filas dinámica para el Asiento
        isp_row = f"<tr><td>(477) IVA Repercutido (ISP)</td><td></td><td class='haber'>{st.session_state.cuota_iva:,.2f}</td></tr>" if st.session_state.isp else ""
        ret_row = f"<tr><td>(475) Retenciones IRPF</td><td></td><td class='haber'>{st.session_state.cuota_ret:,.2f}</td></tr>" if st.session_state.ret_p > 0 else ""
        
        st.markdown(f"""
        <table class="asiento-table">
            <thead><tr><th>Cuenta / Concepto</th><th>Debe</th><th>Haber</th></tr></thead>
            <tbody>
                <tr><td>(629/700) Base Imponible</td><td class="debe">{st.session_state.base:,.2f}</td><td></td></tr>
                <tr><td>(472) IVA Soportado</td><td class="debe">{st.session_state.cuota_iva:,.2f}</td><td></td></tr>
                {isp_row} {ret_row}
                <tr style="background:#f8fafc;"><td><b>(410/430) Total Factura</b></td><td></td><td class="haber">{st.session_state.total:,.2f}</td></tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

    with col_ficha:
        st.markdown(f"### ⚡ Validación {tipo}")
        c1, c2, c3 = st.columns([2, 1, 0.5])
        c1.text_input("SUJETO", value="ADOBE SYSTEMS IE", key=f"s_{tipo}")
        c2.text_input("NIF", value="IE6362892H", key=f"n_{tipo}")
        # Auditoría de Bandera: Si es Adobe, forzamos bandera UE
        st.session_state.org = c3.selectbox("ORG", ["🇪🇸 ES", "🇪🇺 UE", "🌎 EX"], index=1, key=f"o_{tipo}")

        o1, o2, o3 = st.columns([1.2, 0.8, 1])
        st.session_state.isp = o1.checkbox("ISP (Inversión)", value=st.session_state.isp, on_change=sync_finances, key=f"i_{tipo}")
        st.session_state.ret_p = o2.selectbox("RET %", [0, 7, 15, 19], index=[0, 7, 15, 19].index(st.session_state.ret_p), on_change=sync_finances, key=f"r_{tipo}")
        o3.text_input("Nº FRA", value="2026-X01", key=f"f_{tipo}")

        st.divider()
        i1, i2, i3 = st.columns(3)
        st.session_state.base = i1.number_input("BASE", value=st.session_state.base, on_change=sync_finances, format="%.2f", key=f"b_{tipo}")
        st.session_state.iva_p = i2.selectbox("IVA %", [21, 10, 4, 0], index=0, on_change=sync_finances, key=f"v_{tipo}")
        st.session_state.total = i3.number_input("TOTAL (€)", value=st.session_state.total, on_change=sync_finances, format="%.2f", key=f"t_{tipo}")
        
        st.button(f"🚀 REGISTRAR {tipo} (ENTER)", use_container_width=True, type="primary", key=f"btn_{tipo}")

    # --- LIBRO DE REGISTRO (ABAJO) ---
    st.write("###")
    st.subheader(f"📋 Libro de {tipo}")
    lc = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    h_titles = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]
    for col, t in zip(lc, h_titles): col.markdown(f"**{t}**")

    # Fila de ejemplo con 349 recuperado
    row = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    row[0].write("✅")
    row[1].markdown(f"### {st.session_state.org[:2]}")
    row[2].write("19/02")
    row[3].markdown(f"**ADOBE SYSTEMS** <br><small>IE6362892H</small>", unsafe_allow_html=True)
    row[4].write(f"{st.session_state.base:,.2f}€")
    row[5].write(f"{st.session_state.cuota_iva:,.2f}€")
    row[6].write(f"{st.session_state.cuota_ret:,.2f}€" if st.session_state.ret_p > 0 else "-")
    row[7].write(f"**{st.session_state.total:,.2f}€**")
    
    # Badges de Modelos (349 condicional a la bandera UE)
    badges = '<span class="badge badge-303">303</span>'
    if "🇪🇺" in st.session_state.org: badges += '<span class="badge badge-349">349</span>'
    if st.session_state.ret_p > 0: badges += '<span class="badge badge-111">111</span>'
    row[8].markdown(badges, unsafe_allow_html=True)
    row[9].button("👁️", key=f"vis_{tipo}")

    # TOTALES ALINEADOS VERTICALMENTE
    st.markdown('<div class="total-row">', unsafe_allow_html=True)
    tr = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    tr[3].write("TOTALES CUADRE:")
    tr[4].write(f"{st.session_state.base:,.2f}€"); tr[5].write(f"{st.session_state.cuota_iva:,.2f}€")
    tr[6].write(f"{st.session_state.cuota_ret:,.2f}€"); tr[7].write(f"{st.session_state.total:,.2f}€")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_rec: render_form("RECIBIDAS")
with tab_emi: render_form("EMITIDAS")

# --- PESTAÑA: MODELOS (Visión Global) ---
with tab_ctrl:
    st.header("📋 Estado de Modelos del Trimestre")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("303 (IVA)", f"{st.session_state.cuota_iva:,.2f}€", "A Compensar")
    m2.metric("349 (Intra)", f"{st.session_state.base:,.2f}€", "Operaciones")
    m3.metric("111 (Ret)", f"{st.session_state.cuota_ret:,.2f}€", "A Ingresar")
    m4.metric("390 (Anual)", "Cuadrado ✅", delta_color="normal")
    st.divider()
    st.info("💡 Sugerencia IA: Todas las facturas con origen UE están asignadas al Modelo 349.")

# --- PESTAÑA: EVOLUCIÓN (Analítica de Gasto) ---
with tab_evo:
    st.header("📈 Evolución de BI por Cliente / Cuenta")
    col_a, col_b = st.columns(2)
    col_a.line_chart(pd.DataFrame([1200, 1500, 1100, 1800, st.session_state.base], columns=["Base Imponible"]))
    col_b.bar_chart(pd.DataFrame({"Base": [st.session_state.base, 450, 800, 1200]}, index=["Adobe", "Amazon", "Movistar", "Alquiler"]))
