from random import randint
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier


def load_data():
    """
    Função para carregar o conjunto de dados para treinar o modelo.

    Returns:
        Quatro objetos que representam os dados de treinamento e teste.

    """
    # Utilizando a função make_classification para criar um conjunto
    # de dados sintético.
    X, y = make_classification(
        n_samples=1000, n_features=20, n_classes=2, random_state=None
    )
    # Divide o conjunto de dados em treino e teste com proporção de 80/20.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    return X_train, X_test, y_train, y_test


def train_model():
    """
    Função para treinar o modelo de rede neural utilizando o MLPClassifier
    do sklearn.

    Returns:
        Número de neurônios na camada oculta e a acurácia do modelo.
    """
    # Gera uma quantidade aleatória de neurônios na camada oculta do modelo.
    hidden_layer_sizes = randint(50, 150)

    # Gera os dados de treino e teste
    X_train, X_test, y_train, y_test = load_data()

    clf = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, max_iter=500)
    # Treina o modelo com o conjunto de dados de treino
    clf = clf.fit(X_train, y_train)
    # Calcula a acurácia do modelo utilizando os dados de teste.
    model_score = clf.score(X_test, y_test)

    return hidden_layer_sizes, model_score


if __name__ == "__main__":
    print(train_model())
