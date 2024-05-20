from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from vectorWoodsEcomm.models import Product, Category, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist,BlogPost
from taggit.models import Tag
from django.shortcuts import get_object_or_404
from vectorWoodsEcomm.forms import ProductReviewForm
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from reportlab.lib.units import inch
from django.conf import settings
import os
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from svglib.svglib import svg2rlg
from datetime import datetime
from bs4 import BeautifulSoup
from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.graphics import renderPDF

# Create your views here.
def index(request):
    categories = Category.objects.all().order_by("-id")
    products = Product.objects.filter(featured=True)
    blog_posts = BlogPost.objects.all()

    context = {
            "categories" : categories,
            "products":products,
            "blog_posts":blog_posts,
    }
    return render(request, 'index.html', context)


def products_view(request):

    categories = Category.objects.all().order_by("-id")
    products = Product.objects.all().order_by("-date")
    paginator = Paginator(products, 8)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "categories" : categories ,
        "products" : products,
        'page_obj': page_obj,
        
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
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send email
        send_mail(
            subject,
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            email,  # sender
            ['sales@vectorwoodcrafts.co.ke'],  # recipients
            fail_silently=False,
        )

        # Redirect after form submission
        return redirect('thankyou')  # Redirect to a 'thank you' page
    else:
        return render(request, 'contact.html')  # Render the contact form template




def thankyou_view(request):
    return render(request, 'thankyou.html')

def about_view(request):
    return render(request, 'about.html')

def faqs_view(request):
    return render(request, 'faqs.html')

def search_view(request):
    query = request.GET['q']
    products = Product.objects.filter(title__icontains = query, description__icontains = query).order_by("-date")
    context = {
        "products":products,
        "query":query,
    }
    return render(request, 'search.html', context)


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
        'color':request.GET['color'],
        'woodtype':request.GET['woodtype'],
        'dimension':request.GET['dimension'],
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

def cart_view(request):
    cart_total_amount = 0
    vat = 0
    total = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            vat = cart_total_amount * .16
            total = cart_total_amount + vat


        return render(request, 'cart.html' , {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, 'vat': vat, 'total':total })

    else:
        messages.warning(request, 'Your cart is empty')
        return redirect('products')

def checkout_view(request):
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            vat = cart_total_amount * .16
            total = cart_total_amount + vat
        return render(request, 'checkout.html' , {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, 'vat': vat, 'total':total })



