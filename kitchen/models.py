from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class DishType(models.Model):
    name = models.CharField(max_length=155)

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    specialties = models.ManyToManyField(DishType, related_name="cooks", blank=True)
    def __str__(self):
        specialties_list = ", ".join([specialty.name for specialty in self.specialties.all()])
        return f"{self.first_name} {self.last_name}\n{specialties_list}"


class Dish(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE, related_name="dish_types")
    cooks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="cooks")

    def __str__(self):
        return f"{self.dish_type.name}, {self.name}, {self.price}\n{self.description}"
