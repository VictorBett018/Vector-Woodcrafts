# Generated by Django 5.0.2 on 2024-04-18 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vectorWoodsEcomm', '0023_alter_blogpost_list15'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='list15',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
