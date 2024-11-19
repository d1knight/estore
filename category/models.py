from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Проверяем, пуст ли slug
            self.slug = slugify(self.name)  # Генерируем slug из названия
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    




class Attribute(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, related_name='attributes', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Category: {self.category.name})"