import streamlit as st

# 1. MOTOR CONTABLE AVANZADO
if 'base' not in st.session_state: st.session_state.base = 100.00
if 'iva_p' not in st.session_state: st.session_state.iva_p = 21
if 'ret_p' not in st.session_state: st.session_state.ret_p = 0
if 'isp' not in st.session_state: st.session_state.isp = False

def calcular_todo():
    # IVA y Retención
    st.session_state.cuota_iva = round(st.session_state.base * (st.session_state.iva_p / 100), 2)
    st.session_state.cuota_ret = round(st.session_state.base * (st.session_state.ret_p / 100), 2)
    
    # Si es ISP, el IVA no suma al total de la factura (se autorrepercute)
    if st.session_state.isp:
        st.session_state.total = round(st.session_state.base - st.session_state.cuota_ret, 2)
    else:
        st.session_state.total = round(st.session_state.base + st.session_state.cuota_iva - st.session_state.cuota_ret, 2)

if 'cuota_iva' not in st.session_state: calcular_todo()

# 2. INTERFAZ PROFESIONAL
st.set_page_config(layout="wide", page_title="Búnker Pro | Auditoría Contable")

with st.container(border=True):
    col_pdf, col_ficha = st.columns([1, 1.2])
    
    with col_pdf:
        st.markdown("### 📄 Documento / Asiento")
        st.markdown('<div style="background:#f8fafc; height:350px; border:1px solid #cbd5e1; border-radius:8px; padding:10px;">'
                    '<strong>🔍 PREVISUALIZACIÓN ASIENTO:</strong><br><br>'
                    f'629.000 Gasto: {st.session_state.base}€ (D)<br>'
                    f'472.000 IVA Sop: {st.session_state.cuota_iva}€ (D)<br>'
                    + (f'477.000 IVA Rep (ISP): {st.session_state.cuota_iva}€ (H)<br>' if st.session_state.isp else '')
                    + (f'475.100 Retención: {st.session_state.cuota_ret}€ (H)<br>' if st.session_state.ret_p > 0 else '')
                    + f'410.000 Acreedor: {st.session_state.total}€ (H)'
                    +'</div>', unsafe_allow_html=True)
        st.info("💡 ISP: Se genera autorrepercusión automática.")

    with col_ficha:
        with st.form("form_pro"):
            st.markdown("### ⚡ Validación Avanzada")
            
            c1, c2, c3 = st.columns([2, 1, 0.5])
            c1.text_input("PROVEEDOR", value="ADOBE SYSTEMS IE")
            c2.text_input("NIF", value="IE6362892H")
            c3.markdown("## 🇪🇺")

            # Fila de Control Fiscal
            o1, o2, o3 = st.columns([1, 1, 1])
            o1.checkbox("INVERSIÓN SUJETO PASIVO (ISP)", key="isp", on_change=calcular_todo)
            o2.text_input("CTA. GASTO", value="629.000")
            o3.selectbox("RETENCIÓN %", [0, 7, 15, 19], key="ret_p", on_change=calcular_todo)

            st.divider()

            # NÚCLEO REACTIVO
            i1, i2, i3 = st.columns([1, 0.8, 1])
            i1.number_input("BASE IMPONIBLE", key="base", on_change=calcular_todo, format="%.2f")
            i2.selectbox("IVA %", [21, 10, 4, 0], key="iva_p", on_change=calcular_todo)
            i3.number_input("TOTAL FACTURA", key="total", format="%.2f")

            st.form_submit_button("🚀 REGISTRAR (ENTER)", use_container_width=True, type="primary")

# --- REGISTRO CON BANDERAS ISP Y RET ---
st.subheader("📋 Libro de Registro de Facturas")
h = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.2, 0.4])
headers = ["AUD", "ORG", "FECHA", "SUJETO", "BASE", "IVA", "RET", "TOTAL", "MODELOS", "VIS"]
for col, text in zip(h, headers): col.markdown(f"**{text}**")

def fila(aud, flag, fecha, nombre, base, iva, ret, total, modelos, isp=False):
    r = st.columns([0.4, 0.5, 0.8, 2, 0.8, 0.8, 0.8, 0.8, 1.2, 0.4])
    r[0].write("✅")
    r[1].markdown(f"### {flag}")
    r[2].write(fecha)
    r[3].markdown(f"**{nombre}**" + (" <br><small><b>ISP (Inversión)</b></small>" if isp else ""), unsafe_allow_html=True)
    r[4].write(f"{base}€")
    r[5].write(f"{iva}€")
    r[6].write(f"{ret}€")
    r[7].write(f"**{total}€**")
    
    m_html = "".join([f'<span style="background:#01579b;color:white;padding:2px 5px;border-radius:3px;margin-right:2px;font-size:10px;">{m}</span>' for m in modelos])
    r[8].markdown(m_html, unsafe_allow_html=True)
    r[9].button("👁️", key=nombre)

fila("ok", "🇪🇺", "19/02", "ADOBE SYSTEMS", st.session_state.base, st.session_state.cuota_iva, st.session_state.cuota_ret, st.session_state.total, ["303", "349"], isp=st.session_state.isp)
