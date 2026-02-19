import streamlit as st

# 1. CONFIGURACIÓN DE PANTALLA (Para tu LG con f.lux)
st.set_page_config(layout="wide", page_title="Búnker Pro | TSV Engine")

# 2. ESTADO DE SESIÓN (Memoria reactiva)
if 'lineas' not in st.session_state:
    st.session_state.lineas = [{'base': 0.0, 'tipo': 21, 'cta': '600.00000'}]
if 'total_fra' not in st.session_state: st.session_state.total_fra = 0.0

def add_linea():
    # Lógica de autodescuadre: calcula lo que falta para el próximo "+"
    total_actual = sum([l['base'] * (1 + l['tipo']/100) for l in st.session_state.lineas])
    falta = st.session_state.total_fra - total_actual
    nueva_base = falta / 1.21 if falta > 0 else 0.0
    st.session_state.lineas.append({'base': round(nueva_base, 2), 'tipo': 21, 'cta': '600.00000'})

# --- INTERFAZ DUAL (PDF Izquierda | Ficha Derecha) ---
col_pdf, col_ficha = st.columns([1.1, 1])

with col_pdf:
    st.subheader("📁 Visor Drive (f.lux Ready)")
    st.markdown('<div style="height:80vh; background:#2d2f31; border-radius:10px; display:flex; align-items:center; justify-content:center;">'
                '<p style="color:#64748b;">[ Visualizador de PDF conectado a Drive ]</p></div>', unsafe_allow_html=True)

with col_ficha:
    st.subheader("📝 Generador de Asiento TSV")
    
    with st.container(border=True):
        # CABECERA: Tráfico y Total
        c1, c2, c3 = st.columns([1.5, 1, 1])
        with c1: st.text_input("PROVEEDOR", value="RESTAURANTE EL GRIEGO", key="prov")
        with c2: st.text_input("CTA. TRÁFICO", value="410.00012", key="cta_traf")
        with c3: st.number_input("TOTAL FACTURA", key="total_fra", format="%.2f", step=0.01)

        st.divider()

        # CUERPO: Líneas Dinámicas (Multi-IVA / Suplidos)
        for i, linea in enumerate(st.session_state.lineas):
            r1, r2, r3, r4 = st.columns([1.5, 2, 1, 0.5])
            
            with r1: # Cuenta de gasto para esta línea
                st.session_state.lineas[i]['cta'] = st.text_input(f"Cta. Gasto", value=linea['cta'], key=f"cta_{i}", label_visibility="collapsed")
            
            with r2: # Base imponible
                st.session_state.lineas[i]['base'] = st.number_input(f"Base", value=linea['base'], key=f"b_{i}", label_visibility="collapsed")
            
            with r3: # Tipo de IVA
                st.session_state.lineas[i]['tipo'] = st.selectbox(f"IVA", [21, 10, 4, 0], 
                                                                 index=[21,10,4,0].index(linea['tipo']), 
                                                                 key=f"t_{i}", label_visibility="collapsed")
            
            with r4: # Eliminar línea
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.lineas.pop(i)
                    st.rerun()

        # BOTÓN "+" (El corazón de la flexibilidad)
        st.button("➕ Añadir línea (IVA / Suplido / Exento)", on_click=add_linea)

        st.divider()

        # VALIDACIÓN DE CUADRE
        sum_total = sum([round(l['base'] * (1 + l['tipo']/100), 2) for l in st.session_state.lineas])
        dif = round(st.session_state.total_fra - sum_total, 2)
        
        if abs(dif) < 0.01:
            st.success("✅ ASIENTO CUADRADO")
        else:
            st.warning(f"⚠️ DESCUADRE: {dif} € (Pulsa + para cuadrar)")

        # BOTÓN CONTABILIZAR (Captura el ENTER)
        with st.form("save_tsv", clear_on_submit=True):
            if st.form_submit_button("🚀 GUARDAR EN TSV Y SIGUIENTE (ENTER)", use_container_width=True, type="primary"):
                # Aquí se generaría la línea de texto: "410.00012 [TAB] 600.00000 [TAB] 72.97..."
                st.toast("Línea exportada a la cola TSV")
