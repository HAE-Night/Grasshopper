# Generated by Django 4.1 on 2024-01-23 03:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Products", "0002_alter_products_item_photo"),
    ]

    operations = [
        migrations.RenameField(
            model_name="products",
            old_name="Id",
            new_name="ID",
        ),
        migrations.RenameField(
            model_name="products",
            old_name="Description",
            new_name="ITEM",
        ),
        migrations.RemoveField(
            model_name="products",
            name="Height",
        ),
        migrations.RemoveField(
            model_name="products",
            name="Item",
        ),
        migrations.RemoveField(
            model_name="products",
            name="Item_Photo",
        ),
        migrations.RemoveField(
            model_name="products",
            name="Length",
        ),
        migrations.RemoveField(
            model_name="products",
            name="Link",
        ),
        migrations.RemoveField(
            model_name="products",
            name="Unit",
        ),
        migrations.RemoveField(
            model_name="products",
            name="Unit_Price",
        ),
        migrations.RemoveField(
            model_name="products",
            name="Width",
        ),
        migrations.AddField(
            model_name="products",
            name="DESCRIPTION",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="products",
            name="HAE_COST_AED",
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name="products",
            name="HIGHT_MM",
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name="products",
            name="LENGTH_MM",
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name="products",
            name="PRICE_STRATEGY",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="products",
            name="WIDTH_MM",
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name="products",
            name="QTY",
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AddField(
            model_name="products",
            name="ITEM_PHOTO",
            field=models.ImageField(null=True, upload_to="static/Photos/"),
        ),
        migrations.AddField(
            model_name="products",
            name="LINK",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="products",
            name="UNIT",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
