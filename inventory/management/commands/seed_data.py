from decimal import Decimal

from django.core.management.base import BaseCommand

from inventory.models import Category, Product


class Command(BaseCommand):

    help = (
        "Seeds the database with sample categories "
        "and products."
    )

    def handle(self, *args, **options):

        self.stdout.write(
            "Creating sample categories..."
        )

        # ============================================================
        # Food hierarchy
        # ============================================================

        food, _ = Category.objects.get_or_create(
            name="Food",
            parent=None,
        )

        fruits_and_vegetables, _ = (
            Category.objects.get_or_create(
                name="Fruits and Vegetables",
                parent=food,
            )
        )

        fruits, _ = Category.objects.get_or_create(
            name="Fruits",
            parent=fruits_and_vegetables,
        )

        vegetables, _ = Category.objects.get_or_create(
            name="Vegetables",
            parent=fruits_and_vegetables,
        )

        dairy_and_eggs, _ = (
            Category.objects.get_or_create(
                name="Dairy and Eggs",
                parent=food,
            )
        )

        ready_meals, _ = Category.objects.get_or_create(
            name="Ready Meals",
            parent=food,
        )

        salads, _ = Category.objects.get_or_create(
            name="Salads",
            parent=ready_meals,
        )

        main_dishes, _ = Category.objects.get_or_create(
            name="Main Dishes",
            parent=ready_meals,
        )

        # ============================================================
        # Home hierarchy
        # ============================================================

        home, _ = Category.objects.get_or_create(
            name="Home",
            parent=None,
        )

        cleaning_products, _ = (
            Category.objects.get_or_create(
                name="Cleaning Products",
                parent=home,
            )
        )

        # ============================================================
        # Test products
        # Same data used by product search tests
        # ============================================================

        products = [

            {
                "title": "Bananas",
                "description": "Fresh bananas",
                "image": (
                    "https://example.com/bananas.jpg"
                ),
                "sku": "FRUIT-BANANA-001",
                "price": Decimal("2.99"),
                "category": fruits,
            },

            {
                "title": "Green Apples",
                "description": "Fresh green apples",
                "image": (
                    "https://example.com/green-apples.jpg"
                ),
                "sku": "FRUIT-APPLE-001",
                "price": Decimal("3.49"),
                "category": fruits,
            },

            {
                "title": "Tomatoes",
                "description": "Fresh tomatoes",
                "image": (
                    "https://example.com/tomatoes.jpg"
                ),
                "sku": "VEG-TOMATO-001",
                "price": Decimal("4.99"),
                "category": vegetables,
            },

            {
                "title": "Greek Yogurt",
                "description": "Natural Greek yogurt",
                "image": (
                    "https://example.com/greek-yogurt.jpg"
                ),
                "sku": "DAIRY-YOGURT-001",
                "price": Decimal("2.79"),
                "category": dairy_and_eggs,
            },

            {
                "title": "Fresh Milk",
                "description": "Fresh cow milk",
                "image": (
                    "https://example.com/fresh-milk.jpg"
                ),
                "sku": "DAIRY-MILK-001",
                "price": Decimal("3.19"),
                "category": dairy_and_eggs,
            },

            {
                "title": "Chicken Caesar Salad",
                "description": (
                    "Caesar salad with grilled chicken"
                ),
                "image": (
                    "https://example.com/"
                    "chicken-caesar-salad.jpg"
                ),
                "sku": "MEAL-SALAD-001",
                "price": Decimal("8.99"),
                "category": salads,
            },

            {
                "title": "Greek Salad",
                "description": "Fresh Greek style salad",
                "image": (
                    "https://example.com/greek-salad.jpg"
                ),
                "sku": "MEAL-SALAD-002",
                "price": Decimal("7.49"),
                "category": salads,
            },

            {
                "title": "Chicken Curry",
                "description": (
                    "Chicken curry with rice"
                ),
                "image": (
                    "https://example.com/chicken-curry.jpg"
                ),
                "sku": "MEAL-MAIN-001",
                "price": Decimal("12.99"),
                "category": main_dishes,
            },

            {
                "title": "Dishwashing Liquid",
                "description": (
                    "Dishwashing cleaning product"
                ),
                "image": (
                    "https://example.com/"
                    "dishwashing-liquid.jpg"
                ),
                "sku": "HOME-CLEAN-001",
                "price": Decimal("5.99"),
                "category": cleaning_products,
            },

            {
                "title": "Laundry Detergent",
                "description": (
                    "Laundry cleaning product"
                ),
                "image": (
                    "https://example.com/"
                    "laundry-detergent.jpg"
                ),
                "sku": "HOME-CLEAN-002",
                "price": Decimal("18.99"),
                "category": cleaning_products,
            },

        ]

        # ============================================================
        # Additional products for pagination demonstration
        # ============================================================

        additional_products = [

            {
                "title": "Red Apples",
                "description": "Fresh red apples",
                "sku": "FRUIT-APPLE-002",
                "price": Decimal("3.29"),
                "category": fruits,
            },

            {
                "title": "Oranges",
                "description": "Fresh oranges",
                "sku": "FRUIT-ORANGE-001",
                "price": Decimal("3.99"),
                "category": fruits,
            },

            {
                "title": "Strawberries",
                "description": "Fresh strawberries",
                "sku": "FRUIT-STRAWBERRY-001",
                "price": Decimal("5.49"),
                "category": fruits,
            },

            {
                "title": "Blueberries",
                "description": "Fresh blueberries",
                "sku": "FRUIT-BLUEBERRY-001",
                "price": Decimal("6.99"),
                "category": fruits,
            },

            {
                "title": "Carrots",
                "description": "Fresh carrots",
                "sku": "VEG-CARROT-001",
                "price": Decimal("2.49"),
                "category": vegetables,
            },

            {
                "title": "Potatoes",
                "description": "Fresh potatoes",
                "sku": "VEG-POTATO-001",
                "price": Decimal("1.99"),
                "category": vegetables,
            },

            {
                "title": "Cucumbers",
                "description": "Fresh cucumbers",
                "sku": "VEG-CUCUMBER-001",
                "price": Decimal("3.19"),
                "category": vegetables,
            },

            {
                "title": "Red Peppers",
                "description": "Fresh red peppers",
                "sku": "VEG-PEPPER-001",
                "price": Decimal("4.49"),
                "category": vegetables,
            },

            {
                "title": "Free Range Eggs",
                "description": "Free range chicken eggs",
                "sku": "DAIRY-EGG-001",
                "price": Decimal("4.99"),
                "category": dairy_and_eggs,
            },

            {
                "title": "Cheddar Cheese",
                "description": "Mature cheddar cheese",
                "sku": "DAIRY-CHEESE-001",
                "price": Decimal("7.99"),
                "category": dairy_and_eggs,
            },

            {
                "title": "Mozzarella",
                "description": "Fresh mozzarella cheese",
                "sku": "DAIRY-CHEESE-002",
                "price": Decimal("6.49"),
                "category": dairy_and_eggs,
            },

            {
                "title": "Spaghetti Bolognese",
                "description": "Spaghetti with beef sauce",
                "sku": "MEAL-MAIN-002",
                "price": Decimal("10.99"),
                "category": main_dishes,
            },

            {
                "title": "Grilled Chicken",
                "description": "Grilled chicken with vegetables",
                "sku": "MEAL-MAIN-003",
                "price": Decimal("11.99"),
                "category": main_dishes,
            },

            {
                "title": "Vegetable Lasagna",
                "description": "Lasagna with vegetables",
                "sku": "MEAL-MAIN-004",
                "price": Decimal("9.99"),
                "category": main_dishes,
            },

            {
                "title": "Tuna Salad",
                "description": "Fresh salad with tuna",
                "sku": "MEAL-SALAD-003",
                "price": Decimal("8.49"),
                "category": salads,
            },

            {
                "title": "Garden Salad",
                "description": "Fresh mixed vegetable salad",
                "sku": "MEAL-SALAD-004",
                "price": Decimal("6.99"),
                "category": salads,
            },

            {
                "title": "Bathroom Cleaner",
                "description": "Bathroom cleaning product",
                "sku": "HOME-CLEAN-003",
                "price": Decimal("6.49"),
                "category": cleaning_products,
            },

            {
                "title": "Glass Cleaner",
                "description": "Glass cleaning product",
                "sku": "HOME-CLEAN-004",
                "price": Decimal("4.99"),
                "category": cleaning_products,
            },

            {
                "title": "Floor Cleaner",
                "description": "Floor cleaning product",
                "sku": "HOME-CLEAN-005",
                "price": Decimal("7.99"),
                "category": cleaning_products,
            },

            {
                "title": "Kitchen Cleaner",
                "description": "Kitchen cleaning product",
                "sku": "HOME-CLEAN-006",
                "price": Decimal("5.49"),
                "category": cleaning_products,
            },

            {
                "title": "Multi Surface Cleaner",
                "description": "Multi surface cleaning product",
                "sku": "HOME-CLEAN-007",
                "price": Decimal("6.99"),
                "category": cleaning_products,
            },

            {
                "title": "Hand Soap",
                "description": "Liquid hand soap",
                "sku": "HOME-CLEAN-008",
                "price": Decimal("3.99"),
                "category": cleaning_products,
            },

            {
                "title": "Paper Towels",
                "description": "Kitchen paper towels",
                "sku": "HOME-CLEAN-009",
                "price": Decimal("4.49"),
                "category": cleaning_products,
            },

            {
                "title": "Laundry Softener",
                "description": "Fabric softener",
                "sku": "HOME-CLEAN-010",
                "price": Decimal("8.99"),
                "category": cleaning_products,
            },

        ]

        products.extend(additional_products)

        self.stdout.write(
            "Creating sample products..."
        )

        created_count = 0

        for product_data in products:

            product_data.setdefault(
                "image",
                "https://example.com/product.jpg",
            )

            product, created = Product.objects.get_or_create(
                sku=product_data["sku"],
                defaults=product_data,
            )

            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Database seeded successfully. "
                f"Created {created_count} products."
            )
        )