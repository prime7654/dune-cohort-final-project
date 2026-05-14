from decimal import Decimal

from django.db import migrations


MENU_DATA = [
    {
        "name": "Starters",
        "description": "Small bites and light plates to begin a meal.",
        "items": [
            {
                "name": "Pepper Soup",
                "description": "Spicy broth with tender meat and local herbs.",
                "price": Decimal("1800.00"),
                "is_available": True,
            },
            {
                "name": "Spring Rolls",
                "description": "Crispy rolls served with sweet chilli sauce.",
                "price": Decimal("1200.00"),
                "is_available": True,
            },
        ],
    },
    {
        "name": "Main Meals",
        "description": "Filling plates for lunch, dinner, and family orders.",
        "items": [
            {
                "name": "Fried Rice and Chicken",
                "description": "Vegetable fried rice served with seasoned chicken.",
                "price": Decimal("3500.00"),
                "is_available": True,
            },
            {
                "name": "Pounded Yam and Egusi",
                "description": "Smooth pounded yam with rich egusi soup.",
                "price": Decimal("4000.00"),
                "is_available": True,
            },
        ],
    },
    {
        "name": "Grills",
        "description": "Freshly grilled meals served hot from the kitchen.",
        "items": [
            {
                "name": "Suya Platter",
                "description": "Spiced beef suya with onions, cabbage, and pepper.",
                "price": Decimal("3000.00"),
                "is_available": True,
            },
            {
                "name": "Grilled Fish",
                "description": "Whole grilled fish served with plantain and sauce.",
                "price": Decimal("5500.00"),
                "is_available": False,
            },
        ],
    },
    {
        "name": "Drinks",
        "description": "Cold drinks and house refreshments.",
        "items": [
            {
                "name": "Chapman",
                "description": "Classic Nigerian mocktail served chilled.",
                "price": Decimal("1500.00"),
                "is_available": True,
            },
            {
                "name": "Zobo Drink",
                "description": "Refreshing hibiscus drink with ginger and pineapple.",
                "price": Decimal("800.00"),
                "is_available": True,
            },
        ],
    },
]


def seed_menu_data(apps, schema_editor):
    MenuCategory = apps.get_model("restaurants", "MenuCategory")
    MenuItem = apps.get_model("restaurants", "MenuItem")

    for category_data in MENU_DATA:
        category, _ = MenuCategory.objects.update_or_create(
            name=category_data["name"],
            defaults={"description": category_data["description"]},
        )
        for item_data in category_data["items"]:
            MenuItem.objects.update_or_create(
                category=category,
                name=item_data["name"],
                defaults={
                    "description": item_data["description"],
                    "price": item_data["price"],
                    "is_available": item_data["is_available"],
                },
            )


def remove_menu_data(apps, schema_editor):
    MenuCategory = apps.get_model("restaurants", "MenuCategory")
    MenuItem = apps.get_model("restaurants", "MenuItem")

    category_names = [category["name"] for category in MENU_DATA]
    item_names = [
        item["name"]
        for category in MENU_DATA
        for item in category["items"]
    ]

    MenuItem.objects.filter(
        category__name__in=category_names,
        name__in=item_names,
    ).delete()
    MenuCategory.objects.filter(
        name__in=category_names,
        menu_items__isnull=True,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_menu_data, remove_menu_data),
    ]
