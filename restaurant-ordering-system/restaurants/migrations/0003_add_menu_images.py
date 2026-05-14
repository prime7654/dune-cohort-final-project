from django.db import migrations


MENU_IMAGES = {
    "Jollof Rice": "https://images.unsplash.com/photo-1604329760661-e71dc83f8f26?auto=format&fit=crop&w=900&q=80",
    "Pepper Soup": "https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=900&q=80",
    "Spring Rolls": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=900&q=80",
    "Fried Rice and Chicken": "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=900&q=80",
    "Pounded Yam and Egusi": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=900&q=80",
    "Suya Platter": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=900&q=80",
    "Grilled Fish": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=900&q=80",
    "Chapman": "https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=900&q=80",
    "Zobo Drink": "https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=900&q=80",
}


def add_menu_images(apps, schema_editor):
    MenuItem = apps.get_model("restaurants", "MenuItem")

    for item_name, image_url in MENU_IMAGES.items():
        MenuItem.objects.filter(name=item_name).update(image_url=image_url)


def remove_menu_images(apps, schema_editor):
    MenuItem = apps.get_model("restaurants", "MenuItem")

    MenuItem.objects.filter(
        name__in=MENU_IMAGES.keys(),
        image_url__in=MENU_IMAGES.values(),
    ).update(image_url="")


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0002_seed_menu_data"),
    ]

    operations = [
        migrations.RunPython(add_menu_images, remove_menu_images),
    ]
