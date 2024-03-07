from django.shortcuts import render
from vectorWoodsEcomm.models import Product, Category, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address
from taggit.models import Tag
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
    categories = Category.objects.all()
    products = Product.objects.filter(featured=True)

    context = {
            "categories" : categories,
            "products":products
    }
    return render(request, 'index.html', context)


def products_view(request):

    categories = Category.objects.all()
    products = Product.objects.all().order_by("-id")

    context = {
        "categories" : categories ,
        "products" : products,
        
    }


    return render(request, 'products.html', context)

def category_view(request, cid):
    category = Category.objects.get(cid = cid)
    products = Product.objects.filter(category=category)

    context = {
            "category" : category ,
            "products" : products
                }
    return render(request, 'category.html', context)

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    p_image = product.p_images.all()

    context = {
        "product" : product,
        "p_image" : p_image,
        "products": products,
    }
    return render(request, 'product_details.html', context)
def tag_list(request, tag_slug=None):
    products = Product.objects.all().order_by("-id")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags = tag) 
    context={
        "products":products
    }

    return render(request, 'tag.html', context)

def contact_view(request):
    return render(request, 'contact.html')

def about_view(request):
    return render(request, 'about.html')