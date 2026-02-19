import streamlit as st

# 1. CONFIGURACIÓN DEL SaaS
st.set_page_config(layout="wide", page_title="Búnker Pro | High-Speed SaaS")

# Lógica de puntos para Cuentas (TSV Ready)
def format_cuenta(cta, software="A3"):
    cta_limpia = cta.replace(".", "")
    if software == "A3": # Ejemplo: 410.00012
        return f"{cta_limpia[:3]}.{cta_limpia[3:]}"
    return cta_limpia # Contasol suele preferir sin puntos o configurables

# 2. MOTOR REACTIVO
if 'total_f' not in st.session_state: st.session_state.total_f = 72.97
if 'iva_p' not in st.session_state: st.session_state.iva_p = 10

def recalcular():
    st.session_state.base_f = round(st.session_state.total_f / (1 + (st.session_state.iva_p / 100)), 2)
    st.session_state.cuota_f = round(st.session_state.total_f - st.session_state.base_f, 2)

if 'base_f' not in st.session_state: recalcular()

# --- INTERFAZ DUAL ---
col_pdf, col_ficha = st.columns([1.1, 1])

with col_pdf:
    st.markdown('<iframe src="https://www.africau.edu/images/default/sample.pdf" width="100%" height="800px" style="border-radius:10px; border: 1px solid #d1d5db;"></iframe>', unsafe_allow_html=True)

with col_ficha:
    with st.container(border=True):
        # BLOQUE 1: IDENTIFICACIÓN CON ICONO DINÁMICO
        # Cambiamos el icono según la categoría
        icono = "🍽️" if "Restaurante" in "Comidas" else "🏢"
        st.markdown(f"### {icono} Datos del Proveedor")
        
        r1_c1, r1_c2, r1_c3 = st.columns([2, 1, 1])
        prov = r1_c1.text_input("PROVEEDOR", value="RESTAURANTE EL GRIEGO")
        nif = r1_c2.text_input("NIF", value="B12345678")
        # Cuenta formateada para A3/Contasol
        cta_t = r1_c3.text_input("CTA. TRÁFICO", value=format_cuenta("41000012"))

        st.divider()

        # BLOQUE 2: OPERACIÓN (EL CENTRO)
        st.markdown("### ⚙️ Naturaleza del Gasto")
        r2_c1, r2_c2, r2_c3 = st.columns([1, 1, 1])
        tipo_op = r2_c1.selectbox("TIPO OPERACIÓN", ["IVA Soportado", "Bienes Inversión", "Exento"])
        cat_gasto = r2_c2.text_input("CAT. GASTO", value="Comidas")
        cta_g = r2_c3.text_input("CTA. GASTO", value=format_cuenta("62900000"))

        st.divider()

        # BLOQUE 3: IMPORTES (REACTIVIDAD PURA)
        st.markdown("### 💰 Importes")
        
        r3_c1, r3_c2, r3_c3 = st.columns([1.2, 0.8, 1])
        
        # IVA EN EL MEDIO (Eje del pensamiento)
        r3_c2.selectbox("IVA (%)", [21, 10, 4, 0], key="iva_p", on_change=recalcular, index=1)
        
        # Base y Cuota reactivas
        base_edit = r3_c1.number_input("BASE IMPONIBLE", key="base_f", format="%.2f")
        cuota_edit = r3_c3.number_input("CUOTA IVA (Editable)", key="cuota_f", format="%.2f", step=0.01)

        r4_c1, r4_c2 = st.columns([1, 1])
        r4_c1.text_input("Nº FACTURA / REF", value="FRA-2024-001")
        # El Total abajo como disparador
        total_input = r4_c2.number_input("💵 TOTAL FACTURA (€)", key="total_f", on_change=recalcular, format="%.2f")

    # BOTONERA DE ACCIÓN
    c_plus, c_save = st.columns([0.2, 4])
    c_plus.button("➕") # Para bases mixtas
    
    with c_save:
        with st.form("envio", clear_on_submit=True):
            # El botón que Pedro pulsa con el ENTER
            if st.form_submit_button("🚀 CONTABILIZAR ASIENTO (ENTER)", use_container_width=True, type="primary"):
                # Aquí se genera el TSV ligero
                st.toast("Asiento exportado al TSV. ¡Siguiente!")
