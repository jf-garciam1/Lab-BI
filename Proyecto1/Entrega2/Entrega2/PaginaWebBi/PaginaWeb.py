from flask import Flask, render_template, request, send_file
import requests
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if file:

        df = pd.read_excel(file)

        df = df.drop(['sdg'], axis=1)

        response = requests.post('http://127.0.0.1:8000/predict', json=df.to_dict(orient='records'))

        df1 = pd.DataFrame(response.json())

        df1 = df1.drop(['Textos_Tokenizados'], axis=1)

        data_dir = os.path.join(os.getcwd(), './Proyecto1/Entrega2/Entrega2/PaginaWebBi/data')

        nombre_archivo = 'resultado.csv'

        resultado_path = os.path.join(data_dir, nombre_archivo)

        df1.to_csv(resultado_path, index=False)

        send_file(resultado_path, as_attachment=True)

        return render_template('results.html', predictions=response.json())
    
@app.route('/download_resultado')
def download_resultado():
    return send_file('./data/resultado.csv', as_attachment=True)

if __name__ == '__main__':
   app.run(debug=True)

