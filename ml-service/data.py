from random import uniform

import pandas as pd
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split


def load_wine_data_as_frame():
    data_wine = load_wine(as_frame=True)
    return data_wine.frame

def load_wine_data():
    """
    Função para carregar o conjunto de dados Wine para treinar o modelo.

    Returns:
        Quatro objetos que representam os dados de treinamento e teste.

    """
    # Carrega o conjunto de dados de câncer de mama.
    data_wine = load_wine()
    X, y = data_wine.data, data_wine.target

    # Divide o conjunto de dados em treino e teste com proporção de 80/20.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    return X_train, X_test, y_train, y_test

def create_random_sample_wine(sample_size: int = 1) -> pd.DataFrame:
    """
    Cria uma amostra aleatória de um DataFrame que contém valores dentro 
    do intervalo de valores máximo e mínimo de cada coluna.

    Args:
        dados: DataFrame com os dados originais.
        sample_size: Tamanho da amostra. O valor padrão é 1.

    Returns:
        Um novo DataFrame contendo a amostra aleatória.
    """
    data = load_wine_data_as_frame()
    columns = list(set(data.columns) - set(["target"]))
    sample_data = pd.DataFrame(columns=columns)
    for col in columns:
        # Seleciona o valor mínimo e máximo da coluna
        col_min, col_max = data[col].min(), data[col].max()
        # Cria uma lista com valores aleatórios dentro do intervalo da coluna
        col_sample = [uniform(col_min, col_max) for _ in range(sample_size)]
        # Adiciona a coluna amostrada ao DataFrame
        sample_data[col] = col_sample
    return sample_data