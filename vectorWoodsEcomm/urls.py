from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from vectorWoodsEcomm import views
urlpatterns = [
    path('', views.index,name='index'),
    path('products', views.products_view,name='products'),

    path('product/<pid>/', views.product_detail_view, name='product_details'),
    path('category/<cid>/', views.category_view,name='category'),

    #Tags
    path("products/tag/<slug:tag_slug>/", views.tag_list, name='tags')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)