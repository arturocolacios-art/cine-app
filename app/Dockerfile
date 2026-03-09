# 1. Imagen base
FROM python:3.9-slim

# 2. Configuración corregida (con "=")
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo
WORKDIR /app

# 4. Instalamos herramientas de compilación (necesarias para bcrypt y mysql)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Instalamos dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copiamos el código
COPY . .

# 7. Puerto y arranque
EXPOSE 5000
CMD ["python", "app.py"]