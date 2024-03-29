# Generated by Django 5.0.2 on 2024-03-02 11:32

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vectorWoodsEcomm', '0004_productimage_remove_address_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Products'},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='product',
            name='finish',
        ),
        migrations.RemoveField(
            model_name='product',
            name='name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='woodtype',
        ),
        migrations.AddField(
            model_name='category',
            name='cid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdef12345', length=10, max_length=20, prefix='cat', unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=100, upload_to='category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='product', to='vectorWoodsEcomm.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='featured',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default=True, upload_to='products'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='in_stock',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='pid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijk123456789', length=10, max_length=20, prefix='', unique=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='processing', max_length=30),
        ),
        migrations.AddField(
            model_name='product',
            name='sku',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='0123456789', length=10, max_length=20, prefix='sku', unique=True),
        ),
        migrations.AddField(
            model_name='product',
            name='title',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='updated',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, default='This is the product', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(decimal_places=2, default='199.99', max_digits=999999),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default='99.99', max_digits=999999),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Address',
            },
        ),
        migrations.CreateModel(
            name='CartOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dimension', models.CharField(choices=[('dim1', '(L x W x H) 4 x 5 x 6'), ('dim2', '(L x W x H) 4 x 5 x 6')], default='dim1', max_length=30)),
                ('finish', models.CharField(choices=[('white', 'White'), ('black', 'Black'), ('red', 'Red')], default='black', max_length=30)),
                ('price', models.DecimalField(decimal_places=2, default='99.99', max_digits=999999)),
                ('paid_status', models.BooleanField(default=False)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('product_status', models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='processing', max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Product images',
            },
        ),
        migrations.CreateModel(
            name='CartOrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_status', models.CharField(max_length=200)),
                ('invoice_no', models.CharField(max_length=200)),
                ('item', models.CharField(max_length=200)),
                ('img', models.CharField(max_length=200)),
                ('qty', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default='99.99', max_digits=999999)),
                ('total', models.DecimalField(decimal_places=2, default='99.99', max_digits=999999)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vectorWoodsEcomm.cartorder')),
            ],
            options={
                'verbose_name_plural': 'Cart Order Items',
            },
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to='product-images')),
                ('date', models.DateField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vectorWoodsEcomm.product')),
            ],
            options={
                'verbose_name_plural': 'Product images',
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('rating', models.IntegerField(choices=[(1, '⭐✰✰✰✰'), (2, '⭐⭐✰✰✰'), (3, '⭐⭐⭐✰✰'), (4, '⭐⭐⭐⭐✰'), (5, '⭐⭐⭐⭐⭐')], default=None)),
                ('date', models.DateField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vectorWoodsEcomm.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Product Reviews',
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vectorWoodsEcomm.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Wishlist',
            },
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
