import streamlit as st

st.set_page_config(page_title="BUNKER TAX", page_icon="🛡️")
st.title("🛡️ BÚNKER TAX - Control de Facturas")

st.info("Sube la factura y el sistema detectará la operación automáticamente.")

# El buzón de archivos
archivo = st.file_uploader("Arrastra aquí el PDF de la factura", type="pdf")

if archivo:
    st.success(f"✅ Archivo '{archivo.name}' recibido.")
    
    # Lógica Antigravity para Pedro
    if "FR" in archivo.name.upper() or "ALMUDENA" in archivo.name.upper():
        st.warning("⚠️ DETECTADA OPERACIÓN 03 (FRANCIA - ALMUDENA)")
        st.write("Estado: Listo para enviar a Supabase.")
    else:
        st.write("Estado: Factura Nacional detectada.")

    if st.button("Lanzar globos de éxito"):
        st.balloons()
