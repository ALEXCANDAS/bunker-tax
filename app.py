import streamlit as st
import pandas as pd
import numpy as np

# 1. MOTOR DE DATOS (Sin errores de definición)
if 'base' not in st.session_state: st.session_state.base = 100.0
if 'iva_p' not in st.session_state: st.session_state.iva_p = 21

def calc():
    st.session_state.cuota = round(st.session_state.base * (st.session_state.iva_p / 100), 2)
    st.session_state.total = round(st.session_state.base + st.session_state.cuota, 2)

if 'total' not in st.session_state: calc()

# 2. CONFIGURACIÓN VISUAL
st.set_page_config(layout="wide", page_title="Búnker Pro | Auditoría y Analítica")

st.markdown("""
    <style>
    .mod-card { background: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; text-align: center; }
    .status-ok { color: #16a34a; font-weight: bold; }
    .status-pending { color: #ca8a04; font-weight: bold; }
    .asiento-table { width: 100%; border-collapse: collapse; font-family: monospace; }
    .asiento-table td { padding: 8px; border-bottom: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

# 3. NAVEGACIÓN
tab_rec, tab_emi, tab_impuestos, tab_analitica = st.tabs([
    "📥 RECIBIDAS", "📤 EMITIDAS", "📋 ESTADO MODELOS", "📈 EVOLUCIÓN BI"
])

# --- PANTALLAS DE TRABAJO (RECIBIDAS / EMITIDAS) ---
def screen_work(tipo):
    col_doc, col_asiento, col_ficha = st.columns([1, 1, 1.2])
    with col_doc:
        st.markdown("### 📄 Documento")
        st.markdown('<div style="background:#334155; height:350px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white;">VISOR PDF</div>', unsafe_allow_html=True)
    with col_asiento:
        st.markdown("### ⚙️ Asiento D/H")
        st.markdown(f"""
        <table class="asiento-table">
            <tr style="background:#f1f5f9;"><th>Cuenta</th><th>Debe</th><th>Haber</th></tr>
            <tr><td>(629/700)</td><td>{st.session_state.base:,.2f}</td><td></td></tr>
            <tr><td>(472/477)</td><td>{st.session_state.cuota:,.2f}</td><td></td></tr>
            <tr style="font-weight:bold;"><td>(410/430)</td><td></td><td>{st.session_state.total:,.2f}</td></tr>
        </table>
        """, unsafe_allow_html=True)
    with col_ficha:
        st.markdown(f"### ⚡ Registro {tipo}")
        c1, c2, c3 = st.columns([2, 1, 0.5])
        c1.text_input("SUJETO", value="ADOBE SYSTEMS IE", key=f"s_{tipo}")
        c2.text_input("NIF", value="IE6362892H", key=f"n_{tipo}")
        c3.markdown("## 🇪🇺")
        st.divider()
        i1, i2, i3 = st.columns(3)
        st.session_state.base = i1.number_input("BASE", value=st.session_state.base, on_change=calc, key=f"b_{tipo}")
        st.session_state.iva_p = i2.selectbox("IVA %", [21, 10, 4, 0], on_change=calc, key=f"v_{tipo}")
        st.session_state.total = i3.number_input("TOTAL", value=st.session_state.total, key=f"t_{tipo}")
        st.button(f"🚀 REGISTRAR (ENTER)", use_container_width=True, type="primary", key=f"btn_{tipo}")

with tab_rec: screen_work("RECIBIDAS")
with tab_emi: screen_work("EMITIDAS")

# --- PANTALLA: ESTADO MODELOS (Lo de "ayer" todos juntos) ---
with tab_impuestos:
    st.header("🏁 Estado de Obligaciones Fiscales")
    c1, c2, c3, c4, c5 = st.columns(5)
    
    models = [
        ("M-303", "✅ PRESENTADO", "status-ok"),
        ("M-111", "⚠️ PENDIENTE", "status-pending"),
        ("M-115", "✅ PRESENTADO", "status-ok"),
        ("M-349", "✅ PRESENTADO", "status-ok"),
        ("M-347", "🔍 EN REVISIÓN", "status-pending")
    ]
    
    cols = [c1, c2, c3, c4, c5]
    for col, (name, status, style) in zip(cols, models):
        col.markdown(f"""
        <div class="mod-card">
            <h3>{name}</h3>
            <p class="{style}">{status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("⚠️ Alertas de Auditoría (Marina vs IA)")
    st.error("NIF IE6362892H (Adobe) detectado como Nacional. ¿Falta bandera 🇪🇺 y Modelo 349?")

# --- PANTALLA: EVOLUCIÓN BI (Gráficas por Cliente/Gasto) ---
with tab_analitica:
    st.header("📈 Evolución y Analítica de Negocio")
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("Ingresos vs Gastos (Mensual)")
        chart_data = pd.DataFrame(np.random.randn(12, 2), columns=['Ingresos', 'Gastos'])
        st.line_chart(chart_data)
        
    with col_g2:
        st.subheader("Top Clientes / Proveedores")
        source = pd.DataFrame({
            "Sujeto": ["Cliente A", "Cliente B", "Adobe", "Amazon", "Bar Plaza"],
            "Volumen": [4500, 3200, 1200, 800, 450]
        })
        st.bar_chart(source.set_index("Sujeto"))

    st.divider()
    st.subheader("🔍 Desglose por Tipo de Gasto")
    st.dataframe(pd.DataFrame({
        "Cuenta": ["629.0", "600.0", "621.0", "623.0"],
        "Concepto": ["Suministros", "Compras", "Arrendamientos", "Prof. Indep."],
        "Total Año": ["12.450€", "45.200€", "8.400€", "3.100€"],
        "Variación %": ["+5%", "-2%", "0%", "+15%"]
    }), use_container_width=True)
