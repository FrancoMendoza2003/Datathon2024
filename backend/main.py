import fastapi
import pickle

from pydantic import BaseModel
from utils import prepare_variables
import datetime


class Payload(BaseModel):
    Aeronave: str
    DepartureStation: str
    ArrivalStation: str
    Destination_Type: str
    Origin_Type: str
    STD: str
    STA: str
    Capacity: int


app = fastapi.FastAPI()

model_pasajeros = pickle.load(
    open(
        "../prediction/pasajeros/models/xgb_pasajeros_model.pickle",
        "rb",
    )
)


@app.post("/model")
def predict(data: Payload) -> float:

    variables = data.model_dump()

    # fmt: off
    variables["STD"] = [datetime.datetime.strptime(variables["STD"], "%Y-%m-%d %H:%M:%S")]
    variables["STA"] = [datetime.datetime.strptime(variables["STA"], "%Y-%m-%d %H:%M:%S")]
    # fmt: on

    variables_ = prepare_variables(variables)

    print(variables_)
    prediction = model_pasajeros.predict(variables_)

    return prediction
