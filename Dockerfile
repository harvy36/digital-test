# Usa una imagen base de Python
FROM python:3.9

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=America/Bogota

# Instala tzdata y configura la zona horaria
RUN apt-get update && apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# Crea el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . /app/

# Expone el puerto 8000 para la aplicación
EXPOSE 8000

