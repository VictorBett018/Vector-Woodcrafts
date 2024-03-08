from django.shortcuts import render
from vectorWoodsEcomm.models import Product, Category, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address
from taggit.models import Tag
from django.shortcuts import get_object_or_404
from vectorWoodsEcomm.forms import ProductReviewForm
from django.http import JsonResponse


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
    #getting reviews
    reviews = ProductReview.objects.filter(product = product).order_by("-date")

    #review form
    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    context = {
        "product" : product,
        "p_image" : p_image,
        "products": products,
        "reviews" : reviews,
        "review_form":review_form,
        "make_review" :make_review,
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

def ajax_add_review(request, pid):
    product = Product.objects.get(pid = pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating'],
    )

    context= {
        'user' : user.username,
        'review': request.POST['review'],
        'rating':request.POST['rating'],
    }
    return JsonResponse(
        {
        'bool':True,
        'context':context,
         }
    )

def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title':request.GET['title'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
        'image':request.GET['image'],
        'pid' : request.GET['pid']
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data

        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})


