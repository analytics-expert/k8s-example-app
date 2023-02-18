import os
import mysql.connector
from mysql.connector import pooling

class Database:
    """Classe que representa a conexão com o banco de dados."""
    
    def __init__(self, pool_size=10):
        """Inicializa a classe com os parâmetros de conexão com o banco de dados."""
        self.pool = _get_mysql_connection_pool(pool_size)

    def insert_train_history(self, hidden_layer_sizes, score):
        """Insere dados na tabela especificada."""
        # Obtém uma conexão da piscina de conexões
        cnx = self.pool.get_connection()
        cursor = cnx.cursor()

        # Gera a consulta SQL
        query = "INSERT INTO train_history (hidden_layer_sizes, score) VALUES (%s, %s)"
        cursor.execute(query, (hidden_layer_sizes, score))
        cnx.commit()

        # Fecha o cursor e a conexão
        cursor.close()
        cnx.close()

    def select_top_50_train_history(self):
        """Seleciona dados da tabela especificada."""
        # Obtém uma conexão da piscina de conexões
        cnx = self.pool.get_connection()
        cursor = cnx.cursor(dictionary=True)

        # Gera a consulta SQL
        query = f"SELECT train_history_id, timestamp, hidden_layer_sizes, score FROM train_history ORDER BY score DESC LIMIT 50"
        cursor.execute(query)
        results = cursor.fetchall()

        # Fecha o cursor e a conexão
        cursor.close()
        cnx.close()

        return results
    
def _get_mysql_connection_pool(pool_size):
    host = os.environ.get("MYSQL_HOST")
    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    database = os.environ.get("MYSQL_DB")

    return pooling.MySQLConnectionPool(
        pool_name='mysql_pool', user=user, password=password, host=host, database=database, pool_size=pool_size
    )