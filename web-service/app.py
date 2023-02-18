import os
from flask import Flask, render_template, redirect, url_for
import requests
import logging

app = Flask(__name__)

@app.route('/')
def index():
    """
    Função index para exibir a página principal
    """
    DB_SERVICE_URL = os.environ.get('DB_SERVICE_URL')

    # Faz uma requisição GET para o endpoint train_history do serviço de banco de dados
    response = requests.get(f'{DB_SERVICE_URL}/train_history')
    train_history = response.json()

    # Renderiza a página HTML com os dados da história de treinamento
    return render_template('index.html', train_history=train_history)

@app.route('/refresh')
def refresh():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
