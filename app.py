import streamlit as st
import pandas as pd
import numpy as np

# 1. INICIALIZACIÓN ABSOLUTA (Evita cualquier error en rojo)
if 'base' not in st.session_state: st.session_state.base = 1000.00
if 'iva_p' not in st.session_state: st.session_state.iva_p = 21
if 'ret_p' not in st.session_state: st.session_state.ret_p = 0
if 'isp' not in st.session_state: st.session_state.isp = False
if 'cuota' not in st.session_state: st.session_state.cuota = 210.00
if 'c_ret' not in st.session_state: st.session_state.c_ret = 0.00
if 'total' not in st.session_state: st.session_state.total = 1210.00

def sync():
    """Motor de cálculo que se activa al pulsar TAB"""
    st.session_state.cuota = round(st.session_state.base * (st.session_state.iva_p / 100), 2)
    st.session_state.c_ret = round(st.session_state.base * (st.session_state.ret_p / 100), 2)
    if st.session_state.isp:
        st.session_state.total = round(st.session_state.base - st.session_state.c_ret, 2)
    else:
        st.session_state.total = round(st.session_state.base + st.session_state.cuota - st.session_state.c_ret, 2)

# 2. CONFIGURACIÓN DE PANTALLA
st.set_page_config(layout="wide", page_title="Búnker Pro | Asesoría")

st.markdown("""
    <style>
    .asiento-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 0.9rem; }
    .asiento-table td, .asiento-table th { border: 1px solid #e2e8f0; padding: 8px; }
    .debe { color: #2563eb; text-align: right; font-weight: bold; }
    .haber { color: #dc2626; text-align: right; font-weight: bold; }
    .mod-card { background: #f8fafc; border: 1px solid #cbd5e1; padding: 15px; border-radius: 8px; text-align: center; }
    .total-line { background: #f1f5f9; font-weight: bold; border-top: 2px solid #3b82f6; padding: 12px 0; }
    </style>
    """, unsafe_allow_html=True)

# 3. NAVEGACIÓN POR PESTAÑAS
tab_rec, tab_emi, tab_modelos, tab_graficas = st.tabs(["📥 RECIBIDAS", "📤 EMITIDAS", "📋 ESTADO MODELOS", "📈 EVOLUCIÓN"])

