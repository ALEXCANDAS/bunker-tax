import streamlit as st

# 1. MOTOR DE CÁLCULO CONTABLE (Sin errores, reactivo al 100%)
# Inicializamos todas las variables para evitar NameErrors
if 'base' not in st.session_state: st.session_state.base = 100.00
if 'iva_p' not in st.session_state: st.session_state.iva_p = 21
if 'ret_p' not in st.session_state: st.session_state.ret_p = 0
if 'isp' not in st.session_state: st.session_state.isp = False
if 'cuota_iva' not in st.session_state: st.session_state.cuota_iva = 21.00
if 'cuota_ret' not in st.session_state: st.session_state.cuota_ret = 0.00
if 'total' not in st.session_state: st.session_state.total = 121.00

def recalcular():
    """Calcula el asiento al instante al usar el Tabulador."""
    # Cálculo de cuotas
    st.session_state.cuota_iva = round(st.session_state.base * (st.session_state.iva_p / 100), 2)
    st.session_state.cuota_ret = round(st.session_state.base * (st.session_state.ret_p / 100), 2)
    
    # Lógica de ISP (Inversión del Sujeto Pasivo):
    # El IVA se autorrepercuted y NO se paga al proveedor.
    if st.session_state.isp:
        st.session_state.total = round(st.session_state.base - st.session_state.cuota_ret, 2)
    else:
        # Lógica normal: Base + IVA - Retención
        st.session_state.total = round(st.session_state.base + st.session_state.cuota_iva - st.session_state.cuota_ret, 2)

# 2. CONFIGURACIÓN VISUAL (LG UltraWide)
st.set_page_config(layout="wide", page_title="Búnker Pro | Producción")

st.markdown("""
    <style>
    /* Estilos de Asiento Contable */
    .asiento-header { background: #1e293b; color: white; padding: 10px; border-radius: 5px 5px 0 0; font-weight: bold; }
    .asiento-body { background: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; font-family: 'Roboto Mono', monospace; border-radius: 0 0 5px 5px; }
    .debe { color: #2563eb; font-weight: bold; }
    .haber { color: #dc2626; font-weight: bold; }
    
    /* Estilos de Libro de Registro */
    .total-row { background: #f1f5f9; font-weight: bold; border-top: 2px solid #3b82f6; padding: 15px 0; margin-top: 10px; }
    .flag-icon { font-size: 1.6rem; margin-right: 5px; }
    
    /* Badges de Modelos */
    .badge-mod { background: #01579b; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; margin-right: 4px; }
    .badge-349 { background: #166534; }
    .badge-111 { background: #9a3412; }
    </style>
    """, unsafe_allow_html=True)

# 3. INTERFAZ DE TRABAJO
# Usamos pestañas para organizar, definidas antes de usar.
tab_rec, tab_emi, tab_imp = st.tabs(["📥 RECIBIDAS", "📤 EMITIDAS", "📊 CONTROL IMPUESTOS"])

