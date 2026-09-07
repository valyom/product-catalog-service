import logging

from decimal import Decimal


from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from inventory.models import Category, Product
from inventory.services.category_service import CategoryService

logger = logging.getLogger(__name__)


class ProductService:

    @staticmethod
    def get_queryset():
        return ( 
            Product.objects
                .select_related("category")
                .order_by("id")
        )

    @staticmethod
    def create_product(**validated_data):
        product = Product.objects.create(**validated_data)

        logger.info(
            "Product created: id=%s, sku=%s",
            product.pk,
            product.sku,
        )

        return product

    @staticmethod
    def update_product(product, **validated_data):
        for field, value in validated_data.items():
            setattr(product, field, value)

        product.save()

        logger.info(
            "Product updated: id=%s, sku=%s",
            product.pk,
            product.sku,
        )

        return product

    @staticmethod
    def delete_product(product):
        product_id = product.pk
        product_sku = product.sku

        product.delete()

        logger.info(
            "Product deleted: id=%s, sku=%s",
            product_id,
            product_sku,
        )

    @staticmethod
    def get_products(
        *,
        title: str | None = None,
        sku: str | None = None,
        category_id: int | None = None,
        price_min: Decimal | None = None,
        price_max: Decimal | None = None,
    ) -> QuerySet[Product]:
        
        queryset = ProductService.get_queryset()

        if title:
            queryset = queryset.filter(
                title__icontains=title
            )

        if sku:
            queryset = queryset.filter(
                sku=sku
            )

        if category_id is not None:
            try:
                category = Category.objects.get(
                    pk=category_id
                )
            except Category.DoesNotExist:
                logger.warning(
                    "Product search requested with non-existing category: "
                    "category_id=%s",
                    category_id,
                )

                raise ValidationError(
                    {
                        "category_id": "Category does not exist."
                    }
                )

            category_ids = CategoryService.get_descendant_ids(
                category
            )

            queryset = queryset.filter(
                category_id__in=category_ids
            )

        if price_min is not None:
            queryset = queryset.filter(
                price__gte=price_min
            )

        if price_max is not None:
            queryset = queryset.filter(
                price__lte=price_max
            )

        return queryset