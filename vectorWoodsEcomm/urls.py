from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from vectorWoodsEcomm import views
urlpatterns = [
    path('', views.index,name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('thankyou/', views.thankyou_view, name='thankyou'),
    path('about/', views.about_view, name='about'),
    path('faqs/', views.faqs_view, name='faqs'),
    path('products', views.products_view,name='products'),
    path('product/<pid>/', views.product_detail_view, name='product_details'),
    path('category/<cid>/', views.category_view,name='category'),
    path('search/', views.search_view, name='search'),
    path('blog/', views.blog_view, name='blog'),
    path('blog/<bid>/', views.blog_detail_view, name='blog_details'),
    path("products/tag/<slug:tag_slug>/", views.tag_list, name='tags'),
    path('ajax-add-review/<pid>/', views.ajax_add_review, name = 'ajax-add-review'),
    path('add-to-cart/', views.add_to_cart, name = 'add-to-cart'),
    path('cart/', views.cart_view, name = 'cart'),
    path('delete-from-cart/', views.delete_item_from_cart, name = 'delete-from-cart'),
    path('update-cart/', views.update_cart, name = 'update-cart'),
    path('checkout/', views.checkout_view, name = 'checkout'),
    path('order-success/', views.order_success_view, name='order-success'),

    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.svg')),






] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)