flask db upgrade
gunicorn wsgi:app -b 0.0.0.0 --access-logfile=/dev/stdout --error-logfile=/dev/stdout