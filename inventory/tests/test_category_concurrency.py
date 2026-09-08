from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from inventory.exceptions import CategoryVersionConflictError
from inventory.models import Category
from inventory.services.category_service import CategoryService


class CategoryOptimisticLockingServiceTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
        )

    def test_update_category_increments_version(self):

        category = CategoryService.update_category(
            self.category,
            name="Electronics Updated",
            version=1,
        )

        category.refresh_from_db()

        self.assertEqual(
            category.name,
            "Electronics Updated",
        )

        self.assertEqual(
            category.version,
            2,
        )

    def test_update_category_rejects_stale_version(self):

        CategoryService.update_category(
            self.category,
            name="Electronics Updated",
            version=1,
        )

        with self.assertRaises(
            CategoryVersionConflictError
        ):
            CategoryService.update_category(
                self.category,
                name="Another Update",
                version=1,
            )

        self.category.refresh_from_db()

        self.assertEqual(
            self.category.name,
            "Electronics Updated",
        )

        self.assertEqual(
            self.category.version,
            2,
        )


class CategoryOptimisticLockingApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.category = Category.objects.create(
            name="Electronics",
        )

        self.url = (
            f"/api/v1/categories/{self.category.pk}/"
        )

    def test_update_category_returns_updated_version(self):

        response = self.client.patch(
            self.url,
            {
                "name": "Electronics Updated",
                "version": 1,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["name"],
            "Electronics Updated",
        )

        self.assertEqual(
            response.data["version"],
            2,
        )

    def test_update_category_returns_conflict_for_stale_version(self):

        first_response = self.client.patch(
            self.url,
            {
                "name": "Electronics Updated",
                "version": 1,
            },
            format="json",
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_200_OK,
        )

        second_response = self.client.patch(
            self.url,
            {
                "name": "Another Update",
                "version": 1,
            },
            format="json",
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_409_CONFLICT,
        )

        self.assertEqual(
            second_response.data["detail"],
            (
                "Category was modified by another request. "
                "Please reload and try again."
            ),
        )

        self.category.refresh_from_db()

        self.assertEqual(
            self.category.name,
            "Electronics Updated",
        )

        self.assertEqual(
            self.category.version,
            2,
        )