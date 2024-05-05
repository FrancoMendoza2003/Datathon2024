import pandas as pd
import numpy as np


def prepare_variables(variables: dict) -> pd.DataFrame:

    variables_ = pd.DataFrame(variables)

    # fmt: off
    for col, prefix in zip([ "DepartureStation", "ArrivalStation", "Destination_Type", "Origin_Type"], [ "departure", "arrival", "destino", "origen"]):
            variables_encoded = pd.get_dummies(variables_[col], dtype="int")
            for col in variables_encoded.columns:
                variables_[f"{prefix}_{'_'.join(col.strip().lower().split())}"] = variables_encoded[col]

    # variables_ = one_hot_encode(variables_, column=col, prefix=prefix)
    # fmt: on

    variables_["Dia"] = variables_["STD"].dt.day_of_year
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

    variables_.to_csv("test_.csv", index=False)

    return variables_
