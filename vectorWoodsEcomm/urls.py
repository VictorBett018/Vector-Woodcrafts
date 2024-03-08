from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from vectorWoodsEcomm import views
urlpatterns = [
    path('', views.index,name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('products', views.products_view,name='products'),
    path('product/<pid>/', views.product_detail_view, name='product_details'),
    path('category/<cid>/', views.category_view,name='category'),

    #Tags
    path("products/tag/<slug:tag_slug>/", views.tag_list, name='tags'),
    #add review
    path('ajax-add-review/<pid>/', views.ajax_add_review, name = 'ajax-add-review'),
    
    path('add-to-cart/', views.add_to_cart, name = 'add-to-cart'),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)