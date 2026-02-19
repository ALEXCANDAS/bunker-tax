import streamlit as st
import pandas as pd

# 1. MOTOR DE ESTADO (Cerebro del Sistema)
# Inicialización para evitar que las variables "desaparezcan" entre clics
if 'base' not in st.session_state: st.session_state.base = 100.00
if 'iva_p' not in st.session_state: st.session_state.iva_p = 21
if 'ret_p' not in st.session_state: st.session_state.ret_p = 0
if 'isp' not in st.session_state: st.session_state.isp = False

def recalcular():
    """Calcula el asiento al segundo (al pulsar TAB o cambiar valor)"""
    st.session_state.c_iva = round(st.session_state.base * (st.session_state.iva_p / 100), 2)
    st.session_state.c_ret = round(st.session_state.base * (st.session_state.ret_p / 100), 2)
    
    if st.session_state.isp:
        # ISP: El IVA no se le paga al proveedor (Autorrepercusión)
        st.session_state.total = round(st.session_state.base - st.session_state.c_ret, 2)
    else:
        st.session_state.total = round(st.session_state.base + st.session_state.c_iva - st.session_state.c_ret, 2)

# Ejecución inicial para asegurar que el estado existe
if 'c_iva' not in st.session_state: recalcular()

# 2. CONFIGURACIÓN VISUAL
st.set_page_config(layout="wide", page_title="Búnker Pro | Auditoría Real")

st.markdown("""
    <style>
    .asiento-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 0.95rem; }
    .asiento-table th { background: #1e293b; color: white; padding: 10px; text-align: left; }
    .asiento-table td { padding: 10px; border-bottom: 1px solid #e2e8f0; }
    .debe { color: #2563eb; text-align: right; font-weight: bold; }
    .haber { color: #dc2626; text-align: right; font-weight: bold; }
    .badge { padding: 2px 8px; border-radius: 4px; color: white; font-weight: bold; font-size: 11px; margin-right: 4px; }
    .b-303 { background: #01579b; } .b-349 { background: #166534; } .b-111 { background: #9a3412; }
    .total-row { background: #f1f5f9; font-weight: bold; border-top: 3px solid #3b82f6; padding: 15px 0; }
    </style>
    """, unsafe_allow_html=True)

# 3. NAVEGACIÓN
tab_rec, tab_emi, tab_imp, tab_ana = st.tabs(["📥 RECIBIDAS", "📤 EMITIDAS", "📋 MODELOS", "📈 EVOLUCIÓN"])

def render_panel(tipo):
    col_pdf, col_asiento, col_ficha = st.columns([1, 1, 1.2])
    
    with col_pdf:
        st.markdown("### 📄 Visor")
        st.markdown('<div style="background:#334155; height:360px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white;">VISOR PDF ACTIVO</div>', unsafe_allow_html=True)

    with col_asiento:
        st.markdown("### ⚙️ Asiento Contable (D/H)")
        # Construimos la tabla de asiento dinámica
        isp_row = f"<tr><td>(477) IVA Rep. (ISP)</td><td></td><td class='haber'>{st.session_state.c_iva:,.2f}</td></tr>" if st.session_state.isp else ""
        ret_row = f"<tr><td>(475.1) Retención IRPF</td><td></td><td class='haber'>{st.session_state.c_ret:,.2f}</td></tr>" if st.session_state.ret_p > 0 else ""
        
        st.markdown(f"""
        <table class="asiento-table">
            <thead><tr><th>Cuenta / Concepto</th><th>Debe</th><th>Haber</th></tr></thead>
            <tbody>
                <tr><td>(629/700) Base Imponible</td><td class="debe">{st.session_state.base:,.2f}</td><td></td></tr>
                <tr><td>(472) IVA Soportado</td><td class="debe">{st.session_state.c_iva:,.2f}</td><td></td></tr>
                {isp_row} {ret_row}
                <tr style="background:#f8fafc;"><td><b>(410/430) Total</b></td><td></td><td class="haber">{st.session_state.total:,.2f}</td></tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

    with col_ficha:
        st.markdown(f"### ⚡ Validación {tipo}")
        c1, c2, c3 = st.columns([2, 1, 0.5])
        c1.text_input("SUJETO", value="ADOBE SYSTEMS IE", key=f"s_{tipo}")
        c2.text_input("NIF", value="IE6362892H", key=f"n_{tipo}")
        org = c3.selectbox("ORG", ["🇪🇸", "🇪🇺", "🌎"], key=f"o_{tipo}", index=1)

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

    # --- LIBRO DE REGISTRO (ABAJO) ---
    st.write("###")
    st.subheader(f"📋 Libro de {tipo}")
    lc = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    for col, h in zip(lc, ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]):
        col.markdown(f"**{h}**")

    r = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    r[0].write("✅"); r[1].markdown(f"### {org}"); r[2].write("19/02")
    r[3].markdown("ADOBE SYSTEMS <br><small>IE6362892H</small>", unsafe_allow_html=True)
    r[4].write(f"{st.session_state.base:,.2f}€"); r[5].write(f"{st.session_state.c_iva:,.2f}€")
    r[6].write(f"{st.session_state.c_ret:,.2f}€" if st.session_state.c_ret > 0 else "-")
    r[7].write(f"**{st.session_state.total:,.2f}€**")
    
    badges = '<span class="badge b-303">303</span>'
    if org == "🇪🇺": badges += '<span class="badge b-349">349</span>'
    r[8].markdown(badges, unsafe_allow_html=True); r[9].button("👁️", key=f"vbtn_{tipo}")

    st.markdown('<div class="total-row">', unsafe_allow_html=True)
    tr = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    tr[3].write("TOTALES CUADRE:"); tr[4].write(f"{st.session_state.base:,.2f}€")
    tr[5].write(f"{st.session_state.c_iva:,.2f}€"); tr[7].write(f"{st.session_state.total:,.2f}€")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_rec: render_panel("RECIBIDAS")
with tab_emi: render_panel("EMITIDAS")
with tab_imp:
    st.header("📋 Estado de Modelos")
    c1, c2, c3 = st.columns(3)
    c1.metric("303 (IVA)", f"{st.session_state.c_iva}€", "Pendiente")
    c2.metric("111 (Ret)", f"{st.session_state.c_ret}€", "Ingresar")
    c3.metric("349 (Intra)", f"{st.session_state.base}€", "Operado")
with tab_ana:
    st.header("📈 Evolución de BI")
    st.line_chart(pd.DataFrame([120, 450, 300, 1000, st.session_state.base], columns=["Base Imponible"]))
