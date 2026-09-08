from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema,
)

from inventory.serializers.category import CategorySerializer


category_list_schema = extend_schema(
    summary="List categories",
    description=(
        "Returns a list of all categories."
    ),
    responses={
        200: CategorySerializer(many=True),
    },
    examples=[
        OpenApiExample(
            "Category list",
            summary="Example category list",
            description=(
                "Example response containing product categories."
            ),
            value=[
                {
                    "id": 1,
                    "name": "Food",
                    "parent": None,
                },
                {
                    "id": 2,
                    "name": "Dairy Products",
                    "parent": 1,
                },
                {
                    "id": 3,
                    "name": "Bakery",
                    "parent": 1,
                },
            ],
            response_only=True,
            status_codes=["200"],
        ),
    ],
)


category_create_schema = extend_schema(
    summary="Create a category",
    description=(
        "Creates a new product category. "
        "A category can optionally have a parent category."
    ),
    request=CategorySerializer,
    responses={
        201: CategorySerializer,
        400: None,
    },
    examples=[
        OpenApiExample(
            "Create root category",
            summary="Create root category",
            description=(
                "Example request for creating a root category."
            ),
            value={
                "name": "Food",
                "parent": None,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Create child category",
            summary="Create child category",
            description=(
                "Example request for creating a category "
                "with a parent category."
            ),
            value={
                "name": "Dairy Products",
                "parent": 1,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Created category",
            summary="Created category",
            description=(
                "Example response returned after successfully "
                "creating a category."
            ),
            value={
                "id": 2,
                "name": "Dairy Products",
                "parent": 1,
            },
            response_only=True,
            status_codes=["201"],
        ),
    ],
)


category_retrieve_schema = extend_schema(
    summary="Retrieve a category",
    description=(
        "Returns a category by its ID."
    ),
    responses={
        200: CategorySerializer,
        404: None,
    },
    examples=[
        OpenApiExample(
            "Category response",
            summary="Dairy Products category",
            description=(
                "Example response returned when retrieving "
                "a category."
            ),
            value={
                "id": 2,
                "name": "Dairy Products",
                "parent": 1,
            },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Category not found",
            summary="Category does not exist",
            description=(
                "Returned when no category exists with "
                "the specified ID."
            ),
            value={
                "detail": "No Category matches the given query."
            },
            response_only=True,
            status_codes=["404"],
        ),
    ],
)


category_update_schema = extend_schema(
    summary="Update a category",
    description=(
        "Replaces all category fields with the provided values. "
        "The category hierarchy cannot contain cycles."
    ),
    request=CategorySerializer,
    responses={
        200: CategorySerializer,
        400: None,
        404: None,
    },
    examples=[
        OpenApiExample(
            "Update category request",
            summary="Rename category",
            description=(
                "Example request for updating a category."
            ),
            value={
                "name": "Fresh Dairy Products",
                "parent": 1,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Updated category",
            summary="Updated category",
            description=(
                "Example response returned after successfully "
                "updating a category."
            ),
            value={
                "id": 2,
                "name": "Fresh Dairy Products",
                "parent": 1,
            },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Category cannot be its own parent",
            summary="Invalid parent category",
            description=(
                "Returned when a category is assigned "
                "as its own parent."
            ),
            value={
                "parent": [
                    "A category cannot be its own parent."
                ],
            },
            response_only=True,
            status_codes=["400"],
        ),
        OpenApiExample(
            "Category hierarchy cycle",
            summary="Category hierarchy cycle detected",
            description=(
                "Returned when assigning a parent would create "
                "a cycle in the category hierarchy."
            ),
            value={
                "parent": [
                    "Category hierarchy cannot contain a cycle."
                ],
            },
            response_only=True,
            status_codes=["400"],
        ),
        OpenApiExample(
            "Category not found",
            summary="Category does not exist",
            description=(
                "Returned when no category exists with "
                "the specified ID."
            ),
            value={
                "detail": "No Category matches the given query."
            },
            response_only=True,
            status_codes=["404"],
        ),
    ],
)


category_partial_update_schema = extend_schema(
    summary="Partially update a category",
    description=(
        "Updates only the provided category fields. "
        "The category hierarchy cannot contain cycles."
    ),
    request=CategorySerializer,
    responses={
        200: CategorySerializer,
        400: None,
        404: None,
    },
    examples=[
        OpenApiExample(
            "Rename category",
            summary="Update category name",
            description=(
                "Example request for updating only "
                "the category name."
            ),
            value={
                "name": "Fresh Dairy Products",
            },
            request_only=True,
        ),
        OpenApiExample(
            "Move category",
            summary="Update category parent",
            description=(
                "Example request for assigning a different "
                "parent category."
            ),
            value={
                "parent": 5,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Partial update response",
            summary="Updated category",
            description=(
                "Example response returned after successfully "
                "updating a category."
            ),
            value={
                "id": 2,
                "name": "Fresh Dairy Products",
                "parent": 1,
            },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Category cannot be its own parent",
            summary="Invalid parent category",
            description=(
                "Returned when a category is assigned "
                "as its own parent."
            ),
            value={
                "parent": [
                    "A category cannot be its own parent."
                ],
            },
            response_only=True,
            status_codes=["400"],
        ),
        OpenApiExample(
            "Category hierarchy cycle",
            summary="Category hierarchy cycle detected",
            description=(
                "Returned when assigning a parent would create "
                "a cycle in the category hierarchy."
            ),
            value={
                "parent": [
                    "Category hierarchy cannot contain a cycle."
                ],
            },
            response_only=True,
            status_codes=["400"],
        ),
        OpenApiExample(
            "Category not found",
            summary="Category does not exist",
            description=(
                "Returned when no category exists with "
                "the specified ID."
            ),
            value={
                "detail": "No Category matches the given query."
            },
            response_only=True,
            status_codes=["404"],
        ),
    ],
)


category_delete_schema = extend_schema(
    summary="Delete a category",
    description=(
        "Deletes a category by its ID. "
        "A category cannot be deleted while it is still "
        "referenced by products or child categories."
    ),
    responses={
        204: None,
        404: None,
        409: None,
    },
    examples=[
        OpenApiExample(
            "Category deletion blocked",
            summary="Category is still in use",
            description=(
                "Returned when the category is still referenced "
                "by products or child categories."
            ),
            value={
                "detail": (
                    "Category cannot be deleted because it is still "
                    "referenced by products or child categories."
                ),
            },
            response_only=True,
            status_codes=["409"],
        ),
        OpenApiExample(
            "Category not found",
            summary="Category does not exist",
            description=(
                "Returned when no category exists with "
                "the specified ID."
            ),
            value={
                "detail": "No Category matches the given query."
            },
            response_only=True,
            status_codes=["404"],
        ),
    ],
)