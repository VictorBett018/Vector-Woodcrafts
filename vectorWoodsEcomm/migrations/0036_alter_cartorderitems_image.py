# Generated by Django 5.0.2 on 2024-05-23 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vectorWoodsEcomm', '0035_rename_img_cartorderitems_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorderitems',
            name='image',
            field=models.ImageField(upload_to='order-images'),
        ),
    ]
