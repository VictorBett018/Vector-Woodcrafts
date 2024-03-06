from vectorWoodsEcomm.models import Product, Category, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address


def default(request):
    categories = Category.objects.all()
    return {
        'categories':categories
    }