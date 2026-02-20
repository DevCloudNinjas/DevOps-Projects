from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

from apps import users

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

class Domain(DomainMixin):
    pass


class Country(models.Model):
    name = models.CharField(max_length=255)

# class Account(models.Model):
#     user = models.ForeignKey(users, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     domain = models.CharField(max_length=255)
#     subdomain = models.CharField(max_length=255)
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)

#     class TenantMeta:
#         tenant_field_name = 'id'

# class Manager(models.Model):
#     name = models.CharField(max_length=255)
#     account = models.ForeignKey(
#         Account, on_delete=models.CASCADE, related_name="managers"
#     )
#     class TenantMeta:
#         tenant_field_name = 'account_id'
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['id', 'account_id'], name='unique_manager_account')
#         ]

# class Project(models.Model):
#     name = models.CharField(max_length=255)
#     account = models.ForeignKey(
#         Account, related_name="projects", on_delete=models.CASCADE
#     )
#     managers = models.ManyToManyField(Manager, through="ProjectManager")
#     class TenantMeta:
#         tenant_field_name = 'account_id'

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['id', 'account_id'], name='unique_project_account')
#         ]

# class ProjectManager(models.Model):
#     project = TenantForeignKey(
#         Project, on_delete=models.CASCADE, related_name="projectmanagers"
#     )
#     manager = TenantForeignKey(Manager, on_delete=models.CASCADE)
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)

#     class TenantMeta:
#         tenant_field_name = 'account_id'