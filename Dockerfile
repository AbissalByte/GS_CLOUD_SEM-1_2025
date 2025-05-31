# Imagem base - Python 3.11 (pequena e segura)
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo do script para dentro do container
COPY check_password.py .

# Instala dependências (no caso, apenas 'requests')
RUN pip install --no-cache-dir requests

# Executa o script ao iniciar o container
CMD ["python", "check_password.py"]