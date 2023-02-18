import json
from database import Database
from flask import Flask, request

# Cria a instância Flask
app = Flask(__name__)
db = Database()


@app.route("/train_history", methods=["POST"])
def insert_train_history():
    """Rota para inserir dados na tabela."""
    # Obtém os dados enviados na requisição
    hidden_layer_sizes = request.json.get("hidden_layer_sizes")
    score = request.json.get("model_score")

    # Insere os dados na tabela
    db.insert_train_history(hidden_layer_sizes, score)

    # Retorna uma resposta de sucesso
    return "Dados inseridos com sucesso", 200


@app.route("/train_history", methods=["GET"])
def select_train_history():
    """Rota para selecionar dados da tabela."""
    # Seleciona os dados da tabela
    results = db.select_top_50_train_history()

    # Retorna os dados selecionados
    return json.dumps(results, default=str), 200
