# gunicorn_config.py

bind = "0.0.0.0:8000"
module = "multitenantsaas.wsgi:application"

workers = 4  # Adjust based on your server's resources
worker_connections = 1000
threads = 4

certfile = "/etc/letsencrypt/live/prodxcloud.io/fullchain.pem"
keyfile = "/etc/letsencrypt/live/prodxcloud.io/privkey.pem"

# docker-compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot --email joelwembo@outlook.com --agree-tos --no-eff-email -d prodxcloud.io
