# 1. Uso una imagen ligera de Python 3.11 para asegurar compatibilidad con librerías modernas
FROM python:3.11-slim

# 2. Configuro las variables de entorno con el formato moderno
# PYTHONDONTWRITEBYTECODE: Evita que Python genere archivos .pyc
# PYTHONUNBUFFERED: Fuerza que los logs se muestren en tiempo real sin búfer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Gestión de dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el código fuente al contenedor
COPY . .

# 6. Exponemos el puerto de comunicación
EXPOSE 5000

# 7. Punto de entrada de la aplicación
CMD ["python", "app.py"]