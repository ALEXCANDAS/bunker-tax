import streamlit as st

# 1. Configuración de pantalla ancha (estilo Dashboard)
st.set_page_config(page_title="BUNKER TAX PRO", page_icon="🛡️", layout="wide")

# 2. Barra lateral estilo SaaS
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5717/5717462.png", width=100)
    st.title("MENÚ BÚNKER")
    opcion = st.radio("Ir a:", ["Dashboard", "Subir Facturas", "Historial", "Clientes (8)"])
    st.info("Usuario: Alejandro\nNivel: Antigravity")

# 3. Cuerpo principal
if opcion == "Dashboard":
    st.title("📊 Dashboard de Control")
    
    # Métricas que impresionan a Pedro
    col1, col2, col3 = st.columns(3)
    col1.metric("Facturas Hoy", "12", "+2")
    col2.metric("Total Mes", "14.500 €", "15%")
    col3.metric("Pendientes", "3", "-1")
    
    st.write("### Últimos Movimientos")
    st.table([{"Cliente": "Almudena", "Operación": "03 Francia", "Estado": "OK"},
              {"Cliente": "Pedro", "Operación": "Nacional", "Estado": "Pendiente"}])

elif opcion == "Subir Facturas":
    st.title("📥 Buzón de Entrada")
    archivo = st.file_uploader("Arrastra el PDF aquí", type="pdf")
    if archivo:
        st.success(f"Archivo {archivo.name} listo para procesar.")
        if st.button("Analizar con Gemini"):
            st.snow() # Un toque de magia
            st.write("Simulando análisis... Detectado Importe: 1.200€")
