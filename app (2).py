"""Interfaz: streamlit run app.py"""
import streamlit as st
import streamlit.components.v1 as components
from lector import leer_archivo
from gerente import decidir_area
from agentes import ejecutar_agente, AGENTES, CLAVE
from oficina import html_oficina

st.set_page_config(page_title="Oficina Virtual", page_icon="🏢", layout="wide")
st.title("🏢 Oficina Virtual")

if not CLAVE:
    st.error("Falta la clave de la API. En Streamlit Cloud ve a ⋮ → Settings → Secrets y agrega: "
             'ANTHROPIC_API_KEY = "tu_clave"')
    st.stop()

oficina = st.empty()


def mostrar(estado="espera", area=None, mensaje=""):
    with oficina.container():
        components.html(html_oficina(estado, area, mensaje), height=470)


mostrar()

archivo = st.file_uploader("Sube un documento (CSV, Excel, PDF o TXT)", type=["csv", "xlsx", "xls", "pdf", "txt"])
pregunta = st.text_input("¿Qué necesitas? (opcional)", placeholder="Ej: proyecta las ventas de los próximos 6 meses")

if st.button("Enviar al gerente", type="primary", disabled=archivo is None):
    try:
        documento = leer_archivo(archivo.name, archivo.getvalue())
    except Exception as e:
        st.error(f"No pude leer el archivo: {e}")
        st.stop()

    mostrar("gerente", mensaje="Revisando el documento…")
    decision = decidir_area(documento, pregunta)
    area = decision["area"]
    st.info(f"🧑‍💼 Gerente → {AGENTES[area]['emoji']} **{AGENTES[area]['nombre']}**: {decision['razon']}")

    mostrar("area", area)
    estado = st.empty()
    respuesta = ejecutar_agente(area, documento, pregunta, avisar=estado.caption)
    estado.empty()

    mostrar("listo", area, "¡Listo!")
    st.markdown(respuesta)
