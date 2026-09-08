from rest_framework import generics, status
from rest_framework.response import Response
from decimal import Decimal, InvalidOperation

from drf_spectacular.utils import (
    extend_schema_view,
)
from rest_framework.exceptions import ValidationError 

from inventory.pagination import ProductPagination
from inventory.serializers.product import (
    ProductReadSerializer,
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
        
        title = self.request.query_params.get("title")
        sku = self.request.query_params.get("sku")
        category_id = self.request.query_params.get("category_id")
        price_min = self.request.query_params.get("price_min")
        price_max = self.request.query_params.get("price_max")

        category_id_value = (
            self._parse_positive_int(
                "category_id",
                category_id,
            )
            if category_id is not None
            else None
        )

        price_min_value = (
            self._parse_decimal(
                "price_min",
                price_min,
            )
            if price_min is not None
            else None
        )

        price_max_value = ( 
            self._parse_decimal(
                "price_max",
                price_max,
            )
            if price_max is not None 
            else None
        )

        title_value = (
            self._parse_non_empty_string(
                "title",
                title,
            )
            if title is not None
            else None
        )

        sku_value = (
            self._parse_non_empty_string(
                "sku",
                sku,
            )
            if sku is not None
            else None
        )

        if (
            price_min_value is not None
            and price_max_value is not None
            and price_min_value > price_max_value
        ):
            raise ValidationError(
                {
                    "price_range": (
                        "price_min cannot be greater than price_max."
                    )
                }
            )

        return ProductService.get_products(
            title=title_value,
            sku=sku_value,
            category_id=category_id_value,
            price_min=price_min_value,
            price_max=price_max_value,
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductWriteSerializer

        return ProductReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) #ProductWriteSerializer
        serializer.is_valid(raise_exception=True)

        product = ProductService.create_product(
            **serializer.validated_data
        )

        response_serializer = ProductReadSerializer(product)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def _parse_non_empty_string(
        param: str,
        value: str,
    ) -> str:
        parsed_value = value.strip()

        if not parsed_value:
            raise ValidationError(
                {
                    param: "Must not be empty."
                }
            )

        return parsed_value
    
    @staticmethod
    def _parse_positive_int(
        param: str,
        value: str,
    ) -> int:
        try:
            parsed_value = int(value)
        except ValueError:
            raise ValidationError(
                {
                    param: "Must be a valid integer."
                }
            )

        if parsed_value <= 0:
            raise ValidationError(
                {
                    param: "Must be a positive integer."
                }
            )

        return parsed_value

        
    @staticmethod
    def _parse_decimal(
        param: str,
        value: str,
    ) -> Decimal:
        try:
            parsed_value = Decimal(value)
        except InvalidOperation:
            raise ValidationError(
                {
                    param: "Must be a valid decimal number."
                }
            )

        if parsed_value < 0:
            raise ValidationError(
                {
                    param: "Must be greater than or equal to zero."
                }
            )

        return parsed_value
        
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