from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:category_slug>/', views.products_by_category, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:slug>/', views.product_detail, name='product_detail'),
    # path('search/', views.product_search, name='product_search'),  # Добавленный путь для поиска
    # path('get-category-attributes/', views.get_category_attributes, name='get_category_attributes'),  # Новый URL
]
