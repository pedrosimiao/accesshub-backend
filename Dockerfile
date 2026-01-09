# Imagem Base
FROM python:3.12-slim

# Variáveis de Ambiente de Otimização
# PYTHONDONTWRITEBYTECODE=1: impede criacao de arquivos .pyc (lixo em containers)
# PYTHONUNBUFFERED=1: logs (print) no painel
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de Trabalho
# Cria uma pasta /app dentro do Linux do container e entra nela
WORKDIR /app

# Dependências de Sistema
# driver do Postgres (psycopg2) precisa de compiladores C (gcc) e bibliotecas (libpq-dev)
# para ser instalado.
# 'rm -rf...' limpa o cache do apt para deixar a imagem leve
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalação do Poetry
RUN pip install poetry

# Configuração do Poetry
# não configurar ambiente virtual (.venv),
# container é o ambiente isolado.
RUN poetry config virtualenvs.create false

# Estratégia de Cache (Camadas)
# copia arquivos de dependência primeiro.
# Em CI/CD, pular a instalação e usar o cache.
COPY pyproject.toml poetry.lock ./

# Instalação das Libs
RUN poetry install --no-interaction --no-ansi --only main

# Copia o Código Fonte todo o resto do projeto para dentro da pasta /app
COPY . .

# Coleta de Estáticos (Whitenoise)
# coletar CSS do Admin , mover pasta 'staticfiles'
# Whitenoise lê pasta e serve o CSS em produção
RUN python manage.py collectstatic --noinput

# container escuta na porta 8000.
EXPOSE 8000

# Script de Entrada
# copia o entrypoint (gerenciamento do startup e permissão de execução)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# rodar entrypoint.sh ao iniciar
ENTRYPOINT ["/entrypoint.sh"]