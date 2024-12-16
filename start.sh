#!/bin/bash

# Función para manejar señales (SIGINT y SIGTERM)
cleanup() {
    echo "Apagando servicios..."
    kill -TERM "$DJANGO_PID" 2>/dev/null
    kill -TERM "$ANGULAR_PID" 2>/dev/null
    exit 0
}

# Atrapar señales
trap cleanup SIGINT SIGTERM

# Iniciar el servidor de Django
cd /usr/src/app/django
/usr/src/app/venv/bin/python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Iniciar el servidor Angular con redirección de logs
cd /usr/src/app/angular
ng serve --host 0.0.0.0 --port 4200 &
ANGULAR_PID=$!

# Iniciar Nginx en modo no daemon
nginx -g "daemon off;" &
NGINX_PID=$!

# Manejar el cierre de los procesos de Django y Angular
trap 'kill %1; kill %2' SIGINT SIGTERM

# Esperar por los procesos hijo
wait "$DJANGO_PID"
wait "$ANGULAR_PID"
wait "$NGINX_PID"
