import streamlit as st
import pandas as pd

# 1. INICIALIZACIÓN DE CEREBRO (Evita NameErrors y KeyErrors)
if 'base' not in st.session_state: st.session_state.base = 100.00
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

def recalcular():
    """Calcula cuotas y totales al instante sin errores de formulario."""
def update_finance():
    st.session_state.cuota_iva = round(st.session_state.base * (st.session_state.iva_p / 100), 2)
    st.session_state.cuota_ret = round(st.session_state.base * (st.session_state.ret_p / 100), 2)
    
    # Lógica ISP: El IVA no suma al total a pagar al acreedor
    # Si es ISP, el IVA se autorrepercuted (no suma al total a pagar)
    if st.session_state.isp:
        st.session_state.total = round(st.session_state.base - st.session_state.cuota_ret, 2)
    else:
        st.session_state.total = round(st.session_state.base + st.session_state.cuota_iva - st.session_state.cuota_ret, 2)

# Ejecución inicial para asegurar que las variables existan
if 'cuota_iva' not in st.session_state: recalcular()
if 'total' not in st.session_state: update_finance()

# 2. CONFIGURACIÓN DE PANTALLA
st.set_page_config(layout="wide", page_title="Búnker Pro | Auditoría Total")
# 3. NAVEGACIÓN CENTRALIZADA
nav = st.sidebar.radio("📁 GESTIÓN DE FACTURACIÓN", ["📥 Recibidas", "📤 Emitidas", "📊 Control de Impuestos"])

st.markdown("""
    <style>
    .asiento-header { background: #1e293b; color: white; padding: 10px; border-radius: 5px 5px 0 0; font-weight: bold; }
    .asiento-body { background: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; font-family: 'Roboto Mono', monospace; border-radius: 0 0 5px 5px; }
    .total-row { background: #f1f5f9; font-weight: bold; border-top: 2px solid #3b82f6; padding: 15px 0; margin-top: 10px; }
    .badge-mod { background: #01579b; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; margin-right: 4px; }
    .badge-349 { background: #166534; }
    .badge-111 { background: #9a3412; }
    </style>
    """, unsafe_allow_html=True)
# --- PANTALLA: RECIBIDAS / EMITIDAS (Diferenciadas por lógica) ---
if nav in ["📥 Recibidas", "📤 Emitidas"]:
    with st.container(border=True):
        col_doc, col_asiento, col_ficha = st.columns([1, 1, 1.2])
        
        with col_doc:
            st.markdown("### 📄 Documento (IA)")
            st.markdown('<div style="background:#334155; height:380px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white;">VISOR PDF (Metadata Activo)</div>', unsafe_allow_html=True)

# 3. NAVEGACIÓN (Definida al inicio para evitar errores)
tab_rec, tab_emi, tab_reg = st.tabs(["📥 RECIBIDAS", "📤 EMITIDAS", "📋 LIBRO DE REGISTRO"])
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

with tab_rec:
    col_doc, col_asiento, col_ficha = st.columns([1, 0.9, 1.2])
    
    with col_doc:
        st.markdown("### 📄 Documento")
        st.markdown('<div style="background:#334155; height:350px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white;">Visor PDF Activo</div>', unsafe_allow_html=True)

    with col_asiento:
        st.markdown("### ⚙️ Asiento Contable")
        # Visualización limpia del asiento (Debe/Haber)
        st.markdown('<div class="asiento-header">PREVISUALIZACIÓN ASIENTO</div>', unsafe_allow_html=True)
        asiento_html = f"""
        <div class="asiento-body">
        (629) Gasto Corriente ............ {st.session_state.base:,.2f} (D)<br>
        (472) IVA Soportado ............... {st.session_state.cuota_iva:,.2f} (D)<br>
        """
        if st.session_state.isp:
            asiento_html += f"(477) IVA Repercutido (ISP) ..... {st.session_state.cuota_iva:,.2f} (H)<br>"
        if st.session_state.ret_p > 0:
            asiento_html += f"(475.1) Retención IRPF .......... {st.session_state.cuota_ret:,.2f} (H)<br>"
        
        asiento_html += f"<b>(410) Acreedor/Proveedor ...... {st.session_state.total:,.2f} (H)</b></div>"
        st.markdown(asiento_html, unsafe_allow_html=True)
        if st.session_state.isp: st.warning("💡 ISP: Inversión del Sujeto Pasivo detectada.")

    with col_ficha:
        st.markdown("### ⚡ Validación Rápida")
        # Identificación
        c1, c2, c3 = st.columns([2, 1, 0.5])
        c1.text_input("PROVEEDOR", value="ADOBE SYSTEMS IE")
        c2.text_input("NIF / VAT", value="IE6362892H")
        c3.markdown("## 🇪🇺") # Bandera visual

        # Configuración de Modelos
        o1, o2, o3 = st.columns([1.2, 0.8, 1])
        st.session_state.isp = o1.checkbox("ISP (Inversión)", value=st.session_state.isp, on_change=recalcular)
        st.session_state.ret_p = o2.selectbox("RET %", [0, 7, 15, 19], index=[0, 7, 15, 19].index(st.session_state.ret_p), on_change=recalcular)
        o3.text_input("Nº FACTURA", value="2026-X01")

        st.divider()
        # Importes (Reactividad Pura sin Formulario para evitar errores)
        i1, i2, i3 = st.columns([1.2, 0.8, 1.2])
        st.session_state.base = i1.number_input("BASE IMPONIBLE", value=st.session_state.base, on_change=recalcular, format="%.2f")
        st.session_state.iva_p = i2.selectbox("IVA %", [21, 10, 4, 0], index=[21, 10, 4, 0].index(st.session_state.iva_p), on_change=recalcular)
        st.session_state.total = i3.number_input("TOTAL (€)", value=st.session_state.total, on_change=recalcular, format="%.2f")
        
        # Botón de acción principal
        st.button("🚀 REGISTRAR ASIENTO (ENTER)", use_container_width=True, type="primary")
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

# --- BLOQUE DE REGISTRO (CON BANDERAS Y TOTALES ALINEADOS) ---
with tab_reg:
    st.subheader("📋 Libro de Registro y Auditoría")
    # 10 Columnas perfectamente alineadas
    cols = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    headers = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]
    for col, h in zip(cols, headers): col.markdown(f"**{h}**")
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
@@ -104,17 +100,35 @@ def recalcular():
    row[5].write(f"{st.session_state.cuota_iva:,.2f}€")
    row[6].write(f"{st.session_state.cuota_ret:,.2f}€" if st.session_state.ret_p > 0 else "-")
    row[7].write(f"**{st.session_state.total:,.2f}€**")
    
    # Badges de modelos
    row[8].markdown('<span class="badge-mod">303</span><span class="badge-mod badge-349">349</span>', unsafe_allow_html=True)
    row[9].button("👁️", key="vis_1")
    row[8].markdown('<span class="mod-badge" style="background:#01579b">303</span><span class="mod-badge" style="background:#166534">349</span>', unsafe_allow_html=True)
    row[9].button("👁️", key="vis_rec")

    # TOTALES DE CONTROL (Verticalmente debajo de sus columnas)
    # TOTALES ALINEADOS
    st.markdown('<div class="total-row">', unsafe_allow_html=True)
    t = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    t[3].write("TOTALES CUADRE:")
    t[4].write(f"{st.session_state.base:,.2f}€")
    t[5].write(f"{st.session_state.cuota_iva:,.2f}€")
    t[6].write(f"{st.session_state.cuota_ret:,.2f}€")
    t[7].write(f"{st.session_state.total:,.2f}€")
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
