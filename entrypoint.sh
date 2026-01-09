#!/bin/sh

# 'set -e' faz o script parar se qualquer comando der erro.
# evitar subir o servidor se as migrations falharem
set -e

echo "Iniciando processo de deploy..."

# roda as migrations automaticamente a cada deploy.
echo "Aplicando migrations no Banco de Dados..."
python manage.py migrate --noinput

echo "Iniciando servidor Gunicorn..."
# inicia servidor web de produção
# bind 0.0.0.0:8000 -> acesso ao container.
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000