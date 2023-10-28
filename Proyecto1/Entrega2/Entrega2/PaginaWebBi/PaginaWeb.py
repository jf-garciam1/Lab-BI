from flask import Flask, render_template, request
import requests
import pandas as pd
import io

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

        return render_template('results.html', predictions=response.json())

if __name__ == '__main__':
   app.run(debug=True)

