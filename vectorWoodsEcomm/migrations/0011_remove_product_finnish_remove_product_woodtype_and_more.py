# Generated by Django 5.0.2 on 2024-03-10 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vectorWoodsEcomm', '0010_remove_cartorder_dimension_remove_cartorder_finish_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='finnish',
        ),
        migrations.RemoveField(
            model_name='product',
            name='woodtype',
        ),
        migrations.AddField(
            model_name='product',
            name='color1',
            field=models.CharField(default='Brown', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='color2',
            field=models.CharField(default='White', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='color3',
            field=models.CharField(default='Gray', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='color4',
            field=models.CharField(default='Black', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='woodtype1',
            field=models.CharField(default='Mahogany', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='woodtype2',
            field=models.CharField(default='Oak', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='woodtype3',
            field=models.CharField(default='Maple', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='woodtype4',
            field=models.CharField(default='Cherry', max_length=100, null=True),
        ),
    ]
