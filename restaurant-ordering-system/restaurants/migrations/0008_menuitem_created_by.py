from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("restaurants", "0007_migrate_image_urls_to_imagefield"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_menu_items",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
