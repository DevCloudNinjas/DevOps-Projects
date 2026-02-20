docker exec -it web_prodxcloud_django python manage.py shell

tenant = Client(schema_name="app1", name="app1")

domain = Domain(domain="app1.127.0.0.1", tenant=tenant, is_primary=True)