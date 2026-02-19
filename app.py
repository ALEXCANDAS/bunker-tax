import streamlit as st
import pandas as pd

# 1. MOTOR DE CÁLCULO (Aislado de errores de formulario)
if 'base' not in st.session_state: st.session_state.base = 1000.00
if 'iva_p' not in st.session_state: st.session_state.iva_p = 21
if 'ret_p' not in st.session_state: st.session_state.ret_p = 0
if 'isp' not in st.session_state: st.session_state.isp = False

def recalcular():
    """Cálculo instantáneo al Tabulador. Sin errores de callback."""
    st.session_state.c_iva = round(st.session_state.base * (st.session_state.iva_p / 100), 2)
    st.session_state.c_ret = round(st.session_state.base * (st.session_state.ret_p / 100), 2)
    if st.session_state.isp:
        st.session_state.total = round(st.session_state.base - st.session_state.c_ret, 2)
    else:
        st.session_state.total = round(st.session_state.base + st.session_state.c_iva - st.session_state.c_ret, 2)

if 'c_iva' not in st.session_state: recalcular()

# 2. SETUP VISUAL (Limpieza de tablas y alineación)
st.set_page_config(layout="wide", page_title="Búnker Pro | Producción")

st.markdown("""
    <style>
    .asiento-table { width: 100%; border-collapse: collapse; font-family: 'Roboto Mono', monospace; font-size: 0.9rem; }
    .asiento-table th { background: #1e293b; color: white; padding: 10px; text-align: left; }
    .asiento-table td { padding: 8px 12px; border: 1px solid #e2e8f0; }
    .debe { color: #2563eb; text-align: right; font-weight: bold; width: 100px; }
    .haber { color: #dc2626; text-align: right; font-weight: bold; width: 100px; }
    .total-line { background: #f1f5f9; font-weight: bold; border-top: 3px solid #3b82f6; padding: 15px 0; margin-top: 5px; }
    .badge-349 { background: #166534; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-303 { background: #01579b; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; margin-right: 4px; }
    </style>
    """, unsafe_allow_html=True)

# 3. NAVEGACIÓN
tab_rec, tab_emi, tab_mods, tab_evo = st.tabs(["📥 RECIBIDAS", "📤 EMITIDAS", "📋 ESTADO MODELOS", "📈 EVOLUCIÓN"])

