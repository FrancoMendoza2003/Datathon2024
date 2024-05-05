import json
import math

with open("data/productos.json") as f:
    data = json.load(f)
    modelos_nombres = [f"Modelo-{producto}" for producto in data["productos"]]
    categorias_productos = data["categorias"]
    categorias = data["categorias_unicas"]
    product_index = data["product_index"]
    index_product = {v: k for k, v in product_index.items()}

with open("data/vuelos.json") as f:
    data = json.load(f)
    aeronaves_opciones = data["aeronaves"]
    tipo_lugares_opciones = data["tipo_lugares"]
    origenes_opciones = data["origenes"]
    destinos_opciones = data["destinos"]

import streamlit as st
import pickle
import datetime

from utils.model import prepare_variables_product, prepare_variables


# Se cargan los modelos cargados en el archivo
for model_name in modelos_nombres:
    if f"model_{model_name}" not in st.session_state:
        st.session_state[f"model_{model_name}"] = pickle.load(
            open(
                f"../prediction/productos/renamed/{model_name}.pkl",
                "rb",
            )
        )

if "model_pasajeros" not in st.session_state:
    st.session_state["model_pasajeros"] = pickle.load(
        open(
            "../prediction/pasajeros/models/xgb_pasajeros_model.pickle",
            "rb",
        )
    )
if "model_booking" not in st.session_state:

    st.session_state["model_booking"] = pickle.load(
        open(
            "../prediction/pasajeros/models/xgb_bookings_model.pickle",
            "rb",
        )
    )

st.title("Cantidad de Productos en Vuelos")
st.subheader("Predicción de Productos en Vuelos a vender")

with st.form("productos"):
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

            # fmt: off
            prediction_passengers = st.session_state["model_pasajeros"].predict(variables)
            prediction_bookings = st.session_state["model_booking"].predict(variables)
            # fmt: on

            print("=======")
            print(prediction_passengers, prediction_bookings)
            print("=======")

            data = {
                "Aeronave": [aeronave],
                "DepartureStation": [origen],
                "ArrivalStation": [destino],
                "Destination_Type": [tipo_lugares_opciones[destino]],
                "Origin_Type": [tipo_lugares_opciones[origen]],
                "STD": [departure_datetime],
                "STA": [arrival_datetime],
                "Capacity": [capacidad],
                "Passengers": prediction_bookings,
                "Bookings": prediction_bookings,
                "Book_Pass": [prediction_bookings[0] / prediction_bookings[0]],
            }

            print(f"{data=}")

            predictions = {}

            models = [
                st.session_state[f"model_{model_name}"]
                for model_name in modelos_nombres
            ]
            for i, model in enumerate(models):
                variables = prepare_variables_product(data, model, i)
                try:
                    predictions[index_product[i]] = math.ceil(
                        model.predict(variables)[0]
                    )
                except Exception as e:
                    print("ERROR DE INFERENCIA")
                    continue

            format_str = ""
            for key, value in predictions.items():
                value = max(0, value - 2)
                if value == 0:
                    continue

                format_str += f"* {key}: {value}\n\n"
            st.success(
                f"Predicciones realizadas con éxito\n_________________________\n{format_str}"
            )
