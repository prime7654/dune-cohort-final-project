from django.db import migrations, models


MENU_ITEM_IMAGES = {
    "Jollof Rice": "menu_items/jollof_rice.jpg",
    "Pepper Soup": "menu_items/pepper_soup.jpg",
    "Spring Rolls": "menu_items/spring_rolls.jpg",
    "Fried Rice and Chicken": "menu_items/fried_rice_and_chicken.jpg",
    "Pounded Yam and Egusi": "menu_items/pounded_yam_and_egusi.jpg",
    "Suya Platter": "menu_items/suya_platter.png",
    "Grilled Fish": "menu_items/grilled_fish.jpg",
    "Chapman": "menu_items/chapman.jpg",
    "Zobo Drink": "menu_items/zobo_drink.jpg",
}


def migrate_seeded_images_to_imagefield(apps, schema_editor):
    MenuItem = apps.get_model("restaurants", "MenuItem")

    for item_name, image_path in MENU_ITEM_IMAGES.items():
        MenuItem.objects.filter(name=item_name).update(image=image_path)


def clear_seeded_images(apps, schema_editor):
    MenuItem = apps.get_model("restaurants", "MenuItem")

    for item_name, image_path in MENU_ITEM_IMAGES.items():
        MenuItem.objects.filter(name=item_name, image=image_path).update(image="")


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0006_menuitem_image_menuitem_stock"),
    ]

    operations = [
        migrations.RunPython(
            migrate_seeded_images_to_imagefield,
            clear_seeded_images,
        ),
        migrations.RemoveField(
            model_name="menuitem",
            name="image_url",
        ),
        migrations.AlterField(
            model_name="menuitem",
            name="image",
            field=models.ImageField(blank=True, upload_to="menu_items/"),
        ),
    ]
