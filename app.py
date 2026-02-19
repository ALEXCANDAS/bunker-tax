import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE FILTROS SUPERIORES (Segmentación Total)
with tab_registro:
    st.subheader("📋 Auditoría y Control de Modelos")
    
    # Fila de Filtros (Segmentación)
    f1, f2, f3, f4, f5 = st.columns([1, 1, 1, 1.5, 1])
    tipo_filtro = f1.selectbox("TIPO", ["Todas", "Recibidas", "Emitidas"])
    tri_filtro = f2.selectbox("TRIMESTRE", ["Todos", "1T", "2T", "3T", "4T"])
    mod_filtro = f3.selectbox("MODELO", ["Todos", "303", "111", "347", "190"])
    nif_filtro = f4.text_input("BUSCAR NIF / PROVEEDOR", placeholder="Ej: B123...")
    estado_filtro = f5.selectbox("ESTADO", ["Todos", "✅ Cuadrado", "⚠️ Pendiente"])

    st.divider()

    # 2. TABLA DE REGISTRO CON MINIATURAS Y BANDERAS
    # Definimos la estructura de columnas para que quepa todo sin scroll horizontal molesto
    header = st.columns([0.6, 1, 2, 1, 1, 2, 0.8])
    header[0].write("**Estado**")
    header[1].write("**Fecha**")
    header[2].write("**Sujeto / NIF**")
    header[3].write("**Total**")
    header[4].write("**Tipo**")
    header[5].write("**Banderas de Modelo**")
    header[6].write("**Acción**")

    # Datos simulados que reaccionan a los filtros
    registros = [
        {"status": "✅", "fecha": "19/02/2026", "sujeto": "BAR PLAZA", "nif": "B888888", "total": "15,00€", "tipo": "Recibida", "modelos": ["303"]},
        {"status": "✅", "fecha": "18/02/2026", "sujeto": "ABOGADOS S.L.", "nif": "B999999", "total": "242,00€", "tipo": "Recibida", "modelos": ["303", "111"]},
        {"status": "⚠️", "fecha": "15/02/2026", "sujeto": "CLIENTE FINAL SL", "nif": "B111111", "total": "1.210,00€", "tipo": "Emitida", "modelos": ["303", "347"]},
    ]

    for reg in registros:
        # Lógica de filtrado simple (para el prototipo)
        if tipo_filtro != "Todas" and tipo_filtro[:-1] != reg["tipo"]: continue
        
        row = st.columns([0.6, 1, 2, 1, 1, 2, 0.8])
        row[0].write(reg["status"])
        row[1].write(reg["fecha"])
        row[2].write(f"**{reg['sujeto']}**\n{reg['nif']}")
        row[3].write(reg["total"])
        row[4].write(reg["tipo"])
        
        # Banderas con colores según modelo
        banderas = ""
        for m in reg["modelos"]:
            color = "#01579b" if m == "303" else "#e65100" if m == "111" else "#4a148c"
            banderas += f'<span style="background:{color}; color:white; padding:2px 6px; border-radius:4px; margin-right:5px; font-size:11px;">M-{m}</span>'
        row[5].markdown(banderas, unsafe_allow_html=True)
        
        # EL BOTÓN DE ACCIÓN: Abre un "pop-over" o expander con la imagen
        with row[6].expander("👁️"):
            st.image("https://via.placeholder.com/400x500?text=VISTA+PREVIA+FACTURA", caption=f"Documento: {reg['sujeto']}")
            if st.button("Editar Asiento", key=reg['sujeto']):
                st.info("Cargando en pestaña de edición...")
