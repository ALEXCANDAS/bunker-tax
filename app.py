import streamlit as st

# 1. MOTOR ESTABLE (Sin errores de formulario)
if 'base' not in st.session_state: st.session_state.base = 100.0
if 'iva' not in st.session_state: st.session_state.iva = 21
if 'isp' not in st.session_state: st.session_state.isp = False

def calc():
    # IVA e Inversión del Sujeto Pasivo
    st.session_state.cuota = round(st.session_state.base * (st.session_state.iva / 100), 2)
    if st.session_state.isp:
        st.session_state.total = st.session_state.base # ISP no suma IVA al total
    else:
        st.session_state.total = round(st.session_state.base + st.session_state.cuota, 2)

if 'total' not in st.session_state: calc()

st.set_page_config(layout="wide")
st.title("🛡️ Búnker Pro | Validación Final")

# 2. INTERFAZ DE TRABAJO
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    st.subheader("📄 Datos Factura")
    prov = st.text_input("Proveedor", value="ADOBE")
    nif = st.text_input("NIF", value="IE6362892H")
    org = st.selectbox("Origen", ["España 🇪🇸", "Europa 🇪🇺", "Extra 🌎"], index=1)

with c2:
    st.subheader("⚙️ Configuración")
    st.session_state.isp = st.checkbox("Inversión Sujeto Pasivo (ISP)", value=st.session_state.isp, on_change=calc)
    st.session_state.base = st.number_input("Base Imponible", value=st.session_state.base, on_change=calc)
    st.session_state.iva = st.selectbox("IVA %", [21, 10, 4, 0], index=0, on_change=calc)

with c3:
    st.subheader("💵 Resultado")
    st.metric("Total Factura", f"{st.session_state.total} €")
    st.metric("Cuota IVA", f"{st.session_state.cuota} €")
    if st.button("🚀 REGISTRAR ASIENTO"):
        st.success("Asiento enviado al libro de registro.")

st.divider()

# 3. LIBRO DE REGISTRO SENCILLO (SIN ERRORES)
st.subheader("📋 Libro de Registro")
cols = st.columns([1, 1, 1, 1, 1, 1])
headers = ["SUJETO", "BASE", "IVA", "TOTAL", "ISP", "MODELOS"]
for col, h in zip(cols, headers): col.write(f"**{h}**")

# Fila de ejemplo
f = st.columns([1, 1, 1, 1, 1, 1])
f[0].write(prov)
f[1].write(f"{st.session_state.base}€")
f[2].write(f"{st.session_state.cuota}€")
f[3].write(f"{st.session_state.total}€")
f[4].write("SÍ" if st.session_state.isp else "NO")
f[5].write("303, 349" if org == "Europa 🇪🇺" else "303")
