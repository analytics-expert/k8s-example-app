import os
import pandas as pd

import requests
from flask import Flask, render_template, jsonify, flash

app = Flask(__name__)

# Define a URL do serviço de ML e banco de dados 
ML_SERVICE_URL = os.environ.get("ML_SERVICE_URL")
DB_SERVICE_URL = os.environ.get("DB_SERVICE_URL")

@app.route("/")
def data():
    """
    Função index para exibir a página principal
    """
    # Renderiza a página HTML principal
    return render_template("index.html")

@app.route("/data")
def show_data():
    """
    Endpoint que retorna a tabela com os dados de treinamento.
    """
    try:
        # Faz uma requisição GET para o endpoint data do serviço de ML
        response = requests.get(f"{ML_SERVICE_URL}/data")
        data = pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        # Se ocorrer um erro na requisição, exibe uma mensagem de erro 
        # para o usuário
        flash(
            "Erro ao obter os dados. Verifique o ml-service", "error"
        )
        data = []
    # Renderiza a página HTML com os dados de treinamento
    return render_template("data.html", data=data.to_dict('records'))

@app.route("/train-history")
def train_history():
    """
    Endpoint que retorna o historico de treinamento.
    """
    try:
        # Faz uma requisição GET para o endpoint train_history do serviço
        # de banco de dados
        response = requests.get(f"{DB_SERVICE_URL}/train_history")
        train_history = response.json()
    except requests.exceptions.RequestException as e:
        # Se ocorrer um erro na requisição, exibe uma mensagem de erro para o usuário
        flash(
            "Erro ao obter o histórico de treinamento. Verifique o db-service", "error"
        )
        train_history = []
    # Renderiza a página HTML com os dados do histórico de treinamento
    return render_template("train.html", train_history=train_history)

@app.route("/train-model", methods=["POST"])
def train():
    """
    Endpoint para realizar um novo treinamento do modelo.
    """
    try:
        # Chama a outra API para treinar o modelo
        response = requests.post(f"{ML_SERVICE_URL}/train")
    except Exception as e:
        return jsonify(str(e))
    # Verifica se a resposta foi bem sucedida e retorna o resultado
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": response.text}), response.status_code

@app.route("/predict", methods=["GET"])
def predict():
    """
    Endpoint responsável por fazer uma previsão com base no modelo treinado.
    """
    try:
        # Faz a requisição para o serviço de ML
        response = requests.post(f"{ML_SERVICE_URL}/predict")
        data = response.json()
    except requests.exceptions.RequestException as e:
        # Se ocorrer um erro na requisição, exibe uma mensagem de erro para o usuário
        flash(
            "Erro ao realizar o predict. Verifique o ml-service", "error"
        )
        data = []
    # Renderiza a página HTML com os dados do histórico de treinamento
    return render_template("predict.html", data=data["samples"])


@app.route("/load_predict_template", methods=["GET"])
def load_predict_template():
    # Renderiza a página HTML do predict
    return render_template("predict.html", data=[])

if __name__ == "__main__":
    app.run()
