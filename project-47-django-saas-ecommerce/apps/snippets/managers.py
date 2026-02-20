from django.db import models
from .models import *
from django.db.models import F, ExpressionWrapper, DecimalField


class SalesQuerySet(models.QuerySet):

    def calculated_quantity(self):
        return self.model.objects.annotate(
            profit_percentage=ExpressionWrapper(
                (F('profit')/F('revenue')) * 100,
                output_field=DecimalField()
            ))


class SalesManager(models.Manager):
    def get_queryset(self):
        return SalesQuerySet(self.model, using=self._db)

    def calculated_quantity(self):
        return self.get_queryset().calculated_quantity()