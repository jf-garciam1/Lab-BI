from flask import Flask, render_template, jsonify, request, send_file
from flask_bootstrap import Bootstrap
from joblib import load
import pandas as pd
import os

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aplicar_pipeline', methods=['POST'])
def procesar_archivo():

    filename = os.path.join(os.getcwd(), 'TratamientoTotalPd.joblib')

    pipeline_loaded = load(filename)
    
    new_data = pd.read_excel(request.files['csvFile'])
    df_transformado = pipeline_loaded.named_steps['transformacionesPd'].transform(new_data)
    
    X_tfidf = pipeline_loaded.named_steps['tfidf'].transform(df_transformado["Textos_espanol"])
    predicciones = pipeline_loaded.named_steps['svm_model'].predict(X_tfidf)
    
    df_transformado['sdg'] = predicciones
    
    # Guardar el resultado en un archivo CSV
    output_path = './data/prueba.csv'
    df_transformado.to_csv(output_path, index=False)
    
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