with tab_rec:
    # Layout de 3 columnas: Visor | Asiento | Ficha
    col_doc, col_asiento, col_ficha = st.columns([1, 1, 1.2])
    
    with col_doc:
        st.markdown("### 📄 Visor Documental")
        st.markdown('<div style="background:#334155; height:380px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;">VISOR PDF ACTIVO</div>', unsafe_allow_html=True)

    with col_asiento:
        st.markdown("### ⚙️ Previsualización Asiento (D/H)")
        # Tabla de Asiento Profesional
        st.markdown('<div class="asiento-header">DIARIO PREVIO</div>', unsafe_allow_html=True)
        
        # Construcción dinámica del asiento HTML
        asiento_html = f"""
        <div class="asiento-body">
        <table style="width:100%;">
            <tr><td>(629) Gasto Corriente</td><td class="debe">{st.session_state.base:,.2f}</td><td></td></tr>
            <tr><td>(472) IVA Soportado</td><td class="debe">{st.session_state.cuota_iva:,.2f}</td><td></td></tr>
        """
        if st.session_state.isp:
            asiento_html += f"<tr><td>(477) IVA Rep. (ISP)</td><td></td><td class='haber'>{st.session_state.cuota_iva:,.2f}</td></tr>"
        if st.session_state.ret_p > 0:
            asiento_html += f"<tr><td>(475.1) Ret. IRPF</td><td></td><td class='haber'>{st.session_state.cuota_ret:,.2f}</td></tr>"
        
        asiento_html += f"""
            <tr style="font-weight:bold; border-top:1px solid #e2e8f0;"><td>(410) Acreedor/Prov.</td><td></td><td class="haber">{st.session_state.total:,.2f}</td></tr>
        </table>
        </div>
        """
        st.markdown(asiento_html, unsafe_allow_html=True)
        if st.session_state.isp: st.warning("💡 ISP: Inversión del Sujeto Pasivo detectada.")

    with col_ficha:
        st.markdown("### ⚡ Validación Rápida")
        # Fila 1: Identificación y Bandera Real
        c1, c2, c3 = st.columns([2, 1, 0.5])
        c1.text_input("PROVEEDOR", value="ADOBE SYSTEMS IE")
        c2.text_input("NIF / VAT", value="IE6362892H")
        c3.markdown('<span class="flag-icon">🇪🇺</span>', unsafe_allow_html=True)

        # Fila 2: Configuración Fiscal (ISP y Retención)
        o1, o2, o3 = st.columns([1, 1, 1.2])
        st.session_state.isp = o1.checkbox("ISP (Inversión)", value=st.session_state.isp, on_change=recalcular)
        st.session_state.ret_p = o2.selectbox("RET %", [0, 7, 15, 19], index=[0, 7, 15, 19].index(st.session_state.ret_p), on_change=recalcular)
        o3.text_input("Nº FACTURA", value="2026-X01")

        st.divider()
        
        # Fila 3: Núcleo Económico (IVA al Centro, Reactivo al Tab)
        i1, i2, i3 = st.columns([1.2, 0.8, 1.2])
        st.session_state.base = i1.number_input("BASE IMPONIBLE", value=st.session_state.base, on_change=recalcular, format="%.2f")
        st.session_state.iva_p = i2.selectbox("IVA %", [21, 10, 4, 0], index=[21, 10, 4, 0].index(st.session_state.iva_p), on_change=recalcular)
        st.session_state.total = i3.number_input("TOTAL (€)", value=st.session_state.total, on_change=recalcular, format="%.2f")
        
        # Botón de Acción Principal
        if st.button("🚀 REGISTRAR ASIENTO (ENTER)", use_container_width=True, type="primary"):
            st.toast("Asiento contabilizado y pasado al libro.")

# --- LIBRO DE REGISTRO Y AUDITORÍA ---
st.write("###")
st.subheader("📋 Libro de Registro y Auditoría")

# Cabecera de 10 columnas alineadas
cols = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
headers = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]
for col, h in zip(cols, headers): col.markdown(f"**{h}**")

# Fila de Ejemplo (Con Banderas e Iconos)
row = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
row[0].write("✅")
row[1].markdown('<span class="flag-icon">🇪🇺</span>', unsafe_allow_html=True)
row[2].write("19/02")
row[3].markdown(f"**ADOBE SYSTEMS** <br><small>IE6362892H</small>", unsafe_allow_html=True)
row[4].write(f"{st.session_state.base:,.2f}€")
row[5].write(f"{st.session_state.cuota_iva:,.2f}€")
row[6].write(f"{st.session_state.cuota_ret:,.2f}€" if st.session_state.ret_p > 0 else "-")
row[7].write(f"**{st.session_state.total:,.2f}€**")

# Badges de modelos con color
row[8].markdown('<span class="badge-mod">303</span><span class="badge-mod badge-349">349</span>', unsafe_allow_html=True)
row[9].button("👁️", key="vis_1")

# TOTALES DE CUADRE (Alineados verticalmente)
st.markdown('<div class="total-row">', unsafe_allow_html=True)
t = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
t[3].write("TOTALES CUADRE:")
t[4].write(f"{st.session_state.base:,.2f}€")
t[5].write(f"{st.session_state.cuota_iva:,.2f}€")
t[6].write(f"{st.session_state.cuota_ret:,.2f}€")
t[7].write(f"{st.session_state.total:,.2f}€")
st.markdown('</div>', unsafe_allow_html=True)
