-- ESTE ARQUIVO É SOMENTE PARA REFÊRENCIA, USE O init-sql-configmap.yml
-- Cria a base de dados "k8s_app" (se ela não existir)
CREATE DATABASE IF NOT EXISTS k8s_app;

-- Seleciona a base de dados "k8s_app" para ser usada
USE k8s_app;

-- Cria o usuário "k8s_app_user" com a senha "123" (se ele não existir)
CREATE USER IF NOT EXISTS 'k8s_app_user'@'%' IDENTIFIED BY '123';

-- Concede todas as permissões na base de dados "k8s_app" para o usuário "k8s_app_user"
GRANT ALL PRIVILEGES ON k8s_app.* TO 'k8s_app_user'@'%';

-- Cria a tabela "train_history" (se ela não existir) com as colunas especificadas
CREATE TABLE IF NOT EXISTS train_history (
    # Cria a coluna "train_history_id" como chave primária e auto-incremento
    train_history_id INT AUTO_INCREMENT PRIMARY KEY,
    # Cria a coluna "timestamp" como data e hora atual
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    # Cria a coluna "hidden_layer_sizes" como um inteiro pequeno
    hidden_layer_sizes SMALLINT,
    # Cria a coluna "score" como um número de ponto flutuante com 3 dígitos totais e 2 casas decimais
    score FLOAT(3, 2)
);
