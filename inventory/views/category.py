from rest_framework import generics, status
from rest_framework.response import Response

from inventory.exceptions import CategoryDeletionError
from inventory.serializers.category import CategorySerializer
from inventory.services.category_service import CategoryService


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return CategoryService.get_queryset()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = CategoryService.create_category(
            **serializer.validated_data
        )

        response_serializer = self.get_serializer(category)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return CategoryService.get_queryset()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)

        category = self.get_object()

        serializer = self.get_serializer(
            category,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(raise_exception=True)

        category = CategoryService.update_category(
            category,
            **serializer.validated_data,
        )

        response_serializer = self.get_serializer(category)

        return Response(response_serializer.data)

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()

        try:
            CategoryService.delete_category(category)
        except CategoryDeletionError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )