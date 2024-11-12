from django.contrib import admin
from .models import Category, Attribute

# Вспомогательный класс для отображения атрибутов в админке для категории
class AttributeInline(admin.TabularInline):
    model = Attribute
    extra = 1  # Количество пустых полей для добавления новых атрибутов

# Админка для категории
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # Автоматическое заполнение поля slug
    inlines = [AttributeInline]  # Включаем атрибуты в админку категории
    search_fields = ['name', 'description']  # Возможность поиска по имени и описанию категории
    list_filter = ['name']  # Фильтрация категорий по имени

# Регистрируем модели в админке
admin.site.register(Category, CategoryAdmin)
admin.site.register(Attribute)
