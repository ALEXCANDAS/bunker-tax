import streamlit as st
from datetime import date

# 1. SETUP SaaS
st.set_page_config(layout="wide", page_title="Búnker Pro | Sistema Integrado")

# Estado de la cola de facturas
if 'total_f' not in st.session_state: st.session_state.total_f = 72.97
if 'iva_p' not in st.session_state: st.session_state.iva_p = 10

def recalcular():
    st.session_state.base_f = round(st.session_state.total_f / (1 + (st.session_state.iva_p / 100)), 2)
    st.session_state.cuota_f = round(st.session_state.total_f - st.session_state.base_f, 2)

if 'base_f' not in st.session_state: recalcular()

# --- INTERFAZ DUAL ---
col_pdf, col_ficha = st.columns([1.1, 1])

with col_pdf:
    st.markdown("### 📄 Visor de Entrada Directa")
    st.markdown('<iframe src="https://www.africau.edu/images/default/sample.pdf" width="100%" height="750px" style="border-radius:10px; border: 1px solid #d1d5db;"></iframe>', unsafe_allow_html=True)

with col_ficha:
    # FORMULARIO MAESTRO (Para que el Enter funcione de verdad)
    with st.form("contabilizacion_flash", clear_on_submit=True):
        st.markdown("### 📝 Ficha de Validación Manual")
        
        with st.container(border=True):
            # FILA 0: FECHA Y REFERENCIA (Lo que faltaba)
            c_f1, c_f2, c_f3 = st.columns([1, 1, 1])
            fecha_fra = c_f1.date_input("FECHA FACTURA", value=date.today())
            ref_fra = c_f2.text_input("Nº FACTURA", value="FRA-2024-001")
            tipo_op = c_f3.selectbox("OPERACIÓN", ["Soportado Corriente", "Profesional (-15%)", "Bienes Inv."])

            # FILA 1: IDENTIFICACIÓN
            id_c1, id_c2, id_c3 = st.columns([2, 1, 1])
            prov = id_c1.text_input("PROVEEDOR", value="RESTAURANTE EL GRIEGO")
            nif = id_c2.text_input("NIF", value="B12345678")
            cta_t = id_c3.text_input("CTA. TRÁFICO", value="410.00012")

            st.divider()

            # FILA 2: GASTO
            g_c1, g_c2 = st.columns([2, 1])
            cat_gasto = g_c1.text_input("CATEGORÍA / CONCEPTO", value="Comidas y Representación")
            cta_g = g_c2.text_input("CTA. GASTO", value="629.00000")

            st.divider()

            # FILA 3: IMPORTES (REACTIVOS)
            st.markdown("#### 💰 Desglose Económico")
            r3_c1, r3_c2, r3_c3 = st.columns([1.2, 0.8, 1])
            
            # Al ser un FORM, usamos keys para que el on_change se procese al final o con el botón
            iva_p = r3_c2.selectbox("IVA (%)", [21, 10, 4, 0], index=1, key="iva_p_form")
            base_f = r3_c1.number_input("BASE IMPONIBLE", value=st.session_state.base_f, format="%.2f")
            cuota_f = r3_c3.number_input("CUOTA IVA (Editable)", value=st.session_state.cuota_f, format="%.2f")

            # TOTAL FINAL
            st.write("###")
            total_input = st.number_input("💵 TOTAL FACTURA (€)", value=st.session_state.total_f, format="%.2f")

        # BOTÓN "+" DINÁMICO (Simulado)
        if st.form_submit_button("➕ AÑADIR LÍNEA (IVA MIXTO / RETENCIÓN)"):
            st.info("Se habilitará una segunda fila de bases en la siguiente versión.")

        # EL BOTÓN QUE DISPARA EL ENTER
        if st.form_submit_button("🚀 CONTABILIZAR Y PASAR AL SIGUIENTE (ENTER)", use_container_width=True, type="primary"):
            # AQUÍ ES DONDE SE GUARDA EN EL TSV
            st.success(f"Factura {ref_fra} contabilizada correctamente.")
            # Lógica para cargar la siguiente factura de la carpeta...

# --- SECCIÓN DE REGISTRO DE FACTURAS (EL LISTADO GENERAL) ---
st.divider()
st.subheader("📋 Registro General de Facturas (Entrada Automática)")
st.caption("Aquí aparecen las facturas que la IA ya ha procesado desde Drive/TSV sin intervención manual.")

# Simulación de la pantalla de registro
data = {
    "Fecha": ["01/02/2024", "02/02/2024", "03/02/2024"],
    "Proveedor": ["Telefónica", "Amazon Business", "Gasolinera Cepsa"],
    "Total": [54.20, 125.00, 60.00],
    "Estado": ["✅ Auto", "✅ Auto", "⚠️ Pendiente Revisión"]
}
st.table(data)
