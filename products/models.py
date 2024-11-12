from django.db import models
from django.utils.text import slugify
from category.models import Category, Attribute  # Импортируем модель Category и Attribute


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='products/images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='products/images/', blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, unique=True)  # Поле для slug

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # Если slug не заполнен
            self.slug = slugify(self.name)  # Генерируем slug на основе имени продукта
        super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='products/images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Изображение для {self.product.name}"


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_values')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)  # Значение атрибута для продукта (например, "Красный", "L")

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"
