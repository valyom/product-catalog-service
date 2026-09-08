from rest_framework import serializers

from inventory.models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category

        fields = [
            "id",
            "name",
            "parent",
            # version needs special handling - client should pass it 
            # but should not be able to change it.
            "version",
        ] 

        read_only_fields = [
            "id",
        ]

    def validate_version(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Version must be a positive integer."
            )

        return value

    def validate(self, attrs):
    
        # Provides special handling for the version
        request = self.context.get("request")

        if (
            request
            and request.method in ("PUT", "PATCH")
            and "version" not in attrs
        ):
            raise serializers.ValidationError(
                {
                    "version": (
                        "This field is required for updates."
                    )
                }
            )

        return attrs