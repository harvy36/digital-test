# digital-test

Este proyecto es una aplicación basada en Django y PostgreSQL, diseñada para ejecutarse fácilmente mediante Docker y Docker Compose.

## Requisitos Previos

- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/

## Instalación y Ejecución Paso a Paso

### 1. Instala Docker y Docker Compose

Sigue la documentación oficial para tu sistema operativo:

- [Instalar Docker](https://docs.docker.com/get-docker/)
- [Instalar Docker Compose](https://docs.docker.com/compose/install/)

Verifica la instalación ejecutando:

```sh
docker --version
docker compose version
```

### 2. Clona el repositorio

```sh
git clone https://github.com/harvy36/digital-test.git
cd digital-test
```

### 3. Configura las variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido de ejemplo, ajustando los valores según tus preferencias:

```env
POSTGRES_USER=usuario
POSTGRES_PASSWORD=contraseña_segura
POSTGRES_DB=nombre_base
TZ=America/Bogota
```

### 4. Levanta los contenedores

Ejecuta el siguiente comando en la raíz del proyecto:

```sh
docker compose up --build
```

Esto hará lo siguiente:
- Construirá la imagen de la app Django.
- Levantará un contenedor para la base de datos PostgreSQL.
- Levantará un contenedor para la aplicación web, que se conectará automáticamente a la base de datos.

### 5. Acceso a la aplicación

Una vez que los contenedores estén en ejecución, la aplicación estará disponible en:

```
http://localhost:8000
```

### 6. Parar los contenedores

Para detener los servicios, presiona `Ctrl+C` en la terminal donde ejecutaste Docker Compose, o bien:

```sh
docker compose down
```

## Dependencias principales

- Django==4.2
- psycopg2-binary==2.9.6
- django-rest-framework
- django-filter

## Notas adicionales

- Los datos de la base de datos se almacenan en un volumen Docker llamado `pgdata`, por lo que la información persiste aunque apagues los contenedores.
- Puedes modificar el archivo `requirements.txt` si necesitas agregar o actualizar dependencias de Python.

---

¡Listo! Con estos pasos deberías poder levantar el entorno de desarrollo de `digital-test` usando Docker desde cero.