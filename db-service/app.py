import json

from database import Database
from flask import Flask, request

# Cria a instância Flask
app = Flask(__name__)

# Cria a instância do Database
db = Database()


@app.route("/health")
def health():
    """
    Rota para checar o status da conexão com o banco de dados.

    Returns:
        dict: Dicionário com o status da conexão.
        int: Código HTTP 200 se a conexão estiver funcionando, caso contrário 500.
    """
    status = db.check_db_connection()
    return {
        "db-service": "OK",
        "db-connection": ("UP" if status else "DOWN")
    }, 200 if status else 500


@app.route("/train_history", methods=["POST"])
def insert_train_history():
    """Rota para inserir dados na tabela train_history.

    A rota espera receber uma requisição POST com os seguintes dados no corpo da requisição:
        {
            "hidden_layer_sizes": <int>,
            "model_score": <float>
        }

    Onde:
        hidden_layer_sizes: representa o tamanho da camada oculta.
        model_score: representa o score do modelo.

    A rota retorna uma mensagem de sucesso em caso de inserção bem sucedida.
    """
    # Obtém os dados enviados na requisição
    hidden_layer_sizes = request.json.get("hidden_layer_sizes")
    score = request.json.get("model_score")

    # Insere os dados na tabela
    db.insert_train_history(hidden_layer_sizes, score)

    # Retorna uma resposta de sucesso
    return "Dados inseridos com sucesso", 200


@app.route("/train_history", methods=["GET"])
def select_train_history():
    """Rota para selecionar os 50 registros mais recentes da tabela train_history.

    A rota retorna os dados selecionados no formato JSON.
    """
    # Seleciona os dados da tabela
    results = db.select_top_50_train_history()

    # Retorna os dados selecionados
    return json.dumps(results, default=str), 200
