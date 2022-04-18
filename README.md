# KTMFC
CSE 416 Project

# Steps to run
1. Makemigrations then migrate the changes to the database
2. If it is an actual release, turn off DEBUG, python manage.py collectstatic to pull all the static files together (For nginx/apache)
3. Then just do gunicorn --bind 0.0.0.0:8002 AlgoMarket.wsgi:application --daemon for running the application with WSGI.