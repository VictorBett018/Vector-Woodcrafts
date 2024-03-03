from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from vectorWoodsEcomm import views
urlpatterns = [
    path('', views.index,name='index'),
    path('products', views.products_view,name='products'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)