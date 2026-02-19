import streamlit as st

# 1. SETUP DE ALTA VELOCIDAD
st.set_page_config(layout="wide", page_title="Búnker Pro | IA Semántica")

# 2. MOTOR DE INTELIGENCIA SEMÁNTICA (Simulando a Gemini)
def detectar_patron_por_nombre(nombre):
    nombre = nombre.upper()
    if "RESTAURANTE" in nombre or "MESON" in nombre or "GASTRO" in nombre:
        return 10
    if "HOTEL" in nombre or "HOSTAL" in nombre:
        return 10
    if "GASOLINA" in nombre or "REPSOL" in nombre:
        return 21
    return 21 # Por defecto España

# 3. ESTADO DE SESIÓN
if 'empresa_lectura' not in st.session_state:
    st.session_state.empresa_lectura = "RESTAURANTE EL GRIEGO S.L."

# --- INTERFAZ ---
st.title("🛡️ Validación Inteligente")

# Simulamos que la IA "lee" el nombre y ajusta el patrón
iva_sugerido = detectar_patron_por_nombre(st.session_state.empresa_lectura)

# FORMULARIO PARA CAPTURAR EL ENTER
with st.form("asiento_flash", clear_on_submit=True):
    
    # FILA DE CABECERA (El "Golpe de Ojo")
    c_nom, c_tot, c_iva = st.columns([2, 1, 1])
    
    with c_nom:
        nombre = st.text_input("📝 PROVEEDOR DETECTADO", value=st.session_state.empresa_lectura)
    
    with c_tot:
        # El foco del asesor empieza aquí
        total = st.number_input("TOTAL FACTURA (€)", value=121.00, format="%.2f")
    
    with c_iva:
        # El IVA se auto-selecciona por el nombre del proveedor
        iva_prio = st.selectbox("IVA PATRÓN (%)", [21, 10, 4, 0], 
                               index=[21, 10, 4, 0].index(iva_sugerido),
                               help="IA detectó Restaurante -> Sugiere 10%")

    st.divider()

    # BLOQUE DE TRABAJO (Autocalculado)
    bi1 = total / (1 + (iva_prio / 100))
    cuota1 = total - bi1

    col_bi, col_cuota, col_check = st.columns([2, 2, 1])
    
    with col_bi:
        base_final = st.number_input("BASE IMPONIBLE 1", value=bi1, format="%.2f")
    
    with col_cuota:
        st.metric("CUOTA IVA", f"{(base_final * (iva_prio/100)):.2f} €")

    # APARTADO EXENTO / OTROS (Para cuadrar al céntimo)
    st.write("###")
    sobrante = total - (base_final * (1 + iva_prio/100))
    
    col_ex, col_status = st.columns([3, 1])
    with col_ex:
        exento = st.number_input("SUPLIDOS / TASAS / EXENTO", value=sobrante if abs(sobrante) > 0.01 else 0.0)
    
    with col_status:
        # Verificación visual de cuadre
        if abs(total - (base_final + (base_final*(iva_prio/100)) + exento)) < 0.01:
            st.success("✅ CUADRADO")
        else:
            st.error("❌ DIFERENCIA")

    st.write("###")
    # BOTÓN QUE CAPTURA EL ENTER
    enviar = st.form_submit_button("🚀 CONTABILIZAR Y SIGUIENTE (PULSA ENTER)", 
                                 type="primary", 
                                 use_container_width=True)

    if enviar:
        st.toast("Asiento enviado al .dat con éxito")
        # Aquí saltaríamos a la siguiente factura
