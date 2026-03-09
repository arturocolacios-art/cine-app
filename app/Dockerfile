# 1. Usamos Python (es un Linux pequeñito por dentro)
FROM python:3.9-slim

# 2. Configuración para que no de guerra
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Carpeta de trabajo
WORKDIR /app

# 4. ESTO ES LO IMPORTANTE: Instalamos el "martillo y clavos" para Linux
# Sin esto, las librerías de seguridad fallan al instalarse
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Instalamos tus librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos tu código de Windows al contenedor
COPY . .

# 7. Arrancamos
EXPOSE 5000
CMD ["python", "app.py"]