def render_workstation(tipo):
    # --- CABECERA DE ACCIÓN ---
    col_doc, col_asiento, col_ficha = st.columns([1, 1, 1.2])
    
    with col_doc:
        st.markdown("### 📄 Visor")
        st.markdown('<div style="background:#334155; height:360px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white;">DOCUMENTO PDF</div>', unsafe_allow_html=True)

    with col_asiento:
        st.markdown("### ⚙️ Asiento Contable (D/H)")
        # Construcción de tabla HTML limpia (evita el "descojone" de las capturas)
        isp_html = f"<tr><td>(477) IVA Repercutido (ISP)</td><td></td><td class='haber'>{st.session_state.c_iva:,.2f}</td></tr>" if st.session_state.isp else ""
        ret_html = f"<tr><td>(475.1) Retenciones IRPF</td><td></td><td class='haber'>{st.session_state.c_ret:,.2f}</td></tr>" if st.session_state.ret_p > 0 else ""
        
        st.markdown(f"""
        <table class="asiento-table">
            <thead><tr><th>Cuenta / Concepto</th><th>Debe</th><th>Haber</th></tr></thead>
            <tbody>
                <tr><td>(629/700) Base Imponible</td><td class="debe">{st.session_state.base:,.2f}</td><td></td></tr>
                <tr><td>(472) IVA Soportado</td><td class="debe">{st.session_state.c_iva:,.2f}</td><td></td></tr>
                {isp_html} {ret_html}
                <tr style="background:#f8fafc; border-top: 2px solid #1e293b;">
                    <td><b>(410/430) Total Factura</b></td><td></td><td class="haber">{st.session_state.total:,.2f}</td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

    with col_ficha:
        st.markdown(f"### ⚡ Validación {tipo}")
        c1, c2, c3 = st.columns([2, 1, 0.5])
        c1.text_input("SUJETO", value="ADOBE SYSTEMS IE", key=f"s_{tipo}")
        c2.text_input("NIF", value="IE6362892H", key=f"n_{tipo}")
        org = c3.selectbox("ORG", ["🇪🇸", "🇪🇺", "🌎"], index=1, key=f"o_{tipo}")

        o1, o2, o3 = st.columns([1.2, 0.8, 1])
        st.session_state.isp = o1.checkbox("ISP (Inversión)", value=st.session_state.isp, on_change=recalcular, key=f"i_{tipo}")
        st.session_state.ret_p = o2.selectbox("RET %", [0, 7, 15, 19], index=0, on_change=recalcular, key=f"r_{tipo}")
        o3.text_input("Nº FRA", value="2026-X01", key=f"f_{tipo}")

        st.divider()
        i1, i2, i3 = st.columns(3)
        st.session_state.base = i1.number_input("BASE", value=st.session_state.base, on_change=recalcular, format="%.2f", key=f"b_{tipo}")
        st.session_state.iva_p = i2.selectbox("IVA %", [21, 10, 4, 0], index=0, on_change=recalcular, key=f"v_{tipo}")
        st.session_state.total = i3.number_input("TOTAL (€)", value=st.session_state.total, on_change=recalcular, format="%.2f", key=f"t_{tipo}")
        
        st.button(f"🚀 REGISTRAR {tipo} (ENTER)", use_container_width=True, type="primary", key=f"btn_{tipo}")

    # --- LIBRO DE REGISTRO (ABAJO) ---
    st.write("###")
    st.subheader(f"📋 Libro de Registro ({tipo})")
    cols = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    h_labels = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]
    for col, label in zip(cols, h_labels): col.markdown(f"**{label}**")

    # Fila de ejemplo con Badges de Modelos
    r = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    r[0].write("✅"); r[1].markdown(f"### {org}"); r[2].write("19/02")
    r[3].markdown(f"**ADOBE SYSTEMS** <br><small>IE6362892H</small>", unsafe_allow_html=True)
    r[4].write(f"{st.session_state.base:,.2f}€"); r[5].write(f"{st.session_state.c_iva:,.2f}€")
    r[6].write(f"{st.session_state.c_ret:,.2f}€" if st.session_state.c_ret > 0 else "-")
    r[7].write(f"**{st.session_state.total:,.2f}€**")
    
    # Lógica de Modelos (303 + 349 si es UE)
    mod_html = '<span class="badge-303">303</span>'
    if org == "🇪🇺": mod_html += '<span class="badge-349">349</span>'
    r[8].markdown(mod_html, unsafe_allow_html=True)
    r[9].button("👁️", key=f"vis_btn_{tipo}")

    # TOTALES ALINEADOS
    st.markdown('<div class="total-line">', unsafe_allow_html=True)
    tr = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    tr[3].write("TOTALES CUADRE:")
    tr[4].write(f"{st.session_state.base:,.2f}€"); tr[5].write(f"{st.session_state.c_iva:,.2f}€")
    tr[6].write(f"{st.session_state.c_ret:,.2f}€"); tr[7].write(f"{st.session_state.total:,.2f}€")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_rec: render_workstation("RECIBIDAS")
with tab_emi: render_workstation("EMITIDAS")
with tab_mods:
    st.header("📋 Estado de Obligaciones del Trimestre")
    m1, m2, m3 = st.columns(3)
    m1.metric("303 (IVA)", f"{st.session_state.c_iva:,.2f}€", "Pendiente")
    m2.metric("349 (Intra)", f"{st.session_state.base:,.2f}€", "Operaciones")
    m3.metric("111 (Ret)", f"{st.session_state.c_ret:,.2f}€", "A Ingresar")
with tab_evo:
    st.header("📈 Evolución de BI")
    st.line_chart(pd.DataFrame([450, 1200, 800, 1500, st.session_state.base], columns=["Base Imponible"]))
