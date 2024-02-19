from django.db import models


# Create your models here.
class Products(models.Model):
    ID = models.AutoField(primary_key=True)
    CATEGORY = models.CharField(max_length=200, null=True)
    ROOM_AREA = models.CharField(max_length=200, null=True)
    ITEM = models.CharField(max_length=200, null=True)
    ITEM_PHOTO = models.ImageField(upload_to='static/Photos/', null=True)
    DESCRIPTION = models.CharField(max_length=200, null=True)
    SIZE_DIMENSION = models.CharField(max_length=200, null=True)
    LENGTH_MM = models.CharField(max_length=200, null=True)
    WIDTH_MM = models.CharField(max_length=200, null=True)
    HEIGHT_MM = models.CharField(max_length=200, null=True)
    QTY = models.CharField(max_length=200, null=True)
    UNIT = models.CharField(max_length=200, null=True)
    UNIT_PRICE_AED = models.CharField(max_length=200, null=True)
    INQUIRY_CODE = models.CharField(max_length=200, null=True)


# 购物车
