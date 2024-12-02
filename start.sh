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
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Iniciar el servidor Angular con redirección de logs
cd /usr/src/app/angular
npx ng serve --host 0.0.0.0 --port 4200 | sed -u 's/Local:.*4200/Local:   http:\/\/localhost:80/' &
ANGULAR_PID=$!

# Iniciar Nginx en modo no daemon
nginx -g "daemon off;" &
NGINX_PID=$!

# Esperar por los procesos hijo
wait "$DJANGO_PID"
wait "$ANGULAR_PID"
wait "$NGINX_PID"
