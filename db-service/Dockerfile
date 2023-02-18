# Define a imagem base para o nosso container
FROM python:3.8-slim-buster

# Define uma variável de ambiente para garantir que
# o Python não escreva arquivos bytecode
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho do nosso aplicativo
# dentro do container
WORKDIR /usr/src/app

# Copia o arquivo requirements.txt para o diretório 
# de trabalho
COPY ./requirements.txt .

# Instala as dependências do nosso aplicativo a
# partir do arquivo requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia o restante dos arquivos do nosso aplicativo 
# para o diretório de trabalho
COPY . .

# Cria um usuário para executar o nosso aplicativo
RUN useradd --create-home --shell /bin/bash appuser

# Define o usuário padrão para executar o aplicativo 
# dentro do container
USER appuser

# Define o comando para iniciar o aplicativo
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
