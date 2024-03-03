from django.shortcuts import render
from vectorWoodsEcomm.models import Product, Category, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address


# Create your views here.
def index(request):
    return render(request, 'index.html')

def products_view(request):
    products = Product.objects.filter(featured=True).order_by("-id")

    context = {
        "products" : products
    }


    return render(request, 'products.html', context)