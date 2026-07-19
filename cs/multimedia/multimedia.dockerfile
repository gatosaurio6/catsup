# Usa una imagen base ligera
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y almacene en buffer la salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para psycopg2 (base de datos)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente
COPY . .

# Exponemos el puerto donde correrá Gunicorn
EXPOSE 8000

# Comando para ejecutar la app en producción con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "multimedia.wsgi:application"]