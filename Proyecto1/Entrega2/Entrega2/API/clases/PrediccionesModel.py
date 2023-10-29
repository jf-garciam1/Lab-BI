from joblib import load

'''
   En este archivo se realiza el modelo para lograr traer o importar la pipline con su archivo joblib, 
   y ejecutarla sobre un conjunto de datos. Para este caso, se va arealizar, para lograr tener un menor 
   acoplamiento dentro del modelo del proyecto.
   
   '''

class Model:

    '''
   Este constructor, define que apenas se inicialize una isntacnia de esta cale. Lo que se va a hacer es realziar la cargar del archivo joblib
   que contiene la piplien, es decir, lo modelos a ejecutar.
   
   '''

    def __init__(self):
        self.model = load("assets/tratamientoD.joblib")

    '''
   Lueog, el metodo make_predictions, se basa en usar es emodelo esa pipline que se cargo antes, dle archivo joblib, y ejecutar cada paso. 
   En un primer momento se realiza la ejecucion del modelo TD-IDDF. con el metodo trasnform sobre los datos. Luego, se realiza la ejecucion dle modelo
   SVM, con el metodo predict, sobre los datos. Lo que nos resulta en la definicion en los datos de la columna de la variable objetivo
   que en este caso son los objetivos de desarollo sostenible.
   
   '''

    def make_predictions(self, data):
        X_tfidf = self.model.named_steps['tfidf'].transform(data["Textos_espanol"])

        data['sdg']  = self.model.named_steps['svm_model'].predict(X_tfidf)

        return data
