celery -A multitenantsaas worker -l info
celery -A multitenantsaas beat -l info

celery -A multitenantsaas worker -l info --beat
