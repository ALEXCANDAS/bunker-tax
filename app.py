import streamlit as st
import pandas as pd

# 1. PANTALLA PRO (Estándar Estonia)
st.set_page_config(layout="wide", page_title="Búnker Pro", initial_sidebar_state="collapsed")

# 2. EL ADN DE DATOS (Los 28 campos que pide el .dat)
COLUMNAS_MAESTRAS = [
    "ESTADO", "FECHA_FACTURA", "NIF", "CUENTA_CONTRA", "TOTAL", 
    "BI1", "IVA1", "CUOTA1", "BI2", "IVA2", "CUOTA2", "BI3", "IVA3", "CUOTA3",
    "TRIMESTRE", "TIPO_OPERACION", "CATEGORIA", "ID_FACTURA", "ID_TERCERO",
    "CP_TERCERO", "RETENCION_%", "RETENCION_€", "IMPRESO", "CUENTA_BASE"
]

# 3. MEMORIA DE TRABAJO (Para que no se pierda nada al recargar)
if 'df_db' not in st.session_state:
    st.session_state.df_db = pd.DataFrame([{c: "" for c in COLUMNAS_MAESTRAS} for _ in range(50)])
if 'vista_pro' not in st.session_state:
    st.session_state.vista_pro = ["ESTADO", "FECHA_FACTURA", "CUENTA_CONTRA", "NIF", "TOTAL"]

# --- ACCIONES RÁPIDAS (Top Bar) ---
c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    st.title("🛡️ Búnker Control")
    st.caption(f"Operativa Activa: {st.session_state.get('empresa', '001')}")
with c2:
    if st.button("🔄 SYNC DRIVE", type="primary", use_container_width=True):
        st.toast("Iniciando escaneo inteligente...")
with c3:
    st.button("📦 GEN .DAT", use_container_width=True)

# --- PANEL DE CONFIGURACIÓN DINÁMICA ---
with st.expander("⚙️ AJUSTE DE PANTALLA (Añadir/Quitar Columnas)"):
    st.session_state.vista_pro = st.multiselect(
        "Columnas en visión:", options=COLUMNAS_MAESTRAS, default=st.session_state.vista_pro
    )

# --- EL MOTOR DE ASIENTOS (Edición Directa Anti-Holded) ---
# Aquí es donde ocurre la magia: Clic, Escribe, Tab, Enter.
edited_df = st.data_editor(
    st.session_state.df_db[st.session_state.vista_pro],
    use_container_width=True,
    hide_index=True,
    num_rows="dynamic",
    key="editor_central",
    column_config={
        "ESTADO": st.column_config.SelectboxColumn(options=["⚡ Pendiente", "✅ OK", "⚠️ Error"]),
        "TOTAL": st.column_config.NumberColumn(format="%.2f €"),
        "FECHA_FACTURA": st.column_config.TextColumn("Fecha"),
        "IVA1": st.column_config.SelectboxColumn(options=["21%", "10%", "4%", "0%"])
    }
)

# Sincronizamos los cambios de la tabla con la base de datos de 28 columnas
if st.button("💾 Guardar Sesión"):
    st.session_state.df_db.update(edited_df)
    st.balloons()

st.caption("🚀 **Antigravity Focus:** Estructura lista para inyección de datos vía Gemini.")
