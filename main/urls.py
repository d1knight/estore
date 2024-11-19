from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('search/', views.search_results, name='search_results'),   
]
