from django.contrib import admin
from .models import Product, ProductAttributeValue  # Исправлено на правильный импорт
from category.models import Attribute  # Импортируем Attribute из категорий

# Админка для значений атрибутов
class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1  # Количество пустых полей для добавления новых значений атрибутов

# Админка для продуктов
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')  # Отображение имени продукта и категории
    search_fields = ['name']  # Возможность поиска по имени продукта
    list_filter = ['category']  # Фильтрация продуктов по категориям
    inlines = [ProductAttributeValueInline]  # Включаем управление значениями атрибутов в админке продукта

# Админка для значений атрибутов
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')  # Отображение продукта, атрибута и его значения
    search_fields = ['value']  # Возможность поиска по значению атрибута
    list_filter = ['attribute', 'product']  # Фильтрация значений по атрибуту и продукту

# Регистрируем модели в админке
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductAttributeValue, ProductAttributeValueAdmin)  # Регистрируем правильную модель
