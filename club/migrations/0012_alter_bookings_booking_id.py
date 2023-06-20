# Generated by Django 4.1.1 on 2023-06-19 11:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("club", "0011_remove_bookings_product_list_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookings",
            name="booking_id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
    ]
