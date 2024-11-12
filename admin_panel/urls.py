from django.urls import path
from . import views

app_name = 'admin_panel'


urlpatterns = [
    path('', views.admin_panel, name='admin_panel'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.create_category, name='create_category'),
    path('category/update/<int:pk>/', views.update_category, name='update_category'),
    path('category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.create_product, name='create_product'),  
]
