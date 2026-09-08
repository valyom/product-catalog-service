from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema_view

from inventory.pagination import ProductPagination
from inventory.serializers.product import (
    ProductReadSerializer,
    ProductSearchSerializer,
    ProductWriteSerializer,
)
from inventory.services.product_service import ProductService
from inventory.api_docs.product import (
    product_list_schema,
    product_create_schema,
    product_retrieve_schema,
    product_update_schema,
    product_partial_update_schema,
    product_delete_schema
)

@extend_schema_view(
    get=product_list_schema,
    post=product_create_schema,
)
class ProductListCreateView(generics.ListCreateAPIView):

    ALLOWED_QUERY_PARAMS = {
        "title",
        "sku",
        "category_id",
        "price_min",
        "price_max",
        "page",
        "page_size",
    }

    serializer_class = ProductReadSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        self._validate_query_params()

        serializer = ProductSearchSerializer(
            data=self.request.query_params,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        return ProductService.get_products(
            **serializer.validated_data,
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductWriteSerializer

        return ProductReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        product = ProductService.create_product(
            **serializer.validated_data,
        )

        response_serializer = ProductReadSerializer(
            product,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def _validate_query_params(self) -> None:
        unsupported_params = (
            set(self.request.query_params.keys())
            - self.ALLOWED_QUERY_PARAMS
        )

        if unsupported_params:
            raise ValidationError(
                dict.fromkeys(
                    unsupported_params,
                    "Unsupported query parameter.",
                )
            )

@extend_schema_view(
    get=product_retrieve_schema,
    put=product_update_schema,
    patch=product_partial_update_schema,
    delete=product_delete_schema,
)
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        return ProductService.get_queryset()

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ProductWriteSerializer

        return ProductReadSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)

        product = self.get_object()

        serializer = self.get_serializer(
            product,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(raise_exception=True)
        # The product may be deleted after serializer validation
        # and before the service acquires the row lock.
        # ProductService._locked_product() handles this with 404.
        product = ProductService.update_product(
            product_id=product.pk,
            **serializer.validated_data,
        )

        response_serializer = ProductReadSerializer(product)

        return Response(response_serializer.data)

    def destroy(self, request, *args, **kwargs):
        ProductService.delete_product(product_id=self.kwargs["pk"])

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )