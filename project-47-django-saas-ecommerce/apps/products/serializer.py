from rest_framework import serializers

from .models import Product , Price , ProductTag


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ("id", "product", 'price')

class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ("id", "name")

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "tags", "desc" , "thumbnail", "url", "quantity")


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name")



class ProductEditableSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
    )
    account = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Product
        fields = ("id", "name", "tags", "desc" , "thumbnail", "url", "quantity")