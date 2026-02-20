
docker exec -it django_fintech_enterprise_container celery -A multitenantsaas worker -l INFO
docker exec -it django_fintech_enterprise_container celery -A multitenantsaas beat -l INFO
