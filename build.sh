#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Recolectar archivos estáticos (CSS, JS)
python manage.py collectstatic --no-input

# Aplicar migraciones a la base de datos de la nube
python manage.py migrate

# --- LÍNEA NUEVA ---
# Crea el superusuario automáticamente si no existe (usando las variables que pusimos en Render)
python manage.py createsuperuser --noinput || echo "El superusuario ya existe, saltando creación."