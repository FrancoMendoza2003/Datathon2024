import json

with open("data/vuelos.json") as f:
    data = json.load(f)
    aeronaves_opciones = data["aeronaves"]
    origenes_opciones = data["origenes"]
    destinos_opciones = data["destinos"]

import streamlit as st
import datetime

# Aeronave	DepartureStation	ArrivalStation	Destination_Type	Origin_Type	STD	STA	Capacity

st.title("Pasajeros en VivaAerobus")
st.subheader("Predicción de volumetría de pasajeros")

with st.form("pasajeros"):
    st.write("Introduce los datos del vuelo")

    left, right = st.columns(2)

    aeronave = left.selectbox(
        "Aeronave",
        aeronaves_opciones,
    )

    capacidad = right.slider(
        "Capacidad de la aeronave",
        min_value=150,
        max_value=275,
        step=5,
        key="capacidad",
    )

    departure_date = st.date_input(
        "Fecha de departo del vuelo",
        datetime.date(2019, 7, 6),
        key="departure_date",
    )

    left, right = st.columns(2)

    departure_time = left.time_input(
        "Hora del departo del vuelo",
        datetime.time(8, 45, 0),
        key="departure_time",
        step=60 * 5,
    )

    arrival_time = right.time_input(
        "Hora de de llegada del vuelo",
        datetime.time(8, 45, 0),
        key="arrival_time",
        step=60 * 5,
    )

    origen = left.selectbox(
        "Origen",
        origenes_opciones,
    )

    destino = right.selectbox(
        "Destino",
        destinos_opciones,
    )

    # Every form must have a submit button.
    submitted = st.form_submit_button("Predice!")

    if submitted:
        ...


st.write("This is the flights page")
