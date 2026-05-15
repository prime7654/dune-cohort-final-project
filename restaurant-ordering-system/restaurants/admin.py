from django.contrib import admin

from .models import MenuCategory, MenuItem


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "stock", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "category__name")
    actions = ("mark_as_out_of_stock",)

    @admin.action(description="Mark as out of stock")
    def mark_as_out_of_stock(self, request, queryset):
        updated_count = queryset.update(stock=0, is_available=False)
        self.message_user(
            request,
            f"{updated_count} menu item(s) marked as out of stock.",
        )
