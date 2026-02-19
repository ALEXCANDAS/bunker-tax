import streamlit as st

# 1. SETUP ULTRA-WIDE (Sin márgenes)
st.set_page_config(layout="wide", page_title="Búnker Pro | Producción")

# Inicialización de estados para reactividad total
if 'total_f' not in st.session_state: st.session_state.total_f = 72.97
if 'iva_p' not in st.session_state: st.session_state.iva_p = 10

def recalcular():
    # Esta es la lógica que "mueve" la base sola
    st.session_state.base_f = round(st.session_state.total_f / (1 + (st.session_state.iva_p / 100)), 2)
    st.session_state.cuota_f = round(st.session_state.total_f - st.session_state.base_f, 2)

if 'base_f' not in st.session_state: recalcular()

# --- INTERFAZ DUAL ---
col_pdf, col_ficha = st.columns([1.1, 1])

with col_pdf:
    st.markdown('<iframe src="https://www.africau.edu/images/default/sample.pdf" width="100%" height="800px" style="border-radius:10px; border: 1px solid #d1d5db;"></iframe>', unsafe_allow_html=True)

with col_ficha:
    with st.container(border=True):
        # BLOQUE 1: IDENTIFICACIÓN (Arriba, fijo)
        st.markdown("### 🏢 Identificación")
        r1_c1, r1_c2, r1_c3 = st.columns([2, 1, 1])
        r1_c1.text_input("PROVEEDOR", value="RESTAURANTE EL GRIEGO")
        r1_c2.text_input("NIF", value="B12345678")
        r1_c3.text_input("CTA. TRÁFICO", value="410.00012")

        st.divider()

        # BLOQUE 2: OPERACIÓN (EL CENTRO)
        st.markdown("### ⚙️ Configuración del Asiento")
        r2_c1, r2_c2, r2_c3 = st.columns([1, 1, 1])
        # Separamos Tipo de Operación de Categoría
        r2_c1.selectbox("TIPO OPERACIÓN", ["IVA Soportado (Gasto)", "Bienes Inversión", "Intracomunitaria"])
        r2_c2.text_input("CAT. GASTO", value="Comidas")
        r2_c3.text_input("CTA. GASTO", value="629.00000")

        st.divider()

        # BLOQUE 3: IMPORTES (EL MOTOR REACTIVO)
        st.markdown("### 💰 Liquidación")
        
        # Fila económica: Base -> IVA (Medio) -> Cuota
        r3_c1, r3_c2, r3_c3 = st.columns([1.2, 0.8, 1])
        
        # El IVA en el centro, como pediste
        r3_c2.selectbox("IVA (%)", [21, 10, 4, 0], key="iva_p", on_change=recalcular, index=1)
        
        # La Base y Cuota ahora sí se mueven solas
        base_edit = r3_c1.number_input("BASE IMPONIBLE", key="base_f", format="%.2f")
        cuota_edit = r3_c3.number_input("CUOTA IVA (Editable)", key="cuota_f", format="%.2f", step=0.01)

        # Referencia y Total final (El disparador)
        r4_c1, r4_c2 = st.columns([1, 1])
        r4_c1.text_input("Nº FACTURA / REF", value="FRA-2024-001")
        # Al cambiar el total, todo lo de arriba baila
        total_input = r4_c2.number_input("💵 TOTAL FACTURA (€)", key="total_f", on_change=recalcular, format="%.2f")

    # BOTONERA
    c_plus, c_save = st.columns([0.2, 4])
    c_plus.button("➕") # Solo para casos raros, no mueve nada
    
    with c_save:
        with st.form("envio", clear_on_submit=True):
            if st.form_submit_button("🚀 CONTABILIZAR Y SIGUIENTE (ENTER)", use_container_width=True, type="primary"):
                st.toast("Guardado con éxito.")