def generate_invoice_pdf(order):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    # Create PDF
    p = canvas.Canvas(response, pagesize=letter)

    # p.saveState()
    # p.translate(0, 0)
    # p.rotate(55)
    # p.setFillAlpha(0.4)
    # logo_path = os.path.join(settings.BASE_DIR, 'static/img/logo.png')
    # p.drawImage(logo_path, 4*inch, -1.5*inch, width=8*inch, height=4*inch)
    # p.restoreState()
    
    p.saveState()
    p.setFillColorCMYK(0, 0, 0, 0.05)  # Set transparency
    p.setFont('Helvetica-Bold', 22)
    p.rotate(45)

    text = "VECTOR WOODCRAFTS"
    text_width = p.stringWidth(text, 'Helvetica-Bold', 12)
    x_start = -letter[1]  # Start from the leftmost side (rotated canvas)
    y_start = -letter[0]  # Start from the bottom (rotated canvas)

    for x in range(int(x_start), int(letter[0] * 2), int(text_width * 2)):  # Adjust spacing as needed
        for y in range(int(y_start), int(letter[1] * 1.5), 50):  # Adjust spacing as needed
            p.drawString(x, y, text)

    p.restoreState()

    current_date = datetime.now().strftime("%Y-%m-%d")

    # Add company logo
    # logo_path = os.path.join(settings.BASE_DIR, 'static/img/logo.png')
    # logo = Image.open(logo_path)
    # rotated_logo = logo.rotate(0, expand=True)
    # rotated_logo_reader = ImageReader(rotated_logo)
    # p.drawImage(rotated_logo_reader, 0.2*inch, 10.1*inch, width=1.6*inch, height=0.75*inch)

    # Add invoice details
    p.drawString(500, 670, "Invoice#" + str(order.id))
    p.drawString(500, 655, current_date)
    p.setFillColorRGB(0.4, 0.1, 0)
    p.setFont('Helvetica-Bold', 36)
    p.drawString(160, 745, "VECTOR WOODCRAFTS")
    p.setFillColorRGB(0, 0, 0)
    p.setFont('Helvetica', 10)
    p.setFillColorRGB(0, 0, 0)
    p.setFont('Helvetica-Bold', 16)
    p.drawString(20, 685, "INVOICE TO:")
    p.setFont('Helvetica', 12)
    p.drawString(20, 670, "Name: " + order.user.first_name + ' ' + order.user.last_name)
    p.drawString(20, 655, "Phone No: " + order.user.phone_no)
    p.drawString(20, 640, "Email: " + order.user.email)
    p.drawString(20, 625, "Delivery address: " + order.user.address + ' , ' + order.user.city)

    # Define header data with Serial Number
    header_data = [["S.No", "Cart Items", "Quantity", "Unit Price", "Sub-total"]]

    # Define table style for the header
    header_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    # Create header table object
    header_table = Table(header_data, colWidths=[0.5*inch, 2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    header_table.setStyle(header_style)

    # Calculate header table height
    header_table_width, header_table_height = header_table.wrap(0, 0)

    # Position header table
    header_table.drawOn(p, 0.3 * inch, 560)

    # Add table for item details with serial number
    data = []
    counter = 1
    for item in order.cartorderitems_set.all():
        data.append([counter, item.item, item.qty, 'Ksh ' + str(item.price), 'Ksh ' + str(item.total)])
        counter += 1

    # Define table style for the data
    style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    # Define column widths for the data table including Serial Number column
    col_widths = [0.5*inch, 2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch]

    # Create table object for the data
    t = Table(data, colWidths=col_widths)
    t.setStyle(style)

    # Calculate table height
    table_height = t.wrap(0, 0)[1]

    # Position table on the canvas
    t.drawOn(p, 0.3 * inch, 560 - table_height)

    # Add totals below the header table, to the bottom right
    p.setFont('Helvetica-Bold', 10)
    totals_y = 590 - table_height - 50  # Adjust position below the last data row
    p.drawString(0.3 * inch + sum(col_widths) - 200, totals_y,"Sub-total:"            " Ksh "   + str(order.subtotal))
    p.drawString(0.3 * inch + sum(col_widths) - 200, totals_y - 15,  "VAT (16%):"            " Ksh " + str(order.vat))
    p.drawString(0.3 * inch + sum(col_widths) - 200, totals_y - 30, "Total:"            " Ksh " + str(order.price))
    p.setFillColorRGB(0.4, 0.1, 0)
    p.setFont('Helvetica-Bold', 16)
    p.drawString(20, 190, "TERMS AND CONDITIONS" )
    p.setFillColorRGB(0, 0, 0)
    p.setFont('Helvetica', 12)
    p.drawString(20, 175, "Your payment is due two weeks on order placement.")
    p.drawString(20, 160, "Failure to pay within two weeks, your order will be cancelled.")

    p.setFillColor('black')
    p.setFont('Helvetica', 12)
    p.drawString(20, 60, "+254 712 555 577")
    p.drawString(20, 45, "sales@vectorwoodcrafts.co.ke")
    p.drawString(20, 30, "www.vectorwoodcrafts.co.ke")
    p.drawString(20, 15, "Butere road No. 16, Industrial Area")

    p.showPage()
    p.save()

    return response

def order_success_view(request):
    cart_total_amount = 0
    order = None

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            vat = int(cart_total_amount * .16)
            total = int(cart_total_amount + vat)

        # Creating order object
        order =  CartOrder.objects.create(
            user=request.user,
            subtotal=cart_total_amount,
            vat=vat,
            price=total
        )

        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            vat = cart_total_amount * .16
            total = cart_total_amount + vat
            cart_order_items = CartOrderItems.objects.create(
                order=order,
                invoice_no="INVOICE_NO-" + str(order.id),
                item=item['title'],
                img=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty']) * float(item['price'])
            ) 

    if 'cart_data_obj' in request.session:
        del request.session['cart_data_obj']

    # Generate invoice PDF
    invoice_pdf = generate_invoice_pdf(order)

    # Send order confirmation email with invoice PDF attached
    # Render the email template (assuming 'order_confirmation_email.html' exists)

    #email_html = render_to_string('order_confirmation_email.html', {'order': order, 'user': request.user}, request=request)

    # Extract text content from the HTML
    user = request.user
    subject = 'Your Vector Woodcrafts Order Confirmation - Order No #' + str(order.id)
    from_email = settings.EMAIL_HOST_USER
    to_email = order.user.email

    # Load and render the template with context
    html_content = render_to_string('email_template.html', {'order': order,'user' : user})

    # Create the email message
    msg = EmailMessage(subject, html_content, from_email, [to_email])
    msg.content_subtype = 'html'  # Main content is now text/html
    msg.attach('invoice.pdf', invoice_pdf.getvalue(), 'application/pdf')
    msg.send()
    
    

    return render(request, 'order-success.html')




def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:

            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    vat = 0
    total = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            vat = cart_total_amount * 0.16
            total = cart_total_amount + vat

    context = render_to_string("async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, 'vat': vat, 'total':total })

    return JsonResponse ({"data":context, 'totalcartitems':len(request.session['cart_data_obj'])})


def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
        

            cart_data = request.session['cart_data_obj']
            cart_data [str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    vat = 0
    total = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            vat = cart_total_amount * .16
            total = cart_total_amount + vat

    context = render_to_string("async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, 'vat': vat, 'total':total })

    return JsonResponse ({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})
def blog_view(request):
    blog_posts = BlogPost.objects.all()
    context = {
        'blog_posts': blog_posts
    }
    return render(request, 'blog.html', context)

def blog_detail_view(request, bid):
    blog = BlogPost.objects.get(bid=bid)

    context = {
        'blog': blog
    }
    return render(request, 'blog_details.html', context)