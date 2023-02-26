import os
import pandas as pd
from data import load_wine_data_as_frame, create_random_sample_wine
import requests
from flask import Flask, jsonify, request
from model import train_and_save_model, load_and_predict

# Criação da aplicação Flask
app = Flask(__name__)

# Define a URL do serviço de banco de dados
DB_SERVICE_URL = os.environ.get("DB_SERVICE_URL") + "/train_history"

@app.route("/health")
def health():
    """Endpoint para verificar a saúde do serviço."""
    return {"ml-service": "OK"}

@app.route('/data', methods=['GET'])
def data():
    """Endpoint para obter os dados de treinamento do modelo."""
    # Create a Pandas DataFrame
    df_data = load_wine_data_as_frame()

    # Convert the DataFrame to a dictionary
    dict_data = df_data.to_dict()

    # Return the dictionary as a JSON response
    return jsonify(dict_data)

@app.route("/train", methods=["POST"])
def train():
    """Treina o modelo e insere o histórico de treinamento na base de dados."""
    # Treina o modelo
    hidden_layer_sizes, score = train_and_save_model()

    # Insere o histórico de treinamento na base de dados
    data = {
        "hidden_layer_sizes": hidden_layer_sizes,
        "model_score": score
    }
    response = requests.post(DB_SERVICE_URL, json=data)

    return {
        "training": {
            "hidden_layer_sizes": hidden_layer_sizes,
            "model_score": score
        },
        "db_response": response.status_code
    }

@app.route("/sample", methods=["GET"])
def get_sample():
    """Endpoint para obter uma amostra aleatória dos dados de treinamento."""
    sample = create_random_sample_wine()
    
    # Convert the DataFrame to a dictionary
    dict_sample = sample.to_dict()

    # Return the dictionary as a JSON response
    return jsonify(dict_sample)


@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint para fazer a predição com base nos dados recebidos via requisição POST."""
    # Get the JSON payload from the request
    payload = request.get_json()

    # Convert the payload to a Pandas DataFrame
    df = pd.DataFrame.from_dict(payload)

    # Load the trained model and make predictions
    y_pred = load_and_predict(df)

    # Return the predictions as a JSON response
    return jsonify({'predictions': y_pred})
