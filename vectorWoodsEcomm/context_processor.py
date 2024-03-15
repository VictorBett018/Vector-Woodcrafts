from vectorWoodsEcomm.models import Product, Category, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address


def default(request):
    categories = Category.objects.all().order_by("-id")
    product = Product.objects.all()

    return {
        'categories':categories,
        'product':product

    }