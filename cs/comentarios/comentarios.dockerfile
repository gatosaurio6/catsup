FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Como tu proyecto es independiente, usar /app es perfecto y estándar
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

# Tu puerto asignado sigue siendo el 8003
EXPOSE 8003

# Reemplaza 'comentarios_backend' por el nombre real que le des a la carpeta de configuración de TU proyecto
CMD ["gunicorn", "--bind", "0.0.0.0:8003", "comentarios.wsgi:application"]