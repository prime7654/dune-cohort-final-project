from django.db import migrations


OLD_SPRING_ROLL_IMAGE = "https://commons.wikimedia.org/wiki/Special:FilePath/DFC_5238-_Freshly_prepared_spring_roll_parcels_arranged_on_a_banana_leaf-lined_plate,_ready_to_enjoy.jpg?width=900"
NEW_SPRING_ROLL_IMAGE = "https://commons.wikimedia.org/wiki/Special:FilePath/Golden_Vegetable_Spring_Rolls_Served_with_Dipping_Sauce.jpg?width=900"


def use_crispy_spring_roll_image(apps, schema_editor):
    MenuItem = apps.get_model("restaurants", "MenuItem")

    MenuItem.objects.filter(name="Spring Rolls").update(
        image_url=NEW_SPRING_ROLL_IMAGE,
    )


def restore_previous_spring_roll_image(apps, schema_editor):
    MenuItem = apps.get_model("restaurants", "MenuItem")

    MenuItem.objects.filter(
        name="Spring Rolls",
        image_url=NEW_SPRING_ROLL_IMAGE,
    ).update(image_url=OLD_SPRING_ROLL_IMAGE)


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0004_replace_with_matching_menu_images"),
    ]

    operations = [
        migrations.RunPython(
            use_crispy_spring_roll_image,
            restore_previous_spring_roll_image,
        ),
    ]
