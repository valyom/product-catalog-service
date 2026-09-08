from django.db import models


class Category(models.Model):
    # not unique -  may have Accessories for Electronics as well as for Furniture
    name = models.CharField(
        max_length=100,
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
    )

    version = models.PositiveIntegerField(
        default=1,
    )
        
    def __str__(self):
        return  f"{self.id} - {self.name}, {self.parent}, {self.version}"
        


class Product(models.Model):
    sku = models.CharField(
        max_length=100,
        unique=True,
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField()

    image = models.URLField(
        max_length=500,
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["category", "price"],
                name="product_category_price_idx",
            ),
        ]

    def __str__(self):
        return f"{self.sku} - {self.title}"