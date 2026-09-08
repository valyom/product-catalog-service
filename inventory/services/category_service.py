import logging

from django.db import transaction
from django.db.models import F
from django.db.models import F, ProtectedError
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from inventory.exceptions import (
    CategoryDeletionError,
    CategoryVersionConflictError,
)
from inventory.models import Category


logger = logging.getLogger(__name__)


class CategoryService:

    @staticmethod
    def get_queryset():
        return Category.objects.select_related("parent")

    @staticmethod
    @transaction.atomic
    def create_category(name, parent=None):
        category = Category.objects.create(
            name=name,
            parent=parent,
        )

        logger.info(
            "Category created: id=%s, name=%s",
            category.pk,
            category.name,
        )

        return category

    @staticmethod
    @transaction.atomic
    def update_category(category, **validated_data):
        """
        Updates a category using optimistic locking.

        The database update matches both the category ID and the
        version provided by the client. This prevents concurrent
        requests from silently overwriting each other's changes.

        If the parent is being changed, the category hierarchy is
        validated before the update to prevent self-references and
        cycles.

        On success, the category version is incremented.
        """

        expected_version = validated_data.pop("version")

        if "parent" in validated_data:
            parent = validated_data["parent"]

            if parent is not None:
                CategoryService._validate_parent(
                    category,
                    parent,
                )

        updated_count = (
            Category.objects
            .filter(
                pk=category.pk,
                version=expected_version,
            )
            .update(
                **validated_data,
                version=F("version") + 1,
            )
        )

        if updated_count == 0:

            logger.warning(
                "Category update conflict: id=%s, "
                "expected_version=%s",
                category.pk,
                expected_version,
            )

            raise CategoryVersionConflictError(
                "Category was modified by another request. "
                "Please reload and try again."
            )

        category.refresh_from_db()

        logger.info(
            "Category updated: id=%s, version=%s",
            category.pk,
            category.version,
        )

        return category

    @staticmethod
    @transaction.atomic
    def delete_category(category_id: int) -> None:

        category = get_object_or_404(
            Category,
            pk=category_id,
        )

        category_name = category.name

        try:
            category.delete()

        except ProtectedError:

            logger.warning(
                "Category deletion blocked: id=%s, name=%s",
                category_id,
                category_name,
            )

            raise CategoryDeletionError(
                "Category cannot be deleted because it is still "
                "referenced by products or child categories."
            )

        logger.info(
            "Category deleted: id=%s, name=%s",
            category_id,
            category_name,
        )

    @staticmethod
    def _validate_parent(
        category: Category,
        parent: Category,
    ) -> None:

        if parent.pk == category.pk:

            logger.warning(
                "Category cannot be its own parent: "
                "category_id=%s",
                category.pk,
            )

            raise ValidationError(
                {
                    "parent": (
                        "A category cannot be its own parent."
                    )
                }
            )

        current = parent

        while current is not None:

            if current.pk == category.pk:

                logger.warning(
                    "Category hierarchy cycle detected: "
                    "category_id=%s",
                    category.pk,
                )

                raise ValidationError(
                    {
                        "parent": (
                            "Category hierarchy cannot "
                            "contain a cycle."
                        )
                    }
                )

            current = current.parent

    @staticmethod
    def get_descendant_ids(
        category: Category,
    ) -> list[int]:

        if category is None:
            raise ValueError(
                "Category must not be None."
            )

        categories = Category.objects.only(
            "id",
            "parent_id",
        )

        children_by_parent: dict[int, list[int]] = {}

        for current_category in categories:

            if current_category.parent_id is not None:

                children_by_parent.setdefault(
                    current_category.parent_id,
                    [],
                ).append(
                    current_category.pk
                )

        category_ids = [category.pk]

        categories_to_process = [
            category.pk
        ]

        while categories_to_process:

            current_id = categories_to_process.pop()

            children = children_by_parent.get(
                current_id,
                [],
            )

            category_ids.extend(children)

            categories_to_process.extend(
                children
            )

        return category_ids