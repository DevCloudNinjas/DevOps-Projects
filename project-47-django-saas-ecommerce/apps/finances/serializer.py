from rest_framework import serializers

from .models import Account, Category, Transaction


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class CategorySerializer(serializers.ModelSerializer):
    parent_category = SimpleCategorySerializer()
    subcategories = SimpleCategorySerializer(many=True, read_only=True)

    def get_fields(self):
        fields = super().get_fields()
        if self.context["request"].method == "GET":
            fields["parent_category"] = SimpleCategorySerializer(read_only=True)
        else:
            fields["parent_category"] = serializers.PrimaryKeyRelatedField(
                queryset=Category.objects.all(), required=False, allow_null=True
            )
        return fields

    class Meta:
        model = Category
        fields = ("id", "name", "parent_category", "subcategories")


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id", "name", "initial_balance", "active")


class SimpleAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id", "name")


class TransactionSerializer(serializers.ModelSerializer):
    category = SimpleCategorySerializer(read_only=True)
    account = SimpleAccountSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ("id", "date", "amount", "description", "type", "category", "account")


class TransactionEditableSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())

    class Meta:
        model = Transaction
        fields = ("id", "date", "amount", "description", "type", "category", "account")