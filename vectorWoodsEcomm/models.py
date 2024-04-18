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
    dim1 = models.CharField(max_length=100, null = True, default="L * W * H")
    dim2 = models.CharField(max_length=100, null = True, default="L * W * H")
    color1 = models.CharField(max_length=100, null = True, default="Brown")
    color2 = models.CharField(max_length=100, null = True, default="White")
    color3 = models.CharField(max_length=100, null = True, default="Gray")
    color4 = models.CharField(max_length=100, null = True, default="Black")
    woodtype1 = models.CharField(max_length=100, null = True, default="Mahogany")
    woodtype2 = models.CharField(max_length=100, null = True, default="Mango")
    woodtype3 = models.CharField(max_length=100, null = True, default="Teak")
    woodtype4 = models.CharField(max_length=100, null = True, default="Cypress")

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
    price = models.DecimalField(max_digits=999999, decimal_places=2,)
    total = models.DecimalField(max_digits=999999, decimal_places=2,)
    
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
        

class BlogPost(models.Model):
    bid = ShortUUIDField(unique=True,length = 10, max_length = 20, alphabet = "abcdefghijk123456789")
    title = models.CharField(max_length=200)
    introduction = models.TextField()
    heading1 = models.CharField(max_length=200, null=True,blank=True)
    para1 = models.TextField(null=True,blank=True)
    subheading1 = models.CharField(max_length=200, null=True,blank=True)
    list11 = models.CharField(max_length=500,null=True,blank=True)
    list12 = models.CharField(max_length=500,null=True,blank=True)
    list13 = models.CharField(max_length=500,null=True,blank=True)
    list14 = models.CharField(max_length=500,null=True,blank=True)
    list15 = models.CharField(max_length=500,null=True,blank=True)
    heading2 = models.CharField(max_length=200, null=True,blank=True)
    para2 = models.TextField(null=True,blank=True)
    subheading2 = models.CharField(max_length=200, null=True,blank=True)
    list21 = models.CharField(max_length=500,null=True,blank=True)
    list22 = models.CharField(max_length=500,null=True,blank=True)
    list23 = models.CharField(max_length=500,null=True,blank=True)
    list24 = models.CharField(max_length=500,null=True,blank=True)
    list25 = models.CharField(max_length=500,null=True,blank=True)
    heading3 = models.CharField(max_length=200, null=True,blank=True)
    para3 = models.TextField(null=True,blank=True)
    subheading3 = models.CharField(max_length=200, null=True,blank=True)
    list31 = models.CharField(max_length=500,null=True,blank=True)
    list32 = models.CharField(max_length=500,null=True,blank=True)
    list33 = models.CharField(max_length=500,null=True,blank=True)
    list34 = models.CharField(max_length=500,null=True,blank=True)
    list35 = models.CharField(max_length=500,null=True,blank=True)
    heading4 = models.CharField(max_length=200, null=True, blank=True)
    para4 = models.TextField(null=True,blank=True)
    subheading4 = models.CharField(max_length=200, null=True,blank=True)
    list41 = models.CharField(max_length=500,null=True,blank=True)
    list42 = models.CharField(max_length=500,null=True,blank=True)
    list43 = models.CharField(max_length=500,null=True,blank=True)
    list44 = models.CharField(max_length=500,null=True,blank=True)
    list45 = models.CharField(max_length=500,null=True,blank=True)
    heading5 = models.CharField(max_length=200, null=True,blank=True)   
    para5 = models.TextField(null=True,blank=True)
    subheading5 = models.CharField(max_length=200, null=True,blank=True)
    list51 = models.CharField(max_length=500,null=True,blank=True)
    list52 = models.CharField(max_length=500,null=True,blank=True)
    list53 = models.CharField(max_length=500,null=True,blank=True)
    list54 = models.CharField(max_length=500,null=True,blank=True)
    list55 = models.CharField(max_length=500,null=True,blank=True)
    conclusion_title = models.CharField(max_length=200,null=True,blank=True)
    conclusion = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='blog_images/')
    published_date = models.DateField()

    def __str__(self):
        return self.title
