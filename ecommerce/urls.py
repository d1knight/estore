from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # Включаем URL из приложения main
    path('category/', include('category.urls')),  # Убедитесь, что вы включили URL приложения category
    path('products/', include('products.urls')),  # Включаем URL приложения products, если такое имеется
    path('admin_panel/', include('admin_panel.urls', namespace = "admin_panel")), #с помощью namespace изолируем admin_panel
]

# Настройка для обработки медиафайлов
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)