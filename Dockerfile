# Usando a imagem estável do Python
FROM python:3.10-slim

# Instala as dependências de sistema atualizadas para Debian Trixie/Bookworm
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Define a pasta de trabalho
WORKDIR /app

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY . .

# Comando para rodar a API (ajustado para a porta do Render)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
