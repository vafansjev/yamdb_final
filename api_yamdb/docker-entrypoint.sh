echo "Apply database migrations"
python manage.py migrate --noinput
echo "Collect static files"
python manage.py collectstatic --no-input
echo "Starting gunicorn server"
gunicorn api_yamdb.wsgi:application --bind 0:8000