
docker exec -it prodxcloud-django-web python manage.py makemigrations
docker exec -it prodxcloud-django-web python manage.py migrate

docker exec -it prodxcloud-django-web python manage.py createsuperuser

