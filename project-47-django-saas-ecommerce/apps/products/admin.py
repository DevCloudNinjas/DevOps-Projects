from django.contrib import admin

# Register your models here.
from .models import Price, Product, ProductTag , PaymentHistory

class PriceAdmin(admin.StackedInline):
    model = Price

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (PriceAdmin,)

    class Meta:
        model = Product

admin.site.register(ProductTag)
admin.site.register(Price)
admin.site.register(PaymentHistory)