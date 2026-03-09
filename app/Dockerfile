# 1. Usamos una imagen ligera de Python
FROM python:3.9-slim

# 2. Corregimos el formato de ENV para quitar los warnings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo
WORKDIR /app

# 4. INSTALAMOS LAS HERRAMIENTAS DE "COCINA" (Esto soluciona el Exit Code 1)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Instalamos las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copiamos tu código
COPY . .

# 7. Exponemos el puerto y arrancamos
EXPOSE 5000
CMD ["python", "app.py"]