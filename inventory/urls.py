from django.urls import path

from inventory.views.category import (
    CategoryDetailView,
    CategoryListCreateView,
)
from inventory.views.product import (
    ProductDetailView,
    ProductListCreateView,
)


urlpatterns = [
    path(
        "categories/",
        CategoryListCreateView.as_view(),
        name="category-list-create",
    ),
    path(
        "categories/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category-detail",
    ),
    path(
        "products/",
        ProductListCreateView.as_view(),
        name="product-list-create",
    ),
    path(
        "products/<int:pk>/",
        ProductDetailView.as_view(),
        name="product-detail",
    ),
]