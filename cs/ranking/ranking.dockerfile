# 1. Usamos una imagen oficial de Python ligera
FROM python:3.12-slim

# 2. Evita que Python escriba archivos .pyc en el contenedor
ENV PYTHONDONTWRITEBYTECODE=1
# 3. Asegura que los logs de Python se muestren en tiempo real sin retrasos
ENV PYTHONUNBUFFERED=1

# 4. Creamos y nos situamos en la carpeta de la app dentro del contenedor
WORKDIR /app/ranking

# 5. Instalamos las dependencias del sistema necesarias por si acaso (como compiladores para BD)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 6. Copiamos e instalamos primero las dependencias de Python
# (Hacer esto primero aprovecha la caché de Docker para que las compilaciones sean más rápidas)
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 7. Copiamos todo el código de nuestro microservicio a la carpeta de trabajo
COPY . /app/

# 8. Exponemos el puerto en el que va a correr Django (por defecto el 8000)
EXPOSE 8002

# 9. Comando para arrancar el servidor en producción usando Gunicorn
# (Reemplaza 'proyecto.wsgi' por el nombre de la carpeta de tu proyecto principal donde está el archivo wsgi.py)
CMD ["gunicorn", "--bind", "0.0.0.0:8002", "ranking.wsgi:application"]