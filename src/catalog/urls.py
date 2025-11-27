from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('<int:product_id>/stock/', views.product_stock, name='product_stock'),
]
