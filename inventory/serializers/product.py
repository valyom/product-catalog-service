from decimal import Decimal

from rest_framework import serializers

from inventory.models import Product
from inventory.serializers.category import CategorySerializer


class ProductWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "sku",
            "title",
            "description",
            "image",
            "price",
            "category",
        ]


class ProductSearchSerializer(serializers.Serializer):
    title = serializers.CharField(
        required=False,
        allow_blank=False,
    )

    sku = serializers.CharField(
        required=False,
        allow_blank=False,
    )

    category_id = serializers.IntegerField(
        required=False,
        min_value=1,
        error_messages={
            "invalid": "Must be a valid integer.",
            "min_value": "Must be a positive integer.",
        },
    )

    price_min = serializers.DecimalField(
        required=False,
        min_value=Decimal("0"),
        max_digits=10,
        decimal_places=2,
        error_messages={
            "invalid": "Must be a valid decimal number.",
            "min_value": (
                "Must be greater than or equal to zero."
            ),
        },
    )

    price_max = serializers.DecimalField(
        required=False,
        min_value=Decimal("0"),
        max_digits=10,
        decimal_places=2,
        error_messages={
            "invalid": "Must be a valid decimal number.",
            "min_value": (
                "Must be greater than or equal to zero."
            ),
        },
    )

    def validate(self, attrs):
        price_min = attrs.get("price_min")
        price_max = attrs.get("price_max")

        if (
            price_min is not None
            and price_max is not None
            and price_min > price_max
        ):
            raise serializers.ValidationError(
                {
                    "price_range": (
                        "price_min cannot be greater than "
                        "price_max."
                    )
                }
            )

        return attrs


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