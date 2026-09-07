from rest_framework import serializers

from inventory.models import Product
from inventory.serializers.category import CategorySerializer


class ProductWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product

        fields = [
            "id",
            "sku",
            "title",
            "description",
            "image",
            "price",
            "category",
        ]

        read_only_fields = [
            "id",
        ]


class ProductReadSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product

        fields = [
            "id",
            "sku",
            "title",
            "description",
            "image",
            "price",
            "category",
        ]        