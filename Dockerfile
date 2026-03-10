# Use uma imagem Python oficial
FROM python:3.11-slim

# Instala dependências do sistema para o OpenCV e o motor WeChat
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia os requisitos e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Comando para rodar o Uvicorn (Render espera a porta 10000 por padrão ou via env PORT)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]