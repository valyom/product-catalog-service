from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
)

from inventory.serializers.product import (
    ProductReadSerializer,
    ProductWriteSerializer,
)

product_not_found_example = OpenApiExample(
    "Product not found",
    summary="Product does not exist",
    description=(
        "Returned when no product exists with "
        "the specified ID."
    ),
    value={
        "detail": "No Product matches the given query."
    },
    response_only=True,
    status_codes=["404"],
)

product_list_schema = extend_schema(
    summary="List and search products",
    description=(
        "Returns a paginated list of products. "
        "Products can be filtered by title, SKU, category "
        "and price range."
    ),
    parameters=[
        OpenApiParameter(
            name="title",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description=(
                "Case-insensitive partial match "
                "against the product title."
            ),
        ),
        OpenApiParameter(
            name="sku",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Exact product SKU match.",
        ),
        OpenApiParameter(
            name="category_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description=(
                "Returns products from the selected category "
                "and all of its descendant categories."
            ),
        ),
        OpenApiParameter(
            name="price_min",
            type=OpenApiTypes.DECIMAL,
            location=OpenApiParameter.QUERY,
            description=(
                "Minimum product price. "
                "Must be greater than or equal to zero."
            ),
        ),
        OpenApiParameter(
            name="price_max",
            type=OpenApiTypes.DECIMAL,
            location=OpenApiParameter.QUERY,
            description=(
                "Maximum product price. "
                "Must be greater than or equal to zero."
            ),
        ),
    ],
    responses={
        200: ProductReadSerializer,
        400: None, 
    },
    examples=[
        OpenApiExample(
            "Invalid price range",
            summary="Minimum price is greater than maximum price",
            description=(
                "Example validation error returned when "
                "price_min is greater than price_max."
            ),
            value={
                "price_range": [
                    "price_min cannot be greater than price_max."
                ],
            },
            response_only=True,
            status_codes=["400"],
        ),
    ],
)


product_create_schema = extend_schema(
    summary="Create a product",
    description="Creates a new product.",
    request=ProductWriteSerializer,
    responses={
        201: ProductReadSerializer, 
    },
    examples=[
        OpenApiExample(
            "Create product request",
            summary="Create fresh milk product",
            description=(
                "Example request for creating a new product."
            ),
            value={
                "sku": "DAIRY-MILK-001",
                "title": "Fresh Milk 3.2%",
                "description": "Fresh cow milk",
                "image": "https://example.com/milk.jpg",
                "price": "3.49",
                "category": 1,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Create product response",
            summary="Created product",
            description=(
                "Example response returned after successfully "
                "creating a product."
            ),
            value={
                "id": 1,
                "sku": "DAIRY-MILK-001",
                "title": "Fresh Milk 3.2%",
                "description": "Fresh cow milk",
                "image": "https://example.com/milk.jpg",
                "price": "3.49",
                "category": {
                    "id": 1,
                    "name": "Dairy Products",
                    "parent": None,
                },
            },
            response_only=True,
            status_codes=["201"],
        ),
    ],
)

product_retrieve_schema = extend_schema(
    summary="Retrieve a product",
    description=(
        "Returns a product by its ID."
    ),
    responses={
        200: ProductReadSerializer,
        404: None,
    },
    examples=[
        OpenApiExample(
            "Product response",
            summary="Fresh milk product",
            description=(
                "Example response returned when retrieving "
                "a product."
            ),
            value={
                "id": 1,
                "sku": "DAIRY-MILK-001",
                "title": "Fresh Milk 3.2%",
                "description": "Fresh cow milk",
                "image": "https://example.com/milk.jpg",
                "price": "3.49",
                "category": {
                    "id": 1,
                    "name": "Dairy Products",
                    "parent": None,
                },
            },
            response_only=True,
            status_codes=["200"],
        ),
        product_not_found_example,
    ],
)


product_update_schema = extend_schema(
    summary="Update a product",
    description=(
        "Replaces all product fields with the provided values."
    ),
    request=ProductWriteSerializer,
    responses={
        200: ProductReadSerializer,
        400: None,
        404: None,
        },
    examples=[
        OpenApiExample(
            "Update product request",
            summary="Update fresh milk product",
            description=(
                "Example request for replacing all product fields."
            ),
            value={
                "sku": "DAIRY-MILK-001",
                "title": "Fresh Milk 3.2%",
                "description": "Fresh cow milk - 1 litre",
                "image": "https://example.com/milk.jpg",
                "price": "3.79",
                "category": 1,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Update product response",
            summary="Updated product",
            description=(
                "Example response returned after successfully "
                "updating a product."
            ),
            value={
                "id": 1,
                "sku": "DAIRY-MILK-001",
                "title": "Fresh Milk 3.2%",
                "description": "Fresh cow milk - 1 litre",
                "image": "https://example.com/milk.jpg",
                "price": "3.79",
                "category": {
                    "id": 1,
                    "name": "Dairy Products",
                    "parent": None,
                },
            },
            response_only=True,
            status_codes=["200"],
        ),
        product_not_found_example,
    ],
)


product_partial_update_schema = extend_schema(
    summary="Partially update a product",
    description=(
        "Updates only the provided product fields."
    ),
    request=ProductWriteSerializer,
    responses={
        200: ProductReadSerializer,
        400: None,
        404: None,
    },
    examples=[
        OpenApiExample(
            "Update product price",
            summary="Update only the product price",
            description=(
                "Example request for updating only "
                "the product price."
            ),
            value={
                "price": "3.79",
            },
            request_only=True,
        ),
        OpenApiExample(
            "Partial update response",
            summary="Updated product",
            description=(
                "Example response returned after successfully "
                "updating the product."
            ),
            value={
                "id": 1,
                "sku": "DAIRY-MILK-001",
                "title": "Fresh Milk 3.2%",
                "description": "Fresh cow milk",
                "image": "https://example.com/milk.jpg",
                "price": "3.79",
                "category": {
                    "id": 1,
                    "name": "Dairy Products",
                    "parent": None,
                },
            },
            response_only=True,
            status_codes=["200"],
        ),
        product_not_found_example,
    ],
)


product_delete_schema = extend_schema(
    summary="Delete a product",
    description=(
        "Deletes a product by its ID."
    ),
    responses={
        204: None,
        404: None,
    },
)

