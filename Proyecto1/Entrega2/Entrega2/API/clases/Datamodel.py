from pydantic import BaseModel

'''
   En este archivo se realiza el modelo de los datos de entrada a la peticion de los API. 
   Para este caso se realiza aesta clas epara la estandarizacion de los datos a lo largo de las peticiones Post, 
   que se vana realizar a lo largo del programa. Y de esta manera aseguraar que todos los JSON, cumplan con el formato, 
   y mnejarlos mas facilmente dentor del API
   
   '''

class DataModel(BaseModel):

    #En este punto se definene las variables que hacen parte del modelo, es decir, de los 
    #datos del modelo. Para ets epunto no se incluye la variable objetivo porque se entiende qeu esta 
    #en un archivo qeu se busca predecir va a estar incompleta. Por lo que no se incluye

    Textos_espanol: str

    #Luego, aqui se definen las columnas para crear los datos modelo en este programa, que vana  resultar siendo las mismas de arriba.

    def columns(self):
        return ["Textos_espanol"]
