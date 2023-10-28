from typing import Optional

from fastapi import FastAPI
from joblib import load
import pandas as pd

from clases.Datamodel import DataModel
from clases.transformaciones import TransformacionesPD
from clases.PrediccionesModel import Model

import logging

from typing import List

logger = logging.getLogger("my_logger")

app = FastAPI()


@app.get("/")
def read_root():
   return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
   return {"item_id": item_id, "q": q}

@app.post("/predict")

def make_predictions(dataList: List[DataModel]):
    
   data_dict_list = [{"Textos_espanol": data.Textos_espanol} for data in dataList]

   df = pd.DataFrame(data_dict_list)

   transformacionesPD = TransformacionesPD()

   model = Model()

   df_transformado = transformacionesPD.transform(df)

   return model.make_predictions(df_transformado).to_dict(orient='records')
