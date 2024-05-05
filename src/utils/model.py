import json
import pandas as pd
import numpy as np

with open("data/vuelos.json") as f:
    data = json.load(f)
    aeronaves_opciones = data["aeronaves"]
    tipo_lugares_opciones = data["tipo_lugares"]
    origenes_opciones = data["origenes"]
    destinos_opciones = data["destinos"]


def one_hot_encode(
    df: pd.DataFrame,
    column: str,
    prefix: str,
) -> pd.DataFrame:

    df_ = df.copy()
    df_encoded = pd.get_dummies(df_[column], dtype="int")
    for col in df_encoded.columns:
        df_[f"{prefix}_{'_'.join(col.strip().lower().split())}"] = df_encoded[col]

    return df_.drop(columns=[column])


def prepare_variables(variables: dict) -> pd.DataFrame:

    variables_ = pd.DataFrame(variables)

    # fmt: off
    for val in list(set(tipo_lugares_opciones.values())):
        variables_[f"origen_{'_'.join(val.strip().lower().split())}"] = np.where(variables_["Origin_Type"] == val, 1, 0) 
        
    for val in list(set(tipo_lugares_opciones.values())):
        variables_[f"destino_{'_'.join(val.strip().lower().split())}"] = np.where(variables_["Destination_Type"] == val, 1, 0) 

    for val in origenes_opciones:
        variables_[f"arrival_{'_'.join(val.strip().lower().split())}"] = np.where(variables_["ArrivalStation"] == val, 1, 0) 
        
    for val in destinos_opciones:
        variables_[f"departure_{'_'.join(val.strip().lower().split())}"] = np.where(variables_["DepartureStation"] == val, 1, 0) 

    variables_ = variables_.drop(columns=["DepartureStation", "ArrivalStation", "Destination_Type", "Origin_Type"])

    # for col, prefix in zip([ "DepartureStation", "ArrivalStation", "Destination_Type", "Origin_Type"], [ "departure", "arrival", "destino", "origen"]):
    #         variables_encoded = pd.get_dummies(variables_[col], dtype="int")
    #         for col in variables_encoded.columns:
    #             variables_[f"{prefix}_{'_'.join(col.strip().lower().split())}"] = variables_encoded[col]

    #         for

    # variables_ = one_hot_encode(variables_, column=col, prefix=prefix)
    # fmt: on

    variables_["Dia"] = variables_["STD"].dt.day_of_year
    # fmt: off
    # variables_["STD"] = pd.to_datetime(variables_["STD"])
    # variables_["STA"] = pd.to_datetime(variables_["STA"])
    variables_["Mes"] = variables_["STD"].dt.month
    variables_["Semana"] = variables_["STD"].dt.isocalendar().week
    variables_["DiaSemana"] = variables_["STD"].dt.weekday + 1
    variables_["Hora"] = variables_["STD"].dt.hour
    variables_["HourDuration"] = (variables_["STA"] - variables_["STD"]).dt.total_seconds() / 3600
    # fmt: on

    variables_ = variables_.drop(columns=["STD"])

    dias_feriado = [
        1,  # Año Nuevo
        36,
        78,
        122,
        136,
        260,
        323,
        360,
        365,  # Año Nuevo
    ]

    variables_["DiasAFeriadoCercano"] = variables_["Dia"].apply(
        lambda x: min([abs(x - feriado) for feriado in dias_feriado])
    )

    # Dias entre 15 de julio y 28 de agosto
    vacaciones_verano = (variables_["Dia"] >= 197) & (variables_["Dia"] <= 241)
    # Dias entre 18 de diciembre y 5 de enero
    vacaciones_invierno = (variables_["Dia"] >= 353) & (variables_["Dia"] <= 5)
    # Dias entre 25 de marzo y 5 de abril
    vacaciones_diatrabajo = (variables_["Dia"] >= 85) & (variables_["Dia"] <= 96)

    variables_["VacacionesEscolares"] = np.where(
        (vacaciones_verano) | (vacaciones_invierno) | (vacaciones_diatrabajo),
        1,
        0,
    )

    variables_ = variables_.drop(columns=["STA", "Aeronave"])

    variables_ = variables_[
        [
            "Capacity",
            "Mes",
            "Semana",
            "DiaSemana",
            "Hora",
            "HourDuration",
            "departure_ab",
            "departure_ac",
            "departure_ad",
            "departure_ae",
            "departure_af",
            "departure_ai",
            "departure_aj",
            "departure_ak",
            "departure_al",
            "departure_am",
            "departure_ao",
            "departure_ap",
            "departure_aq",
            "departure_ar",
            "departure_as",
            "departure_at",
            "departure_au",
            "departure_av",
            "departure_aw",
            "departure_ax",
            "departure_ay",
            "departure_az",
            "departure_ba",
            "departure_bb",
            "departure_bc",
            "departure_bd",
            "departure_be",
            "departure_bf",
            "departure_bg",
            "departure_bh",
            "departure_bi",
            "departure_bj",
            "departure_bk",
            "departure_bl",
            "departure_bm",
            "departure_bn",
            "departure_bo",
            "departure_bp",
            "departure_bq",
            "departure_bs",
            "departure_bt",
            "arrival_ab",
            "arrival_ac",
            "arrival_ad",
            "arrival_ae",
            "arrival_af",
            "arrival_ai",
            "arrival_aj",
            "arrival_ak",
            "arrival_al",
            "arrival_am",
            "arrival_ao",
            "arrival_ap",
            "arrival_aq",
            "arrival_ar",
            "arrival_as",
            "arrival_at",
            "arrival_au",
            "arrival_av",
            "arrival_aw",
            "arrival_ax",
            "arrival_ay",
            "arrival_az",
            "arrival_ba",
            "arrival_bb",
            "arrival_bc",
            "arrival_bd",
            "arrival_be",
            "arrival_bf",
            "arrival_bg",
            "arrival_bh",
            "arrival_bi",
            "arrival_bj",
            "arrival_bk",
            "arrival_bl",
            "arrival_bm",
            "arrival_bn",
            "arrival_bo",
            "arrival_bp",
            "arrival_bq",
            "arrival_bs",
            "arrival_bt",
            "destino_ciudad_fronteriza",
            "destino_ciudad_principal",
            "destino_ecoturismo",
            "destino_mx_amigos_y_familia",
            "destino_playa",
            "origen_ciudad_fronteriza",
            "origen_ciudad_principal",
            "origen_ecoturismo",
            "origen_mx_amigos_y_familia",
            "origen_playa",
            "Dia",
            "DiasAFeriadoCercano",
            "VacacionesEscolares",
        ]
    ]

    variables_.to_csv("test_.csv", index=False)

    return variables_
