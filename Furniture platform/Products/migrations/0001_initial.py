# Generated by Django 4.1 on 2024-01-22 07:41

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Products",
            fields=[
                ("Id", models.AutoField(primary_key=True, serialize=False)),
                ("Item", models.CharField(max_length=200)),
                ("Item_Photo", models.CharField(max_length=200)),
                ("Description", models.CharField(max_length=200)),
                ("Length", models.DecimalField(decimal_places=2, max_digits=5)),
                ("Width", models.DecimalField(decimal_places=2, max_digits=5)),
                ("Height", models.DecimalField(decimal_places=2, max_digits=5)),
                ("QTY", models.IntegerField(default=1)),
                ("Unit", models.CharField(max_length=200)),
                ("Link", models.CharField(max_length=200)),
                ("Unit_Price", models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
