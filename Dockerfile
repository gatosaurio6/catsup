# 1. Usar una imagen oficial de Python súper ligera como base
FROM python:3.11-slim

# 2. Configurar variables de entorno para que Python funcione mejor en contenedores
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Crear una carpeta dentro del contenedor donde vivirá nuestro código
WORKDIR /app

# 4. Copiar solo el archivo de requerimientos primero (para aprovechar la caché de Docker)
COPY requirements.txt /app/

# 5. Instalar las librerías
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar el resto del código de tu proyecto al contenedor
COPY . /app/

# 7. Exponer el puerto por donde el servidor web de Django se comunicará
EXPOSE 8000

# 8. El comando que se ejecutará al encender el contenedor (0.0.0.0 permite que acepte conexiones externas)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]