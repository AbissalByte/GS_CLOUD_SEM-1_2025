# Usa uma imagem leve com Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos para dentro da imagem
COPY requirements.txt .
COPY main.py .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Define o comando padrão ao rodar o container
CMD ["python", "main.py"]
