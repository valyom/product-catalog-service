from rest_framework import generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view

from inventory.api_docs.category import (
    category_list_schema,
    category_create_schema,
    category_retrieve_schema,
    category_update_schema,
    category_partial_update_schema,
    category_delete_schema,
)
from inventory.exceptions import CategoryDeletionError
from inventory.serializers.category import CategorySerializer
from inventory.services.category_service import CategoryService

@extend_schema_view(
    get=category_list_schema,
    post=category_create_schema,
)
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

@extend_schema_view(
    get=category_retrieve_schema,
    put=category_update_schema,
    patch=category_partial_update_schema,
    delete=category_delete_schema,
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