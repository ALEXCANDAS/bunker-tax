import streamlit as st

# 1. MOTOR DE CÁLCULO CONTABLE (REACTIVIDAD PURA)
if 'base' not in st.session_state: st.session_state.base = 100.00
if 'iva_p' not in st.session_state: st.session_state.iva_p = 21
if 'ret_p' not in st.session_state: st.session_state.ret_p = 0
if 'isp' not in st.session_state: st.session_state.isp = False

def recalcular():
    # IVA y Retención
    st.session_state.cuota_iva = round(st.session_state.base * (st.session_state.iva_p / 100), 2)
    st.session_state.cuota_ret = round(st.session_state.base * (st.session_state.ret_p / 100), 2)
    # Lógica ISP: IVA no suma al total a pagar al acreedor
    if st.session_state.isp:
        st.session_state.total = round(st.session_state.base - st.session_state.cuota_ret, 2)
    else:
        st.session_state.total = round(st.session_state.base + st.session_state.cuota_iva - st.session_state.cuota_ret, 2)

if 'cuota_iva' not in st.session_state: recalcular()

# 2. CONFIGURACIÓN VISUAL (LG ULTRAWIDE)
st.set_page_config(layout="wide", page_title="Búnker Pro | Auditoría Total")

st.markdown("""
    <style>
    .asiento-table { width: 100%; border-collapse: collapse; font-family: 'Roboto Mono', monospace; font-size: 0.85rem; }
    .asiento-table th { background: #1e293b; color: white; padding: 5px; text-align: left; }
    .asiento-table td { border-bottom: 1px solid #e2e8f0; padding: 5px; }
    .debe { color: #2563eb; text-align: right; font-weight: bold; }
    .haber { color: #dc2626; text-align: right; font-weight: bold; }
    .total-row { background-color: #f1f5f9; font-weight: bold; border-top: 2px solid #3b82f6; padding: 12px 0; margin-top: 5px; }
    .mod-badge { background:#01579b; color:white; padding:2px 6px; border-radius:4px; font-weight:bold; font-size:11px; margin-right:3px; }
    .mod-349 { background:#166534; } .mod-111 { background:#9a3412; }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL SUPERIOR: ACCIÓN Y ASIENTO ---
with st.container(border=True):
    col_pdf, col_asiento, col_ficha = st.columns([1, 0.8, 1.2])
    
    with col_pdf:
        st.markdown("### 📄 Documento")
        st.markdown('<div style="background:#334155; height:320px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white;">Visor PDF Activo</div>', unsafe_allow_html=True)

    with col_asiento:
        st.markdown("### ⚙️ Asiento Contable")
        # Tabla de Asiento Profesional (Aprovechando la pantalla)
        isp_row = f"<tr><td>(477) IVA Rep (ISP)</td><td></td><td class='haber'>{st.session_state.cuota_iva:,.2f}</td></tr>" if st.session_state.isp else ""
        ret_row = f"<tr><td>(475) Retención IRPF</td><td></td><td class='haber'>{st.session_state.cuota_ret:,.2f}</td></tr>" if st.session_state.ret_p > 0 else ""
        
        st.markdown(f"""
        <table class="asiento-table">
            <thead><tr><th>Cuenta / Concepto</th><th>Debe</th><th>Haber</th></tr></thead>
            <tbody>
                <tr><td>(629) Gasto Corriente</td><td class="debe">{st.session_state.base:,.2f}</td><td></td></tr>
                <tr><td>(472) IVA Soportado</td><td class="debe">{st.session_state.cuota_iva:,.2f}</td><td></td></tr>
                {isp_row}
                {ret_row}
                <tr><td>(410) Acreedor/Prov.</td><td></td><td class="haber">{st.session_state.total:,.2f}</td></tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)
        if st.session_state.isp: st.caption("⚠️ Operación con Inversión del Sujeto Pasivo")

    with col_ficha:
        st.markdown("### ⚡ Validación Rápida")
        c1, c2, c3 = st.columns([2, 1, 0.5])
        c1.text_input("PROVEEDOR", value="ADOBE SYSTEMS IE")
        c2.text_input("NIF / VAT", value="IE6362892H")
        c3.markdown("## 🇪🇺") # Bandera para auditoría de origen

        o1, o2, o3 = st.columns([1.2, 0.8, 1])
        st.checkbox("ISP (Inversión)", key="isp", on_change=recalcular)
        st.selectbox("RET %", [0, 7, 15, 19], key="ret_p", on_change=recalcular)
        o3.text_input("Nº FACTURA", value="2026-X01")

        st.divider()
        # IVA EN EL MEDIO (Eje del asesor)
        i1, i2, i3 = st.columns([1.2, 0.8, 1.2])
        i1.number_input("BASE IMPONIBLE", key="base", on_change=recalcular, format="%.2f")
        i2.selectbox("IVA %", [21, 10, 4, 0], key="iva_p", on_change=recalcular, index=0)
        i3.number_input("TOTAL (€)", key="total", on_change=recalcular, format="%.2f")
        
        st.button("🚀 REGISTRAR (ENTER)", use_container_width=True, type="primary")

# --- PANEL INFERIOR: REGISTRO MAESTRO ---
st.write("###")
st.subheader("📋 Libro de Registro y Auditoría")

# Estructura de 10 columnas clavadas
h = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
headers = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]
for col, text in zip(h, headers): col.markdown(f"**{text}**")

def dibujar_fila(aud, flag, fecha, sujeto, base, iva, ret, total, modelos):
    r = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    r[0].write("✅" if aud=="ok" else "⚠️")
    r[1].markdown(f"### {flag}") # Banderas 🇪🇸 / 🇪🇺
    r[2].write(fecha)
    r[3].markdown(f"**{sujeto}**")
    r[4].write(f"{base:,.2f}€")
    r[5].write(f"{iva:,.2f}€")
    r[6].write(f"{ret:,.2f}€" if ret > 0 else "-")
    r[7].write(f"**{total:,.2f}€**")
    
    m_html = "".join([f'<span class="mod-badge {"mod-349" if m=="349" else "mod-111" if m=="111" else ""}">{m}</span>' for m in modelos])
    r[8].markdown(m_html, unsafe_allow_html=True)
    r[9].button("👁️", key=sujeto)

dibujar_fila("ok", "🇪🇺", "19/02", "ADOBE SYSTEMS", st.session_state.base, st.session_state.cuota_iva, st.session_state.cuota_ret, st.session_state.total, ["303", "349"])
dibujar_fila("ok", "🇪🇸", "18/02", "BAR EL GRIEGO", 66.34, 6.63, 0, 72.97, ["303"])

# --- LÍNEA DE TOTALES ALINEADA ---
st.markdown('<div class="total-row">', unsafe_allow_html=True)
t = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
t[3].write("TOTALES CUADRE:")
t[4].write(f"{st.session_state.base + 66.34:,.2f}€")
t[5].write(f"{st.session_state.cuota_iva + 6.63:,.2f}€")
t[6].write(f"{st.session_state.cuota_ret:,.2f}€")
t[7].write(f"{st.session_state.total + 72.97:,.2f}€")
st.markdown('</div>', unsafe_allow_html=True)
