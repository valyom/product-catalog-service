import logging

from contextlib import contextmanager
from decimal import Decimal
import os
import threading

from django.db import (
    IntegrityError,
    transaction,
)
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
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
    @contextmanager
    def _locked_product(product_id: int):
        # Shared transaction and row-locking context
        # for product update and delete operations.
        with transaction.atomic():

            product = get_object_or_404(
                Product.objects.select_for_update(),
                pk=product_id,
            )

            yield product

    @staticmethod
    def create_product(**validated_data):
        try:
            with transaction.atomic():

                product = Product.objects.create(
                    **validated_data
                )

        except IntegrityError:
            sku = validated_data.get("sku")

            logger.warning(
                "Product not created: duplicate sku=%s",
                sku,
            )

            raise ValidationError(
                {
                    "sku": (
                        "Product with this SKU already exists."
                    )
                }
            )

        logger.info(
            "Product created: id=%s, sku=%s",
            product.pk,
            product.sku,
        )

        return product

    @staticmethod
    def update_product(
        product_id: int,
        **validated_data,
    ):

        with ProductService._locked_product(
            product_id
        ) as product:

            new_sku = validated_data.get(
                "sku",
                product.sku,
            )

            for field, value in validated_data.items():
                setattr(product, field, value)

            try:
                with transaction.atomic():
                    product.save()

            except IntegrityError:

                logger.warning(
                    "Product update failed: duplicate sku=%s",
                    new_sku,
                )

                raise ValidationError(
                    {
                        "sku": (
                            "Product with this SKU already exists."
                        )
                    }
                )

            logger.info(
                "Product updated: id=%s, sku=%s",
                product.pk,
                product.sku,
            )

            return product

    @staticmethod
    def delete_product(product_id: int):

        with ProductService._locked_product(
            product_id
        ) as product:

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
                    "Product search requested with "
                    "non-existing category: category_id=%s",
                    category_id,
                )

                raise ValidationError(
                    {
                        "category_id": (
                            "Category does not exist."
                        )
                    }
                )

            category_ids = (
                CategoryService.get_descendant_ids(
                    category
                )
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