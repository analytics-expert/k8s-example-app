from random import uniform

import pandas as pd
import numpy as np
from sklearn.datasets import load_wine
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_wine_data_as_frame():
    """
    Função para carregar o conjunto de dados Wine para treinar o 
    modelo como um Pandas DataFrame.

    Returns:
        Pandas DataFrame: Conjunto de dados de treinamento e teste.
    """
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

    # Padroniza os dados
    scaler = StandardScaler().fit(X)
    X = scaler.transform(X)

    # Divide o conjunto de dados em treino e teste com proporção de 80/20.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test

def create_random_sample_wine(sample_size: int = 9) -> pd.DataFrame:
    """
    Cria uma amostra aleatória de Wine que contém valores dentro
    do intervalo de valores máximo e mínimo de cada coluna do dado real.

    Args:
        sample_size: Tamanho da amostra. O valor padrão é 9.

    Returns:
        Um novo DataFrame contendo a amostra aleatória.
    """
    # Carrega o dataset Wine
    wine_data = load_wine()

    # Extrai os dados e os rótulos do dataset
    X, y = wine_data.data, wine_data.target
    
    # Padroniza os dados
    scaler = StandardScaler().fit(X)
    X = scaler.transform(X)

    # Cria uma lista com as classes de target
    target_classes = list(set(y))

    # Verifica se sample_size é um múltiplo de 3
    if sample_size % 3 != 0:
        raise ValueError("O tamanho da amostra deve ser um múltiplo de 3.")

    # Cria uma lista vazia para armazenar a amostra
    sample_data = []

    # Para cada classe em target_classes, gera uma amostra com base no mínimo
    # e máximo de cada coluna
    for cls in target_classes:
        # Seleciona apenas as linhas correspondentes à classe atual
        class_data = X[y == cls]
        # Gera uma amostra aleatória da classe atual
        class_sample = resample(class_data, n_samples=sample_size // 3,
                                replace=True, random_state=42)
        # Adiciona a amostra da classe atual à lista de amostras
        sample_data.append(class_sample)

    # Concatena as amostras de cada classe em um único DataFrame
    sample_data = pd.DataFrame(np.concatenate(sample_data)).sample(frac=1)
    sample_data.columns = wine_data.feature_names

    return sample_data
