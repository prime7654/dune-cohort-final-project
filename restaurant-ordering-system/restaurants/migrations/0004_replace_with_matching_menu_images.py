from django.db import migrations


MATCHING_MENU_IMAGES = {
    "Jollof Rice": "https://commons.wikimedia.org/wiki/Special:FilePath/Jollof_rice_and_fried_chicken.jpg?width=900",
    "Pepper Soup": "https://commons.wikimedia.org/wiki/Special:FilePath/Assorted_meat_pepper_soup_at_Lagos_Island.jpg?width=900",
    "Spring Rolls": "https://commons.wikimedia.org/wiki/Special:FilePath/DFC_5238-_Freshly_prepared_spring_roll_parcels_arranged_on_a_banana_leaf-lined_plate,_ready_to_enjoy.jpg?width=900",
    "Fried Rice and Chicken": "https://commons.wikimedia.org/wiki/Special:FilePath/Fried_Rice_and_Chicken.jpg?width=900",
    "Pounded Yam and Egusi": "https://commons.wikimedia.org/wiki/Special:FilePath/Egusi_soup_with_pounded_yam_and_assorted_meats.jpg?width=900",
    "Suya Platter": "https://commons.wikimedia.org/wiki/Special:FilePath/Nigerian_home_made_suya_and_sliced_onions.png?width=900",
    "Grilled Fish": "https://commons.wikimedia.org/wiki/Special:FilePath/Roasted_plantain_with_fish.jpg?width=900",
    "Chapman": "https://commons.wikimedia.org/wiki/Special:FilePath/Chapman_drink.jpg?width=900",
    "Zobo Drink": "https://commons.wikimedia.org/wiki/Special:FilePath/Zobo_drink.jpg?width=900",
}


def replace_menu_images(apps, schema_editor):
    MenuItem = apps.get_model("restaurants", "MenuItem")

    for item_name, image_url in MATCHING_MENU_IMAGES.items():
        MenuItem.objects.filter(name=item_name).update(image_url=image_url)


def clear_matching_menu_images(apps, schema_editor):
    MenuItem = apps.get_model("restaurants", "MenuItem")

    MenuItem.objects.filter(
        name__in=MATCHING_MENU_IMAGES.keys(),
        image_url__in=MATCHING_MENU_IMAGES.values(),
    ).update(image_url="")


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0003_add_menu_images"),
    ]

    operations = [
        migrations.RunPython(replace_menu_images, clear_matching_menu_images),
    ]
