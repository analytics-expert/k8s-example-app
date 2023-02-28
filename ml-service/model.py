import logging
import os
from random import randint, uniform

import joblib
import yaml
from data import create_random_sample_wine, load_wine_data
from sklearn.neural_network import MLPClassifier

MODEL_FILENAME = "models/wine_model.pkl"
SCORE_FILENAME = "models/wine_model_score.yaml"


def train_and_save_model():
    """
    Função para treinar o modelo de rede neural utilizando o MLPClassifier do
    sklearn, salvar o modelo e o score em arquivos.

    Returns:
        Número de neurônios na camada oculta e a acurácia do modelo.
    """
    # Gera uma quantidade aleatória de neurônios na camada oculta do modelo.
    hidden_layer_sizes = randint(20, 50)
    # Gera um valor aleatório para a taxa de aprendizado.
    learning_rate = uniform(0.0001, 0.0005)
    # Gera um valor aleatório para o parâmetro de regularização L2.
    alpha = uniform(0.00005, 0.005)

    # Gera os dados de treino e teste.
    X_train, X_test, y_train, y_test = load_wine_data()

    # Instancia o modelo MLPClassifier.
    clf = MLPClassifier(
        hidden_layer_sizes=hidden_layer_sizes,
        learning_rate_init=learning_rate,
        alpha=alpha,
        max_iter=150,
        random_state=42
    )

    # Treina o modelo com o conjunto de dados de treino.
    clf = clf.fit(X_train, y_train)

    # Calcula a acurácia do modelo utilizando os dados de teste.
    model_score = clf.score(X_test, y_test)

    # Salva o modelo caso ele seja melhor que o modelo atual ou caso não haja
    # modelo salvo.
    _save_model(clf, model_score)

    return hidden_layer_sizes, learning_rate, alpha, model_score


def load_and_predict(X):
    """
    Carrega um modelo de classificação treinado e realiza a predição dos dados fornecidos.

    Args:
        X (array-like): Dados a serem classificados.

    Returns:
        Array com as predições do modelo.
    """
    # Verifica se o arquivo do modelo existe e, caso não exista, retorna [-1]
    if not os.path.isfile(MODEL_FILENAME):
        return len(X)*[-1]

    # Carrega o modelo salvo em disco
    clf = joblib.load(MODEL_FILENAME)

    # Realiza a predição dos dados fornecidos
    y_pred = clf.predict(X.to_numpy())

    return y_pred.tolist()


def _save_model(clf, model_score):
    """
    Função salvar o modelo treinado caso ele tenho um score maior do que o atual

    Args:
        clf: objeto classificador treinado
        model_score: pontuação do modelo

    Returns:
        Score do modelo atual.
    """
    # Verifica se o arquivo do modelo já existe ou se o score do modelo atual é melhor que o modelo já salvo
    if not os.path.isfile(MODEL_FILENAME) or model_score > _get_current_model_score(SCORE_FILENAME):
        # Registra mensagem de log informando que o modelo está sendo salvo
        logging.warning(f"Salvando modelo com score {model_score}")
        # Salva o modelo em um arquivo pickle
        joblib.dump(clf, MODEL_FILENAME)
        # Salva o score do modelo em um arquivo YAML
        _save_model_score(SCORE_FILENAME, model_score)


def _get_current_model_score(score_filename):
    """
    Função para obter o score do modelo atual.

    Args:
        score_filename: Nome do arquivo YAML que contém o score do modelo.

    Returns:
        Score do modelo atual.
    """
    try:
        with open(score_filename, "r") as f:
            scores = yaml.load(f, Loader=yaml.FullLoader)
            current_score = scores["wine_model_score"]
    except (FileNotFoundError, yaml.YAMLError, KeyError):
        current_score = 0
        raise
    return current_score


def _save_model_score(score_filename, model_score):
    """
    Função para salvar o score do modelo em um arquivo YAML.

    Args:
        score_filename: Nome do arquivo YAML para salvar o score do modelo.
        model_score: Score do modelo a ser salvo.
    """
    try:
        with open(score_filename, "w") as f:
            scores = {"wine_model_score": float(model_score)}
            yaml.dump(scores, f)
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    print(train_and_save_model())
    sample = create_random_sample_wine()
    print(load_and_predict(sample))
