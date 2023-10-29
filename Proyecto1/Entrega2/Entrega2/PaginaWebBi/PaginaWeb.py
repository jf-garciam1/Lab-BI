from flask import Flask, render_template, request, send_file
import requests
import pandas as pd
import os

#En este punto se inicializa una aplicacion, o una instancia de tipo flask

app = Flask(__name__)

#Luego, creamos la venta principal de la aplicacion, la cual va consumir del archivo index.html. 
#El cual contiene el codigo de la pagina principal

@app.route('/')
def index():
   return render_template('index.html')

'''

Luego, creamos una ventana que se llama upload. La cual va ser la encargada de mandar el archivo qeu cargue el usuario en la pagina
principal, hacia el api, que es se encargue de desarrollar las debidas trasnofrmaciones y predicciones. Y luego, vuelva a qui para
poder desarrollar la impresion y muestra de resultados. Esta paigna va estar encargada de desarrollar las peticiones POST al API, para
mandar los inputs del usuario.

'''

@app.route('/upload', methods=['POST'])
def upload_file():

    '''

    Para este caso, se crea el metoo upload_file,  el cual se va a ejecutar apenas se inicie la ventana upload.
    Eeste metodo, recibe el archivo, y lo manda por medio de una peticion post al API. Luego, recibe el resultado de esta peticion
    y los muestra al usuairo aparte de mostrar otros resultados del analisis.

    '''

    #Aqui se llama al archivo qeu subio el usuario

    file = request.files['file']

    #Luego, si esta se continua con el proceso sino no

    if file:

        #Se convierte el archivo en un dataframe

        df = pd.read_excel(file)

        #Luego, se le quita la columna d ela variable objetivo, que en este punto esta vacia

        df = df.drop(['sdg'], axis=1)

        #Se manda como lista diccionaros, o lista de JSON, en forma de peticion post al API

        response = requests.post('http://127.0.0.1:8000/predict', json=df.to_dict(orient='records'))

        #Se recibe la respuesta y se transforma a dataframe la lista de JSON, en la cual cada JSON es una fila del dataframe
        #que esta vez si incluye ya la varaibl eobjetivo definida.

        df1 = pd.DataFrame(response.json())

        #Se quita una columna que fue creada para el desarrollo de los modelos

        df1 = df1.drop(['Textos_Tokenizados'], axis=1)

        #Se crear o se busca la ruta de un archivo para guardar los resultados, y qeu el usuario los pueda descargar si lo necesita.

        data_dir = os.path.join(os.getcwd(), './Proyecto1/Entrega2/Entrega2/PaginaWebBi/data')

        nombre_archivo = 'resultado.csv'

        resultado_path = os.path.join(data_dir, nombre_archivo)

        #Se pasa a csv, el dataframe, y se guarda en la ruta que se definio antes.

        df1.to_csv(resultado_path, index=False)

        #Se manda el archivo para que el suario lo pueda descargar

        send_file(resultado_path, as_attachment=True)

        #Se imprimen los resultados obtendios de la peticion post, para que el usuario pueda visualizar el analisis, siendo esto
        #por que se consume el archivo results.html

        return render_template('results.html', predictions=response.json())
    
@app.route('/download_resultado')
def download_resultado():

    '''

    Este metodo se crea para que el usuario pueda descargar lso resultados obtenidos

    '''

    return send_file('./data/resultado.csv', as_attachment=True)

if __name__ == '__main__':
   app.run(debug=True)

