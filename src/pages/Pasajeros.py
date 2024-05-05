import json
import math

with open("data/vuelos.json") as f:
    data = json.load(f)
    aeronaves_opciones = data["aeronaves"]
    tipo_lugares_opciones = data["tipo_lugares"]
    origenes_opciones = data["origenes"]
    destinos_opciones = data["destinos"]

import streamlit as st
import pickle
import datetime

from utils.model import prepare_variables

# Aeronave	DepartureStation	ArrivalStation	Destination_Type	Origin_Type	STD	STA	Capacity

if "model_pasajeros" not in st.session_state:
    st.session_state["model_pasajeros"] = pickle.load(
        open(
            "../prediction/pasajeros/models/xgb_pasajeros_model.pickle",
            "rb",
        )
    )


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
        datetime.date(2023, 1, 1),
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

    departure_datetime = datetime.datetime.combine(departure_date, departure_time)
    arrival_datetime = datetime.datetime.combine(departure_date, arrival_time)

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
        # fmt: off
        if departure_datetime >= arrival_datetime:
            st.error("La fecha de salida no puede ser menor o igual a la fecha de llegada", icon="🚨")
        if origen == destino:
            st.error("El origen y el destino no pueden ser iguales", icon="🚨")
        # fmt: on

        else:
            data = {
                "Aeronave": [aeronave],
                "DepartureStation": [origen],
                "ArrivalStation": [destino],
                "Destination_Type": [tipo_lugares_opciones[destino]],
                "Origin_Type": [tipo_lugares_opciones[origen]],
                "STD": [departure_datetime],
                "STA": [arrival_datetime],
                "Capacity": [capacidad],
            }

            variables = prepare_variables(data)

            variables.to_csv("test_.csv", index=False)

            prediction = st.session_state["model_pasajeros"].predict(variables)

            st.success(
                f"Se espera un volumen de {min(math.floor(prediction), capacidad)} pasajeros"
            )
