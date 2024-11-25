# Usar la imagen personalizada base que ya tiene Node.js, Python, y Angular instalados
FROM minero420/adnbase:latest

# Instalar dependencias adicionales necesarias para venv
USER root
RUN apt-get update && apt-get install -y python3.11-venv

# Establecer el directorio de trabajo para Django
WORKDIR /usr/src/app/django

# Copiar los archivos del proyecto Django al contenedor
COPY ./django /usr/src/app/django

# Crear un ambiente virtual para Python
RUN python3 -m venv /usr/src/app/venv

# Activar el ambiente virtual e instalar las dependencias de Python
RUN /usr/src/app/venv/bin/pip install --upgrade pip && \
    /usr/src/app/venv/bin/pip install -r /usr/src/app/django/requirements.txt

# Configurar el entorno virtual como predeterminado
ENV PATH="/usr/src/app/venv/bin:$PATH"

# Establecer el directorio de trabajo para Angular
WORKDIR /usr/src/app/angular

# Copiar los archivos del proyecto Angular al contenedor
COPY ./angular /usr/src/app/angular

# Instalar las dependencias de Angular (si es necesario)
RUN npm install --legacy-peer-deps --verbose

# Construir la aplicación Angular para producción
RUN ng build

# Exponer puertos para Nginx, que manejará tanto el frontend como el backend
EXPOSE 80
EXPOSE 8000
EXPOSE 4200

# Copiar la configuración de Nginx para servir Angular y hacer proxy hacia Django
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

# Crear un script para ejecutar ambos servicios (Django y Angular) en segundo plano y luego iniciar Nginx
COPY ./start.sh /start.sh
RUN chmod +x /start.sh

# Comando para iniciar el script que ejecutará tanto Django como Angular y luego Nginx
CMD ["/bin/bash", "/start.sh"]
