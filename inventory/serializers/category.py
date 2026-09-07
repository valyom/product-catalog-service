from rest_framework import serializers

from inventory.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "parent",
        ]
        read_only_fields = [ 
            "id",
        ]