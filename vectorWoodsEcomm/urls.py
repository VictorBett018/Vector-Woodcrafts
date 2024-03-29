from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from vectorWoodsEcomm import views
urlpatterns = [
    path('', views.index,name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('thankyou/', views.thankyou_view, name='thankyou'),
    path('about/', views.about_view, name='about'),
    path('products', views.products_view,name='products'),
    path('product/<pid>/', views.product_detail_view, name='product_details'),
    path('category/<cid>/', views.category_view,name='category'),

    #search
    path('search/', views.search_view, name='search'),


    #Tags
    path("products/tag/<slug:tag_slug>/", views.tag_list, name='tags'),
    #add review
    path('ajax-add-review/<pid>/', views.ajax_add_review, name = 'ajax-add-review'),
    
    path('add-to-cart/', views.add_to_cart, name = 'add-to-cart'),
    path('cart/', views.cart_view, name = 'cart'),

    path('delete-from-cart/', views.delete_item_from_cart, name = 'delete-from-cart'),

    path('update-cart/', views.update_cart, name = 'update-cart'),


    path('checkout/', views.checkout_view, name = 'checkout'),






] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)