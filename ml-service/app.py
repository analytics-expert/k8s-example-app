import os
import requests
from flask import Flask
from model import train_model

app = Flask(__name__)

@app.route('/')
def index():
    return "Aplicação para exemplificar o uso Docker and KB8's"

@app.route('/train')
def train():
    hidden_layer_sizes, score = train_model()
    # Insert the training history to the db-service
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