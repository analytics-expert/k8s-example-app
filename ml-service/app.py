import os

import pandas as pd
import requests
from data import create_random_sample_wine, load_wine_data_as_frame
from flask import Flask, jsonify, request
from model import load_and_predict, train_and_save_model

# Criação da aplicação Flask
app = Flask(__name__)

# Define a URL do serviço de banco de dados
DB_SERVICE_URL = os.environ.get("DB_SERVICE_URL") + "/train_history"


@app.route("/health")
def health():
    """Endpoint para verificar a saúde do serviço."""
    return {"ml-service": "OK"}


@app.route("/data", methods=["GET"])
def data():
    """Endpoint para obter os dados de treinamento do modelo."""
    # Carrega os dados
    df_data = load_wine_data_as_frame()

    # Converte DataFrame para dictionary
    dict_data = df_data.to_dict('records')

    # Retorna o dict como um JSON.
    return jsonify(dict_data)

@app.route("/sample", methods=["GET"])
def get_sample():
    """Endpoint para gerar uma amostra aleatória baseado na estatistica 
    do conjunto de treinamento."""
    # Gera uma amostra aleatória
    sample = create_random_sample_wine()

    # Converte DataFrame para dictionary
    dict_sample = sample.to_dict()

    # Retorna o dict como um JSON.
    return jsonify(dict_sample)


@app.route("/train", methods=["POST"])
def train():
    """Treina o modelo e insere o histórico de treinamento na base de dados."""
    # Treina o modelo
    hidden_layer_sizes, learning_rate, alpha, score = train_and_save_model()

    # Insere o histórico de treinamento na base de dados
    data = {
        "hidden_layer_sizes": hidden_layer_sizes,
        "learning_rate": round(learning_rate, 5),
        "alpha": round(alpha, 5),
        "model_score": round(score, 5)
    }
    try:
        response = requests.post(DB_SERVICE_URL, json=data)
        db_response =  str(response.status_code)
    except:
        db_response = 'FAIL'

    return {
        "training": data,
        "db_response": db_response
    }

@app.route("/predict", methods=["POST"])
def predict():
    """Endpoint para fazer a predição com base nos dados recebidos via 
    requisição POST."""
    if request.is_json:
        # Obtém os dados enviados na requisição
        payload = request.get_json()

        # Converte para Data Frame
        df = pd.DataFrame.from_dict(payload)
    else:
        # Gera uma amostra aleatória
        df = create_random_sample_wine()

    # Carrega o modelo treinado e faz as predições.
    y_pred = load_and_predict(df)
    df["predict"] = y_pred

    # Retorna o dict como um JSON.
    return jsonify({"samples" : df.round(5).to_dict('records'), "predictions": y_pred})
