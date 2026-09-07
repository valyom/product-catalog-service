from decimal import Decimal
from unittest import skip

from rest_framework import status
from rest_framework.test import APITestCase

from inventory.models import Category, Product

class ProductSearchTests(APITestCase):
    #   Test Catalog Hierarchy:
    #    
    #      Food (id=1)
    #      │
    #      ├── Fruits and Vegetables (id=2)
    #      │   ├── Fruits (id=3)
    #      │   │   ├── Bananas       sku="FRUIT-BANANA-001" price=Decimal("2.99"),
    #      │   │   └── Green Apples  sku="FRUIT-APPLE-001", price=Decimal("3.49"),
    #      │   │
    #      │   └── Vegetables (id=4)
    #      │       └── Tomatoes      sku="VEG-TOMATO-001",  price=Decimal("4.99"),
    #      │
    #      ├── Dairy and Eggs (id=5)
    #      │   ├── Greek Yogurt      sku="DAIRY-YOGURT-001", price=Decimal("2.79"), 
    #      │   └── Fresh Milk        sku="DAIRY-MILK-001",   price=Decimal("3.19")
    #      │
    #      └── Ready Meals (id=6)
    #          ├── Salads  (id=7)
    #          │   ├── Chicken Caesar Salad  sku="MEAL-SALAD-001", price=Decimal("8.99"),
    #          │   └── Greek Salad           sku="MEAL-SALAD-002", price=Decimal("7.49"),
    #          │
    #          └── Main Dishes (id=8)
    #              └── Chicken Curry  sku="MEAL-MAIN-001", price=Decimal("12.99"),
    #      
    #      Home (id=8)
    #      │
    #      └── Cleaning Products (id=9)
    #          ├── Dishwashing Liquid   sku="HOME-CLEAN-001", price=Decimal("5.99"),
    #          └── Laundry Detergent    sku="HOME-CLEAN-002", price=Decimal("18.99"),
    #      
    # ---------------------------------------------------------------------------
    def setUp(self):
        # Food hierarchy

        self.food = Category.objects.create(
            name="Food",
        )

        self.fruits_and_vegetables = Category.objects.create(
            name="Fruits and Vegetables",
            parent=self.food,
        )

        self.fruits = Category.objects.create(
            name="Fruits",
            parent=self.fruits_and_vegetables,
        )

        self.vegetables = Category.objects.create(
            name="Vegetables",
            parent=self.fruits_and_vegetables,
        )

        self.dairy_and_eggs = Category.objects.create(
            name="Dairy and Eggs",
            parent=self.food,
        )

        self.ready_meals = Category.objects.create(
            name="Ready Meals",
            parent=self.food,
        )

        self.salads = Category.objects.create(
            name="Salads",
            parent=self.ready_meals,
        )

        self.main_dishes = Category.objects.create(
            name="Main Dishes",
            parent=self.ready_meals,
        )

        # Home hierarchy

        self.home = Category.objects.create(
            name="Home",
        )

        self.cleaning_products = Category.objects.create(
            name="Cleaning Products",
            parent=self.home,
        )

        # Products

        self.bananas = Product.objects.create(
            title="Bananas",
            description="Fresh bananas",
            image="https://example.com/bananas.jpg",
            sku="FRUIT-BANANA-001",
            price=Decimal("2.99"),
            category=self.fruits,
        )

        self.green_apples = Product.objects.create(
            title="Green Apples",
            description="Fresh green apples",
            image="https://example.com/green-apples.jpg",
            sku="FRUIT-APPLE-001",
            price=Decimal("3.49"),
            category=self.fruits,
        )

        self.tomatoes = Product.objects.create(
            title="Tomatoes",
            description="Fresh tomatoes",
            image="https://example.com/tomatoes.jpg",
            sku="VEG-TOMATO-001",
            price=Decimal("4.99"),
            category=self.vegetables,
        )

        self.greek_yogurt = Product.objects.create(
            title="Greek Yogurt",
            description="Natural Greek yogurt",
            image="https://example.com/greek-yogurt.jpg",
            sku="DAIRY-YOGURT-001",
            price=Decimal("2.79"),
            category=self.dairy_and_eggs,
        )

        self.fresh_milk = Product.objects.create(
            title="Fresh Milk",
            description="Fresh cow milk",
            image="https://example.com/fresh-milk.jpg",
            sku="DAIRY-MILK-001",
            price=Decimal("3.19"),
            category=self.dairy_and_eggs,
        )

        self.chicken_caesar_salad = Product.objects.create(
            title="Chicken Caesar Salad",
            description="Caesar salad with grilled chicken",
            image="https://example.com/chicken-caesar-salad.jpg",
            sku="MEAL-SALAD-001",
            price=Decimal("8.99"),
            category=self.salads,
        )

        self.greek_salad = Product.objects.create(
            title="Greek Salad",
            description="Fresh Greek style salad",
            image="https://example.com/greek-salad.jpg",
            sku="MEAL-SALAD-002",
            price=Decimal("7.49"),
            category=self.salads,
        )

        self.chicken_curry = Product.objects.create(
            title="Chicken Curry",
            description="Chicken curry with rice",
            image="https://example.com/chicken-curry.jpg",
            sku="MEAL-MAIN-001",
            price=Decimal("12.99"),
            category=self.main_dishes,
        )

        self.dishwashing_liquid = Product.objects.create(
            title="Dishwashing Liquid",
            description="Dishwashing cleaning product",
            image="https://example.com/dishwashing-liquid.jpg",
            sku="HOME-CLEAN-001",
            price=Decimal("5.99"),
            category=self.cleaning_products,
        )

        self.laundry_detergent = Product.objects.create(
            title="Laundry Detergent",
            description="Laundry cleaning product",
            image="https://example.com/laundry-detergent.jpg",
            sku="HOME-CLEAN-002",
            price=Decimal("18.99"),
            category=self.cleaning_products,
        )

        self.url = "/api/v1/products/"

    # ---------------------------------------------------------------------------
    #    PRODUCTS
    # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    #    ── Chicken Caesar Salad  sku="MEAL-SALAD-001", price=Decimal("8.99")
    #    ── Chicken Curry         sku="MEAL-MAIN-001", price=Decimal("12.99")   
    # ---------------------------------------------------------------------------
    def test_search_by_title_returns_partial_case_insensitive_matches(
        self,
    ):
        response = self.client.get(
            self.url,
            {
                "title": "CHICKEN",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            2,
        )

        returned_skus = {
            product["sku"]
            for product in response.data["results"]
        }

        self.assertEqual(
            returned_skus,
            {
                "MEAL-SALAD-001",
                "MEAL-MAIN-001",
            },
        )

    # ---------------------------------------------------------------------------
    #     Main Dishes (id=8)
    #     └── Chicken Curry  sku="MEAL-MAIN-001", price=Decimal("12.99")
    #              
    #     Salads  (id=7)
    #     └── Chicken Caesar Salad  sku="MEAL-SALAD-001", price=Decimal("8.99"),
    # ---------------------------------------------------------------------------
    def test_search_by_sku_returns_exact_match(self):
        response = self.client.get(
            self.url,
            {
                "sku": "MEAL-SALAD-001",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        product = response.data["results"][0]

        self.assertEqual(
            product["sku"],
            "MEAL-SALAD-001",
        )

        self.assertEqual(
            product["title"],
            "Chicken Caesar Salad",
        )

    # ---------------------------------------------------------------------------
    #     Salads  (id=7)
    #     └── Chicken Caesar Salad  sku="MEAL-SALAD-001", price=Decimal("8.99"),
    #  
    #     Cleaning Products (id=9)
    #     └── Laundry Detergent    sku="HOME-CLEAN-002", price=Decimal("18.99"),
    # ---------------------------------------------------------------------------
    def test_search_by_price_min_returns_products_at_or_above_minimum(
        self,
    ):
        response = self.client.get(
            self.url,
            {
                "price_min": "10",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            2,
        )

        returned_skus = {
            product["sku"]
            for product in response.data["results"]
        }

        self.assertEqual(
            returned_skus,
            {
                "MEAL-MAIN-001",
                "HOME-CLEAN-002",
            },
        )

    # ---------------------------------------------------------------------------
    #      Dairy and Eggs (id=5)
    #      └── Greek Yogurt      sku="DAIRY-YOGURT-001", price=Decimal("2.79")
    #
    #      Fruits (id=3)
    #      └── Bananas       sku="FRUIT-BANANA-001" price=Decimal("2.99"),
    # ---------------------------------------------------------------------------
    def test_search_by_price_max_returns_products_at_or_below_maximum(
        self,
    ):
        response = self.client.get(
            self.url,
            {
                "price_max": "3.00",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            2,
        )

        returned_skus = {
            product["sku"]
            for product in response.data["results"]
        }

        self.assertEqual(
            returned_skus,
            {
                "DAIRY-YOGURT-001",
                "FRUIT-BANANA-001",
            },
        )

    # ---------------------------------------------------------------------------
    #      Dairy and Eggs (id=5)
    #      └──Fresh Milk        sku="DAIRY-MILK-001",   price=Decimal("3.19")
    #
    #      Fruits (id=3)  
    #      └── Green Apples  sku="FRUIT-APPLE-001", price=Decimal("3.49"),
    def test_search_by_price_range_returns_products_within_range(
        self,
    ):
        response = self.client.get(
            self.url,
            {
                "price_min": "3.00",
                "price_max": "6.00",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            4,
        )

        returned_skus = {
            product["sku"]
            for product in response.data["results"]
        }

        self.assertEqual(
            returned_skus,
            {
                "DAIRY-MILK-001",
                "FRUIT-APPLE-001",
                "VEG-TOMATO-001",
                "HOME-CLEAN-001",
            },
        )

    # ---------------------------------------------------------------------------
    #    CATEGORY
    #----------------------------------------------------------------------------

    #----------------------------------------------------------------------------
    #      Fruits (id=3)
    #      ├── Bananas       sku="FRUIT-BANANA-001" price=Decimal("2.99"),
    #      └── Green Apples  sku="FRUIT-APPLE-001", price=Decimal("3.49"),
    def test_search_by_leaf_category_returns_products_in_category(
        self,
    ):
        response = self.client.get(
            self.url,
            {
                "category_id": self.fruits.pk,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            2,
        )

        returned_skus = {
            product["sku"]
            for product in response.data["results"]
        }

        self.assertEqual(
            returned_skus,
            {
                "FRUIT-BANANA-001",
                "FRUIT-APPLE-001",
            },
        )

    #------------------------------------------------------------------------
    #      Fruits and Vegetables
    #      │
    #      ├── Fruits
    #      │   ├── Bananas       sku="FRUIT-BANANA-001" price=Decimal("2.99"),
    #      │   └── Green Apples  sku="FRUIT-APPLE-001", price=Decimal("3.49"),
    #      │
    #      └── Vegetables
    #          └── Tomatoes      sku="VEG-TOMATO-001",  price=Decimal("4.99"),
    def test_search_by_parent_category_returns_products_from_descendants(
        self,
    ):
        response = self.client.get(
            self.url,
            {
                "category_id": self.fruits_and_vegetables.pk,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            3,
        )

        returned_skus = {
            product["sku"]
            for product in response.data["results"]
        }

        self.assertEqual(
            returned_skus,
            {
                "FRUIT-BANANA-001",
                "FRUIT-APPLE-001",
                "VEG-TOMATO-001",
            },
        )        

    # --------------------------------------------------------------------------
    #      [ Food ]
    #        
    #      [+] Fruits
    #      [+] Vegetables
    #      [+] Dairy
    #      [+] Ready Meals
    #       
    #      [-] Cleaning Products
    #      [-] Household products
    def test_search_by_root_category_returns_products_from_all_descendants(
        self,
    ):
        response = self.client.get(
            self.url,
            {
                "category_id": self.food.pk,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            8,
        )

        returned_skus = {
            product["sku"]
            for product in response.data["results"]
        }

        self.assertEqual(
            returned_skus,
            {
                "FRUIT-BANANA-001",
                "FRUIT-APPLE-001",
                "VEG-TOMATO-001",
                "DAIRY-YOGURT-001",
                "DAIRY-MILK-001",
                "MEAL-SALAD-001",
                "MEAL-SALAD-002",
                "MEAL-MAIN-001",
            },
        )

    # ---------------------------------------------------------------------------
    #   COMBINED FILTERS
    #---------------------------------------------------------------------------_

    # ---------------------------------------------------------------------------
    #                    Ready Meals
    #                    ├── Salads
    #                    │   ├── Chicken Caesar Salad  → 8.99
    #                    │   └── Greek Salad           → 7.49
    #                    │
    #                    └── Main Dishes
    #                        └── Chicken Curry         → 12.99
    #
    #          ?category_id=<Ready Meals>&price_min=8&price_max=10
    def test_search_by_category_and_price_range_returns_matching_products(
        self,
    ):
        response = self.client.get(
            self.url,
            {
                "category_id": self.ready_meals.pk,
                "price_min": "8.00",
                "price_max": "10.00",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        product = response.data["results"][0]

        self.assertEqual(
            product["sku"],
            "MEAL-SALAD-001",
        )

        self.assertEqual(
            product["title"],
            "Chicken Caesar Salad",
        )

    # ---------------------------------------------------------------------------   
    #       Ready Meals
    #       ├── Salads
    #       │   ├── Chicken Caesar Salad sku="MEAL-SALAD-001", price=Decimal("8.99")
    #       │    
    #       │
    #       └── Main Dishes
    #           └── Chicken Curry        sku="MEAL-MAIN-001", price=Decimal("12.99"),   
    #     
    #        ?category_id=<Ready Meals>&title=chicken 
    #        "chicken" vs "Chicken Caesar Salad" and "Chicken Curry" 
    def test_search_by_title_and_category_returns_matching_products(
        self,
    ):
        response = self.client.get(
            self.url,
            {
                "title": "chicken",
                "category_id": self.ready_meals.pk,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            2,
        )

        returned_skus = {
            product["sku"]
            for product in response.data["results"]
        }

        self.assertEqual(
            returned_skus,
            {
                "MEAL-SALAD-001",
                "MEAL-MAIN-001",
            },
        )

    # ---------------------------------------------------------------------------
    #   VALIDATION TEST
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    # ?unknown=value
    #---------------------------------------------------------------------------
    def test_search_with_unsupported_query_parameter_returns_bad_request(
        self,
    ):
        response = self.client.get(
            self.url,
            {
                "unknown": "value",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            str(response.data["unknown"]),
            "Unsupported query parameter.",
        )

    #---------------------------------------------------------------------------
    # category_id=abc
    # category_id=0
    # category_id=-1
    #---------------------------------------------------------------------------
    def test_search_with_invalid_category_id_returns_bad_request(
        self,
    ):
        test_cases = {
            "abc": "Must be a valid integer.",
            "0": "Must be a positive integer.",
            "-1": "Must be a positive integer.",
        }

        for category_id, expected_message in test_cases.items():
            with self.subTest(category_id=category_id):
                response = self.client.get(
                    self.url,
                    {
                        "category_id": category_id,
                    },
                )

                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                )

                self.assertEqual(
                    str(response.data["category_id"]),
                    expected_message,
                )

    #---------------------------------------------------------------------------
    # ?price_min=abc 
    # ?price_max=abc 
    #---------------------------------------------------------------------------   
    def test_search_with_invalid_price_returns_bad_request(
        self,
    ):
        test_cases = (
            "price_min",
            "price_max",
        )

        for param in test_cases:
            with self.subTest(param=param):
                response = self.client.get(
                    self.url,
                    {
                        param: "abc",
                    },
                )

                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                )

                self.assertEqual(
                    str(response.data[param]),
                    "Must be a valid decimal number.",
                )
    #---------------------------------------------------------------------------
    # ?price_min=-10
    # ?price_max=-10 
    #---------------------------------------------------------------------------   
    def test_search_with_negative_price_returns_bad_request(
        self,
    ):
        for param in ("price_min", "price_max"):
            with self.subTest(param=param):
                response = self.client.get(
                    self.url,
                    {
                        param: "-10.00",
                    },
                )

                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                )

                self.assertEqual(
                    str(response.data[param]),
                    "Must be greater than or equal to zero.",
                )
    #---------------------------------------------------------------------------
    # ?price_min=10&price_max=5
    #---------------------------------------------------------------------------   
    def test_search_with_invalid_price_range_returns_bad_request(
        self,
    ):
        response = self.client.get(
            self.url,
            {
                "price_min": "10.00",
                "price_max": "5.00",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            str(response.data["price_range"]),
            "price_min cannot be greater than price_max.",
        )

    #---------------------------------------------------------------------------
    # ?category_id=999999
    #---------------------------------------------------------------------------   
    def test_search_with_non_existing_category_returns_bad_request(
        self,
    ):
        response = self.client.get(
            self.url,
            {
                "category_id": "999999",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            str(response.data["category_id"]),
            "Category does not exist.",
        ) 