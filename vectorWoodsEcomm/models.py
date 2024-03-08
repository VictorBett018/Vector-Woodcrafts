from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager




STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

DIMENSION = (
    ("dim1", "(L x W x H) 4 x 5 x 6"),
    ("dim2", "(L x W x H) 4 x 5 x 6"),
)
FINISH = (
    ("white", "White"),
    ("black", "Black"),
    ("red", "Red"),
)
RATING = (
    (1, "⭐✰✰✰✰"),
    (2, "⭐⭐✰✰✰"),
    (3, "⭐⭐⭐✰✰"),
    (4, "⭐⭐⭐⭐✰"),
    (5, "⭐⭐⭐⭐⭐"),
)


# Create your models here.
class Category(models.Model):
    cid = ShortUUIDField(unique=True,length = 10, max_length = 20, prefix = "cat", alphabet = "abcdef12345")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width ="50" heght ="50"/>' % (self.image.url))

    def __str__(self):
        return self.title

class Product(models.Model):
    pid = ShortUUIDField(unique=True,length = 10, max_length = 20, alphabet = "abcdefghijk123456789")
    title = models.CharField(max_length=100)  

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    image = models.ImageField(upload_to = "products")
    description = models.TextField(null=True, blank=True, default="This is the product")


    product_status = models.CharField(choices=STATUS_CHOICE,max_length=30, default="processing")
    price = models.DecimalField(max_digits=999999, decimal_places=2, default="99.99")
    old_price = models.DecimalField(max_digits=999999, decimal_places=2, default="199.99")
    tags = TaggableManager(blank=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)
    sku = ShortUUIDField(unique=True,length = 10, max_length = 20,prefix="sku", alphabet = "0123456789")
    date = models.DateField(auto_now_add=True)
    updated = models.DateField(null=True, blank= True)
    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width ="50" heght ="50" />' % (self.image.url))

    def __str__(self):
        return self.title 

    def get_percentage(self):
        new_price = ((self.old_price-self.price)/self.price) * 100
        return new_price

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images")
    product = models.ForeignKey(Product, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product images"

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dimension = models.CharField(choices=DIMENSION,max_length=30, default="dim1")
    finish = models.CharField(choices=FINISH,max_length=30, default="black")
    price = models.DecimalField(max_digits=999999, decimal_places=2, default="99.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE,max_length=30, default="processing")

    class Meta:
        verbose_name_plural = "Product images"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    product_status = models.CharField(max_length=200)
    invoice_no = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    img = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=999999, decimal_places=2, default="99.99")
    total = models.DecimalField(max_digits=999999, decimal_places=2, default="99.99")
    
    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_img(self):
        return mark_safe('<img src="/media/%s" width ="50" heght ="50" />' % (self.image))



class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateField(auto_now_add=True)

    
    class Meta:
        verbose_name_plural = "Product Reviews"
    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating   



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)

    date = models.DateField(auto_now_add=True)

    
    class Meta:
        verbose_name_plural = "Wishlist"
    def __str__(self):
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"




      