# --- FUNCIÓN PARA RECIBIDAS/EMITIDAS ---
def render_registro(tipo):
    col_pdf, col_asiento, col_ficha = st.columns([1, 1, 1.2])
    with col_pdf:
        st.markdown("### 📄 Visor")
        st.markdown('<div style="background:#334155; height:350px; border-radius:8px; color:white; display:flex; align-items:center; justify-content:center;">PDF DRIVE</div>', unsafe_allow_html=True)
    
    with col_asiento:
        st.markdown("### ⚙️ Asiento Contable")
        isp_h = f"<tr><td>(477) IVA Rep (ISP)</td><td></td><td class='haber'>{st.session_state.cuota:,.2f}</td></tr>" if st.session_state.isp else ""
        ret_h = f"<tr><td>(475.1) Retenciones</td><td></td><td class='haber'>{st.session_state.c_ret:,.2f}</td></tr>" if st.session_state.ret_p > 0 else ""
        st.markdown(f"""
        <table class="asiento-table">
            <tr style="background:#f8fafc;"><th>Cuenta</th><th>Debe</th><th>Haber</th></tr>
            <tr><td>(629/700) Base</td><td class="debe">{st.session_state.base:,.2f}</td><td></td></tr>
            <tr><td>(472) IVA Sop</td><td class="debe">{st.session_state.cuota:,.2f}</td><td></td></tr>
            {isp_h} {ret_h}
            <tr style="background:#fff7ed;"><td><b>(410/430) Total</b></td><td></td><td class="haber"><b>{st.session_state.total:,.2f}</b></td></tr>
        </table>
        """, unsafe_allow_html=True)

    with col_ficha:
        st.markdown(f"### ⚡ Validación {tipo}")
        c1, c2, c3 = st.columns([2, 1, 0.5])
        c1.text_input("SUJETO", value="ADOBE SYSTEMS IE", key=f"suj_{tipo}")
        c2.text_input("NIF", value="IE6362892H", key=f"nif_{tipo}")
        c3.markdown("## 🇪🇺")
        
        o1, o2, o3 = st.columns(3)
        st.session_state.isp = o1.checkbox("ISP (Inversión)", value=st.session_state.isp, on_change=sync, key=f"isp_{tipo}")
        st.session_state.ret_p = o2.selectbox("RET %", [0, 7, 15, 19], index=[0, 7, 15, 19].index(st.session_state.ret_p), on_change=sync, key=f"ret_{tipo}")
        o3.text_input("CTA. TRÁFICO", value="410.0001", key=f"cta_{tipo}")
        
        st.divider()
        i1, i2, i3 = st.columns(3)
        st.session_state.base = i1.number_input("BASE", value=st.session_state.base, on_change=sync, format="%.2f", key=f"base_{tipo}")
        st.session_state.iva_p = i2.selectbox("IVA %", [21, 10, 4, 0], index=[21, 10, 4, 0].index(st.session_state.iva_p), on_change=sync, key=f"iva_{tipo}")
        st.session_state.total = i3.number_input("TOTAL", value=st.session_state.total, format="%.2f", key=f"tot_{tipo}")
        st.button("🚀 REGISTRAR (ENTER)", use_container_width=True, type="primary", key=f"btn_{tipo}")

    st.write("###")
    # LIBRO DE REGISTRO ALINEADO
    h_cols = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    headers = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]
    for col, head in zip(h_cols, headers): col.markdown(f"**{head}**")
    
    r_cols = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    r_cols[0].write("✅"); r_cols[1].markdown("### 🇪🇺"); r_cols[2].write("19/02")
    r_cols[3].markdown("ADOBE SYSTEMS<br><small>IE6362892H</small>", unsafe_allow_html=True)
    r_cols[4].write(f"{st.session_state.base:,.2f}€")
    r_cols[5].write(f"{st.session_state.cuota:,.2f}€")
    r_cols[6].write(f"{st.session_state.c_ret:,.2f}€" if st.session_state.c_ret > 0 else "-")
    r_cols[7].write(f"**{st.session_state.total:,.2f}€**")
    r_cols[8].markdown('<span style="background:#01579b; color:white; padding:2px 5px; border-radius:4px; font-size:10px;">303</span>', unsafe_allow_html=True)
    r_cols[9].button("👁️", key=f"vis_{tipo}")

    st.markdown('<div class="total-line">', unsafe_allow_html=True)
    t_cols = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    t_cols[3].write("SUMATORIOS CONTROL:")
    t_cols[4].write(f"{st.session_state.base:,.2f}€"); t_cols[5].write(f"{st.session_state.cuota:,.2f}€")
    t_cols[6].write(f"{st.session_state.c_ret:,.2f}€"); t_cols[7].write(f"{st.session_state.total:,.2f}€")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_rec: render_registro("RECIBIDAS")
with tab_emi: render_registro("EMITIDAS")

# --- PANTALLA: ESTADO MODELOS (Checklist visual) ---
with tab_modelos:
    st.header("🏁 Estado de Obligaciones del Trimestre")
    c1, c2, c3, c4, c5 = st.columns(5)
    mods = [("M-303", "✅ LISTO"), ("M-111", "⚠️ PENDIENTE"), ("M-115", "✅ LISTO"), ("M-349", "✅ LISTO"), ("M-347", "🔍 REVISIÓN")]
    for col, (m, s) in zip([c1, c2, c3, c4, c5], mods):
        col.markdown(f'<div class="mod-card"><h3>{m}</h3><p>{s}</p></div>', unsafe_allow_html=True)
    st.divider()
    st.error("IA Detecta: Adobe aparece en Recibidas sin bandera 🇪🇺. ¿Presentamos M-349?")

# --- PANTALLA: ANALÍTICA (Evolución de la empresa) ---
with tab_graficas:
    st.header("📈 Evolución del Negocio")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("Ingresos vs Gastos")
        st.line_chart(pd.DataFrame(np.random.randn(20, 2), columns=['Ingresos', 'Gastos']))
    with col_g2:
        st.subheader("Top Gastos por Cuenta")
        st.bar_chart(pd.DataFrame({"Base": [5000, 2400, 1200, 900]}, index=["600", "629", "621", "623"]))
