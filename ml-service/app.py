import os
import requests
from flask import Flask
from model import train_model

# Criação da aplicação Flask
app = Flask(__name__)


@app.route("/")
def index():
    """Retorna uma mensagem de boas-vindas."""
    return "Aplicação para exemplificar o uso Docker and K8s"


@app.route("/train")
def train():
    """Treina o modelo e insere o histórico de treinamento na base de dados."""
    # Treina o modelo
    hidden_layer_sizes, score = train_model()

    # Insere o histórico de treinamento na base de dados
    url = os.environ.get("DB_SERVICE_URL") + "/train_history"
    data = {
        "hidden_layer_sizes": hidden_layer_sizes,
        "model_score": score
    }
    response = requests.post(url, json=data)

    return {
        "training": {
            "hidden_layer_sizes": hidden_layer_sizes,
            "model_score": score
        },
        "db_response": response.status_code
    }
