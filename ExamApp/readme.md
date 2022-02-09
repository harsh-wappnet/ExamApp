docker-compose up -d --build

docker-compose exec web python manage.py migrate --noinput

docker-compose exec db psql --username=hello_django --dbname=hello_django_dev

