from django.db import models
from category.models import Category

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='menu_images', blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE, related_name='menu_items')

    def __str__(self):
        return self.name