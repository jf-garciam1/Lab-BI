from typing import Optional

from fastapi import FastAPI
from joblib import load
import pandas as pd

from clases.Datamodel import DataModel
from clases.transformaciones import TransformacionesPD
from clases.PrediccionesModel import Model

import logging

from typing import List

'''
En archivo se esta realizando la creacion del API. Para este caso se esta desarrollando el API en fastapi.
Aqui se vana realziar las peticiones, qeu nso van a permitir manejar los datos y realizar su debido 
procesamiento y su debida prediccion de resultados
'''

#Para este caso se esta creando la aplciacion se esta inicializando un objeto de calse fastapi.

app = FastAPI()

#Luego, en este caso, se esta realizano la creacion de una, ventan se podria decir, de una ventana o un espacion para recepcion de peticion post

@app.post("/predict")

#Luego, aqui se crea la funcion que se va aejecutarr cuando se haga un lñlamado a esta url

def make_predictions(dataList: List[DataModel]):

   '''
   Antes de explicar el cuerpo de la funcion, es necsario  explicar sus entradas
   En este caso, esta funcion recib ecomo entrada una lista de objetos, llamdos Datamodel.
   Los objetos dataModel, surgen d ela calse qeu se encuentra en este mismo proyecto llamada de la msima manera. Dentro de esta clase
   se guardan la forma que dberian tener los JSOn, que entran como parametro para poder luego transformarlos mas facilmente
   Es un modod de mantener un estandarizacion de los datos y qeu no halla nigun como dato mal planteado.
   Luego, aqui se esta desarrollando un lista de dicionarios, los caules cad diccionario pertence a un JSOn, 
   que viene como entrada a la peticion post
   Cabe aclarar que al ser tantos datos, no solo se recib eun JSON, sino que se va arecibir una lista de JSON o mas bien, una lista
   de los objetos dataModel, que lleva un formato conocido estos JSON.
   
   '''
   data_dict_list = [{"Textos_espanol": data.Textos_espanol} for data in dataList]

   #Luego, aqui se convietre esta lista deccionarios en un dataframe, para aplicar los pasos conocidos.

   df = pd.DataFrame(data_dict_list)

   #Creamos una isntancia de la calse qeu contiene el metodo para poder desarrollar todas las transfdormacion, mencionadas, en el notebookbase

   transformacionesPD = TransformacionesPD()

   #Creamos una instancia de la clase que contiene el metodo para poder desarrollar todas las predicciones, cargar la pipeline o el archivo joblib que la contiene
   #Ademas, de cargar la pipeline tien una funcion qeu recib elos datos como entrada, ejecuta los modelos, y devuelve las predicciones realizadas.

   model = Model()

   #Aqui se realizna las transformaciones sobre los datos recibidos en la peticion.

   df_transformado = transformacionesPD.transform(df)

   #Aqui se realizan las predicciones, es decir, la ejecucion de los modelos sobre los datos trasnformaddos, se pasan a diccionario, y se devulven a manera de JSON, como respuesta a la peticion

   return model.make_predictions(df_transformado).to_dict(orient='records')
