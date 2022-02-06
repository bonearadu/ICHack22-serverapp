web: gunicorn serverapp.wsgi --log-file -
worker: python manage.py makemigrations && python manage.py migrate && python manage.py process_tasks