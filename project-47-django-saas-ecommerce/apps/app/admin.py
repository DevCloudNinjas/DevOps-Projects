from django.contrib import admin

from .models import Client, Domain

admin.site.register(Client)
admin.site.register(Domain)
