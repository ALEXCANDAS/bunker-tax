# Así era la estructura del "Dato Tabulador" que vimos:
import streamlit as st

col_pdf, col_datos = st.columns([1.5, 1]) # Pantalla partida

with col_pdf:
    st.subheader("Documento Original")
    # Aquí se visualiza el PDF sin que tape nada
    st.markdown(f'<iframe src="{pdf_url}" width="100%" height="800"></iframe>', unsafe_allow_html=True)

with col_datos:
    st.subheader("Registro Contable")
    # Formulario rápido para "tabular"
    with st.form("registro_factura"):
        nif = st.text_input("NIF Emisor", value=dato_ia['nif'])
        base = st.text_input("Base Imponible", value=dato_ia['base'])
        iva = st.text_input("Cuota IVA", value=dato_ia['iva'])
        total = st.text_input("Total Factura", value=dato_ia['total'])
        
        # El botón que lo manda todo al A3/n8n
        if st.form_submit_button("REGISTRAR Y SIGUIENTE (Enter)"):
            enviar_a_n8n(nif, base, iva, total)
            st.success("¡Registrado!")
