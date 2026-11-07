"""Interfaz: streamlit run app.py"""
import streamlit as st
from lector import leer_archivo
from gerente import decidir_area
from agentes import ejecutar_agente, AGENTES

st.set_page_config(page_title="Oficina Virtual", page_icon="🏢", layout="wide")
st.title("🏢 Oficina Virtual")

def dibujar_oficina(activa=None, gerente_activo=False):
    cols = st.columns(5)
    cols[0].markdown(f"### {'🟢' if gerente_activo else '⚪'} 🧑‍💼\n**Gerente**")
    for col, (clave, a) in zip(cols[1:], AGENTES.items()):
        col.markdown(f"### {'🟢' if clave == activa else '⚪'} {a['emoji']}\n**{a['nombre']}**")

oficina = st.empty()
with oficina.container():
    dibujar_oficina()

archivo = st.file_uploader("Sube un documento (CSV, Excel, PDF o TXT)", type=["csv", "xlsx", "xls", "pdf", "txt"])
pregunta = st.text_input("¿Qué necesitas? (opcional)", placeholder="Ej: proyecta las ventas de los próximos 6 meses")

if st.button("Enviar al gerente", type="primary", disabled=archivo is None):
    try:
        documento = leer_archivo(archivo.name, archivo.getvalue())
    except Exception as e:
        st.error(f"No pude leer el archivo: {e}")
        st.stop()

    with oficina.container():
        dibujar_oficina(gerente_activo=True)
    with st.spinner("El gerente está revisando el documento…"):
        decision = decidir_area(documento, pregunta)
    area = decision["area"]
    st.info(f"🧑‍💼 Gerente → {AGENTES[area]['emoji']} **{AGENTES[area]['nombre']}**: {decision['razon']}")

    with oficina.container():
        dibujar_oficina(activa=area)
    estado = st.empty()
    with st.spinner(f"{AGENTES[area]['nombre']} está trabajando…"):
        respuesta = ejecutar_agente(area, documento, pregunta, avisar=estado.caption)
    estado.empty()
    st.markdown(respuesta)
