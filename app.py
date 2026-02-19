import streamlit as st

# 1. SETUP PROFESIONAL
st.set_page_config(layout="wide", page_title="Búnker Pro | Inteligencia de Gasto")

# 2. DICCIONARIO DE ACTIVIDADES (Lo que la IA alimenta y aprende)
# Aquí configuramos qué cuenta y qué IVA suele usar cada tipo de negocio
PATRONES_ACTIVIDAD = {
    "RESTAURACION": {"iva": 10, "cta_gasto": "629.0", "deducible": True},
    "TASAS_REGISTRO": {"iva": 0, "cta_gasto": "629.1", "deducible": False},
    "COMBUSTIBLE": {"iva": 21, "cta_gasto": "628.0", "deducible": True},
    "DEFAULT": {"iva": 21, "cta_gasto": "600.0", "deducible": True}
}

# 3. LÓGICA DE DETECCIÓN SEMÁNTICA
def clasificar_proveedor(nombre):
    n = nombre.upper()
    if "RESTAURANTE" in n or "GRIEGO" in n: return "RESTAURACION"
    if "REGISTRO" in n or "NOTARIA" in n: return "TASAS_REGISTRO"
    if "REPSOL" in n or "CEPSA" in n: return "COMBUSTIBLE"
    return "DEFAULT"

# --- INTERFAZ DE VALIDACIÓN ---
st.title("🛡️ Validación de Gasto e IVA")

# Simulamos lectura de Gemini
prov_detectado = "RESTAURANTE EL GRIEGO"
actividad = clasificar_proveedor(prov_detectado)
patron = PATRONES_ACTIVIDAD[actividad]

with st.form("ficha_inteligente"):
    # CABECERA: TOTAL Y PATRÓN
    c_nom, c_tot, c_iva = st.columns([2, 1, 1])
    with c_nom:
        st.text_input("PROVEEDOR", value=prov_detectado)
        st.caption(f"📂 Actividad detectada: **{actividad}** (Cuenta {patron['cta_gasto']})")
    
    with c_tot:
        total = st.number_input("TOTAL FACTURA (€)", value=72.97, format="%.2f")
    
    with c_iva:
        # IVA configurable que viene pre-seteado por el patrón
        iva_val = st.selectbox("IVA (%)", [21, 10, 4, 0], 
                             index=[21, 10, 4, 0].index(patron['iva']))

    st.divider()

    # CUERPO: SEGMENTACIÓN DE LA BASE
    col_base, col_cuota, col_tipo = st.columns([2, 1, 1])
    
    # Calculamos la base deducible
    base_propuesta = total / (1 + (iva_val / 100))
    
    with col_base:
        base_final = st.number_input("BASE IMPONIBLE (Deducible)", value=base_propuesta)
    
    with col_cuota:
        cuota = base_final * (iva_val / 100)
        st.metric("CUOTA IVA", f"{cuota:.2f} €")
        
    with col_tipo:
        st.selectbox("TIPO GASTO", ["Deducible", "No Deducible", "Exento"], 
                    index=0 if patron['deducible'] else 1)

    # SECCIÓN DE SUPLIDOS (Lo que sobra para cuadrar)
    st.write("###")
    sobrante = total - (base_final + cuota)
    
    c_sup, c_info = st.columns([3, 1])
    with c_sup:
        suplidos = st.number_input("SUPLIDOS / GASTOS NO DEDUCIBLES", value=sobrante if abs(sobrante) > 0.01 else 0.0)
    
    with c_info:
        if abs(total - (base_final + cuota + suplidos)) < 0.01:
            st.success("✅ CUADRADO")
        else:
            st.error("❌ DIFERENCIA")

    st.form_submit_button("🚀 CONTABILIZAR ASIENTO (ENTER)", use_container_width=True, type="primary")
