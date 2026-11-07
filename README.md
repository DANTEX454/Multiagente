# 🏢 Oficina Virtual (gerente + 4 áreas)

El gerente recibe el documento y lo envía al área adecuada:
📒 Contabilidad · 📐 Proyectos · 🩺 Diagnóstico · 📈 Proyecciones

## Instalación (Linux / Chromebook)
```bash
cd oficina_virtual
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY="tu_clave"     # se obtiene en console.anthropic.com
streamlit run app.py
```
Prueba con `ventas_demo.csv` y la solicitud: "proyecta las ventas de los próximos 6 meses".

## Estructura
- `app.py` interfaz · `gerente.py` clasifica · `agentes.py` los 4 agentes
- `calculos.py` cálculos reales en Python (VPN/TIR, razones, proyección, partida doble)
- `lector.py` convierte CSV/Excel/PDF a texto

## Cómo agregar un área nueva
Añade una entrada en `AGENTES` (agentes.py), su herramienta en `calculos.py`,
y menciónala en el prompt de `gerente.py`.
