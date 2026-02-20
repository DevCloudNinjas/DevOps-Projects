docker exec -it web_prodxcloud_django python manage.py makemigrations
docker exec -it web_prodxcloud_django python manage.py migrate
echo 'Production Migration Operation Completed , Please Check the logs status'