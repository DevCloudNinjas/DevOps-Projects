from rest_framework import serializers
from apps.snippets.models import Snippet, Sales


# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']


class SalesSerializer(serializers.ModelSerializer):

    region = serializers.CharField(max_length=255, required=False)
    country = serializers.CharField(max_length=255, required=False)
    ptype = serializers.CharField(max_length=255, required=False)
    channel = serializers.CharField(max_length=255, required=False)
    date = serializers.DateField(format='%d.%m.%Y', required=False)
    quantity = serializers.IntegerField()
    price = serializers.FloatField()
    cost = serializers.FloatField()
    revenue = serializers.FloatField()
    profit = serializers.FloatField()

    profit_percentage = serializers.DecimalField(
        max_digits=10, decimal_places=2)

    class Meta:
        model = Sales
        fields = ('id', 'region', 'country', 'ptype', 'channel', 'date', 'quantity',
                  'price', 'cost', 'revenue', 'profit', 'profit_percentage')
