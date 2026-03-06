# Usa uma imagem oficial do Python
FROM python:3.10-slim

# Instala as dependências do sistema para o OpenCV e PyMuPDF
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Define a pasta de trabalho
WORKDIR /app

# Copia os arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Comando para rodar a API (o Render vai ler a variável $PORT)
CMD uvicorn main:app --host 0.0.0.0 --port $PORT