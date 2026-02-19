import streamlit as st

# 1. NAVEGACIÓN GLOBAL
tab_recibidas, tab_emitidas, tab_registro = st.tabs(["📥 RECIBIDAS", "📤 EMITIDAS", "📋 CONTROL DE MODELOS"])

with tab_registro:
    # FILTROS DE SEGMENTACIÓN (Arriba, fijos)
    f1, f2, f3, f4 = st.columns([1, 1, 1, 2])
    f_tri = f1.selectbox("TRIMESTRE", ["Todos", "1T", "2T", "3T", "4T"])
    f_mod = f2.selectbox("MODELO", ["Todos", "303", "111", "347", "390"])
    f_tipo = f3.selectbox("FLUJO", ["Todos", "Recibidas", "Emitidas"])
    f_search = f4.text_input("🔍 BUSCAR NIF / NOMBRE", placeholder="Filtro rápido...")

    st.divider()

    # 2. CABECERA DE AUDITORÍA (Aprovechando el ancho del LG)
    # Estado | Fecha | Sujeto/NIF | Base | IVA | Ret. | Total | Banderas | Doc
    h = st.columns([0.5, 0.8, 1.8, 0.8, 0.8, 0.8, 0.8, 1.5, 0.5])
    headers = ["ST", "FECHA", "SUJETO / NIF", "BASE", "IVA", "RET.", "TOTAL", "MODELOS", "VISOR"]
    for col, text in zip(h, headers):
        col.markdown(f"**{text}**")

    # 3. FILAS DE DATOS (Mecánica de Punteo 390/111)
    def fila_registro(st_icon, fecha, nombre, nif, base, iva, ret, total, modelos):
        r = st.columns([0.5, 0.8, 1.8, 0.8, 0.8, 0.8, 0.8, 1.5, 0.5])
        r[0].write(st_icon)
        r[1].write(fecha)
        r[2].markdown(f"**{nombre}** \n<small>{nif}</small>", unsafe_allow_html=True)
        r[3].write(f"{base}€")
        r[4].write(f"{iva}€")
        r[5].write(f"{ret}€" if ret > 0 else "-")
        r[6].write(f"**{total}€**")
        
        # Banderas visuales por colores
        banderas = ""
        for m in modelos:
            if m == "303": color = "#01579b" # Azul IVA
            elif m == "111": color = "#e65100" # Naranja Ret
            elif m == "347": color = "#4a148c" # Púrpura 347
            else: color = "#37474f"
            banderas += f'<span style="background:{color}; color:white; padding:2px 6px; border-radius:4px; margin-right:4px; font-size:10px;">M-{m}</span>'
        r[7].markdown(banderas, unsafe_allow_html=True)
        
        # Visor de factura sin romper la fila
        with r[8].expander("👁️"):
            st.image("https://via.placeholder.com/350x450?text=FACTURA+RECIBIDA", use_container_width=True)
            st.button("Editar", key=nombre)

    # Simulación de registros con datos para puntear el 390
    fila_registro("✅", "19/02", "BAR EL GRIEGO", "B12345678", "66.34", "6.63", 0, "72.97", ["303"])
    fila_registro("✅", "18/02", "AUDITORES ASOC.", "B99988877", "200.00", "42.00", 30.00, "212.00", ["303", "111"])
    fila_registro("⚠️", "15/02", "CONSTRUCTORA X", "B55544433", "4000.00", "840.00", 0, "4840.00", ["303", "347"])

    st.divider()
    # TOTALES DE CONTROL (Para cuadrar el 390 al momento)
    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Suma Bases", "4.266,34 €")
    t2.metric("Suma IVA", "888,63 €")
    t3.metric("Suma Retenciones", "30,00 €")
    t4.metric("Total Acumulado", "5.124,97 €")
