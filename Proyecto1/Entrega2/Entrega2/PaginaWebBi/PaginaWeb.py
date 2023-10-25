from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap
from joblib import load
import pandas as pd

app = Flask(__name__, static_folder='/static/TratamientoTotalPd.joblib')

Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aplicar_pipeline', methods=['POST'])
def procesar_archivo():

    # Cargar el modelo y realizar predicciones
    filename = "./static/TratamientoTotalPd.joblib"
    pipeline_loaded = load(filename)
    
    new_data = pd.read_excel(request.files['archivo'])
    df_transformado = pipeline_loaded.named_steps['transformacionesPd'].transform(new_data)
    
    X_tfidf = pipeline_loaded.named_steps['tfidf'].transform(df_transformado["Textos_espanol"])
    predicciones = pipeline_loaded.named_steps['svm_model'].predict(X_tfidf)
    
    df_transformado['sdg'] = predicciones
    
    # Guardar el resultado en un archivo CSV

    df_transformado.to_csv('./data/prueba.csv', index=False)
    
    return jsonify({'mensaje': 'Proceso completado'})

if __name__ == '__main__':
    app.run(debug=True)
