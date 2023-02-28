import os
from mysql.connector import pooling


class Database:
    """Classe que representa a conexão com o banco de dados."""

    _instance = None

    def __new__(cls, pool_size=10):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.conn_pool = cls._get_mysql_connection_pool(
                pool_size
            )
        return cls._instance

    def check_db_connection(self):
        """
        Verifica se a conexão com o banco de dados está funcionando.

        Retorna:
            bool: True se a conexão está funcionando, False caso contrário.
        """
        try:
            cnx = self.conn_pool.get_connection()
            cnx.close()
            return True
        except Exception:
            return False

    def insert_train_history(
        self, hidden_layer_sizes, learning_rate, alpha, score
    ):
        """
        Insere dados na tabela train_history.

        Args:
            hidden_layer_sizes (str): Tamanho da camada oculta.
            learning_rate (float): Taxa de aprendizado.
            alpha (float): Valor de regularização L2.
            score (float): Score do modelo.
        """
        # Obtém uma conexão da piscina de conexões
        cnx = self.conn_pool.get_connection()
        cursor = cnx.cursor()

        # Gera a consulta SQL
        query = """
            INSERT INTO train_history 
               (hidden_layer_sizes, learning_rate, alpha, score)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            query, (hidden_layer_sizes, learning_rate, alpha, score)
        )
        cnx.commit()

        # Fecha o cursor e a conexão
        cursor.close()
        cnx.close()

    def select_top_50_train_history(self):
        """
        Seleciona os 50 registros da tabela especificada com melhor score.

        Returns:
            list: Lista com os registros retornados.
        """
        # Obtém uma conexão da piscina de conexões
        cnx = self.conn_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)

        # Gera a consulta SQL
        query = """
            SELECT 
               train_history_id, timestamp, hidden_layer_sizes, 
               learning_rate, alpha, score
            FROM train_history
            ORDER BY score
            DESC LIMIT 50
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Fecha o cursor e a conexão
        cursor.close()
        cnx.close()

        return results

    @staticmethod
    def _get_mysql_connection_pool(pool_size):
        """
        Esta função retorna um pool de conexões com o banco de dados MySQL.
        Os parâmetros de conexão são obtidos através das variáveis de ambiente.
        O tamanho do pool é passado como parâmetro.

        Args:
            pool_size: tamanho do pool de conexões.
        Returns:
            Pool de conexões com o banco de dados.
        """
        host = os.environ.get("MYSQL_HOST")
        user = os.environ.get("MYSQL_USER")
        password = os.environ.get("MYSQL_PASSWORD")
        database = os.environ.get("MYSQL_DB")

        return pooling.MySQLConnectionPool(
            pool_name="mysql_pool",
            user=user,
            password=password,
            host=host,
            database=database,
            pool_size=pool_size,
        )
