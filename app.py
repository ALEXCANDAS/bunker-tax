import streamlit as st

# 1. SETUP SaaS PRO
st.set_page_config(layout="wide", page_title="Búnker Pro | Auditoría 360")

# CSS para banderas y alertas de auditoría
st.markdown("""
    <style>
    .badge-iso { font-size: 1.2rem; margin-right: 10px; }
    .status-ok { color: #2ecc71; font-weight: bold; }
    .status-alert { color: #e74c3c; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .audit-row { border-bottom: 1px solid #eee; padding: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

tab_recibidas, tab_emitidas, tab_registro = st.tabs(["📥 RECIBIDAS", "📤 EMITIDAS", "📋 CONTROL DE MODELOS"])

with tab_registro:
    # FILTROS DE SEGMENTACIÓN PRO
    f1, f2, f3, f4, f5 = st.columns([1, 1, 1, 1, 2])
    f_tri = f1.selectbox("TRIMESTRE", ["Todos", "1T", "2T", "3T", "4T"])
    f_mod = f2.selectbox("MODELO", ["Todos", "303", "111", "347", "349"])
    f_pais = f3.selectbox("ORIGEN", ["Todos", "ES 🇪🇸", "UE 🇪🇺", "EXT 🌎"])
    f_tipo = f4.selectbox("FLUJO", ["Todos", "Recibidas", "Emitidas"])
    f_busq = f5.text_input("🔍 FILTRO NIF / PROVEEDOR / CUENTA", placeholder="Ej: B12345678...")

    st.divider()

    # CABECERA TÉCNICA (A3/Exact Style)
    # Aud. | Origen | Fecha | Sujeto / NIF | Base | IVA | Ret. | Total | Banderas Modelos | Visor
    h = st.columns([0.4, 0.6, 0.8, 1.8, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
    header_labels = ["AUD", "ORG", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET.", "TOTAL", "MODELOS", "VIS"]
    for col, label in zip(h, header_labels):
        col.markdown(f"**{label}**")

    # FUNCIÓN DE FILA DE AUDITORÍA
    def audit_row(audit_st, flag, fecha, nombre, nif, base, iva, ret, total, modelos, error_msg=""):
        r = st.columns([0.4, 0.6, 0.8, 1.8, 0.8, 0.8, 0.8, 0.8, 1.5, 0.4])
        
        # Auditoría IA vs Humano
        st_icon = "⚠️" if audit_st == "alert" else "✅"
        r[0].markdown(f'<span class="status-{"alert" if audit_st=="alert" else "ok"}">{st_icon}</span>', unsafe_allow_html=True)
        
        r[1].markdown(f'<span class="badge-iso">{flag}</span>', unsafe_allow_html=True)
        r[2].write(fecha)
        r[3].markdown(f"**{nombre}** <br><small>{nif}</small>", unsafe_allow_html=True)
        r[4].write(f"{base}€")
        r[5].write(f"{iva}€")
        r[6].write(f"{ret}€" if ret != "-" else "-")
        r[7].write(f"**{total}€**")
        
        # Banderas de Modelos (Colores dinámicos)
        b_html = ""
        for m in modelos:
            c = "#01579b" if m=="303" else "#e65100" if m=="111" else "#4a148c" if m=="347" else "#27ae60"
            b_html += f'<span style="background:{c}; color:white; padding:2px 5px; border-radius:3px; margin-right:3px; font-size:10px;">M-{m}</span>'
        r[8].markdown(b_html, unsafe_allow_html=True)
        
        with r[9].expander("👁️"):
            st.image("https://via.placeholder.com/400x500?text=FACTURA+AUDITADA", use_container_width=True)
            if error_msg: st.error(f"IA Detecta: {error_msg}")

    # DATOS DE EJEMPLO CON AUDITORÍA REAL
    # 1. Caso Normal
    audit_row("ok", "🇪🇸", "19/02", "BAR EL GRIEGO", "B12345678", "66.34", "6.63", "-", "72.97", ["303"])
    
    # 2. Caso Profesional con Retención (M-111)
    audit_row("ok", "🇪🇸", "18/02", "NACHO SEVILLA ASOC.", "B99887766", "200.00", "42.00", "30.00", "212.00", ["303", "111"])
    
    # 3. ALERTA DE MARINA: Operación Intracomunitaria mal clasificada
    audit_row("alert", "🇪🇺", "17/02", "ADOBE SYSTEMS IE", "IE6362892H", "120.00", "0.00", "-", "120.00", ["303"], 
              error_msg="NIF Irlandés detectado. Debería ser M-349 y Autorepercusión IVA.")
    
    # 4. Caso 347 (Grandes volúmenes)
    audit_row("ok", "🇪🇸", "15/02", "CONSTRUCTORA X", "B55544433", "4000.00", "840.00", "-", "4840.00", ["303", "347"])

    st.divider()

    # RESUMEN CUADRE 390 / ANUAL
    c_b, c_i, c_r, c_t = st.columns(4)
    c_b.metric("Total Base", "4.386,34 €", help="Cifra para el 390")
    c_i.metric("Total IVA", "888,63 €")
    c_r.metric("Total Retenciones", "30,00 €", help="Cifra para el 190")
    c_t.metric("Acumulado Diario", "5.244,97 €")
