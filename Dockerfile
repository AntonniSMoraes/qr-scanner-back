# Use uma imagem Python oficial (slim para manter o deploy leve no Render)
FROM python:3.11-slim

# Instala dependências do sistema atualizadas para o OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglx0 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN mkdir -p temp_images && chmod 777 temp_images
# O restante do seu Dockerfile continua igual...
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
