from rest_framework import serializers

from .models import MenuCategory, MenuItem


class MenuCategoryBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ["id", "name", "description"]


class MenuItemSerializer(serializers.ModelSerializer):
    menu_category = MenuCategoryBriefSerializer(source="category", read_only=True)
    menu_category_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuCategory.objects.all(),
        source="category",
        write_only=True,
    )

    class Meta:
        model = MenuItem
        fields = [
            "id",
            "menu_category",
            "menu_category_id",
            "name",
            "description",
            "price",
            "stock",
            "is_available",
            "image",
            "created_at",
        ]
        read_only_fields = ["id", "menu_category", "created_at"]


class MenuCategorySerializer(serializers.ModelSerializer):
    menu_item_count = serializers.SerializerMethodField()
    menu_items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = MenuCategory
        fields = ["id", "name", "description", "menu_item_count", "menu_items"]

    def get_menu_item_count(self, obj):
        if hasattr(obj, "menu_item_count"):
            return obj.menu_item_count
        return obj.menu_items.count()
