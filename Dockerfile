# 1. Usamos una imagen ligera de Python
FROM python:3.9-slim

# 2. Evitamos que Python genere archivos .pyc y forzamos que los logs salgan rápido
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalamos las dependencias
# Copiamos primero el requirements para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto del código (incluyendo la carpeta app y templates)
COPY . .

# 6. Exponemos el puerto 5000 (el que usa Flask por defecto)
EXPOSE 5000

# 7. Comando para arrancar la aplicación
# OJO: Verifica que la ruta a app.py sea correcta según tu carpeta
CMD ["python", "app.py"]