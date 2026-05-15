from django.db import models


class MenuCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "menu categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(
        MenuCategory,
        on_delete=models.CASCADE,
        related_name="menu_items",
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=10)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="menu_items/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category__name", "name"]
        constraints = [
            # The same item name can exist in different categories, but not twice in one.
            models.UniqueConstraint(
                fields=["category", "name"],
                name="unique_menu_item_per_category",
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.price}"

    @property
    def image_src(self):
        if self.image:
            return self.image.url
        return ""
