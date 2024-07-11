from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class DishType(models.Model):
    name = models.CharField(max_length=155)

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    specialties = models.ManyToManyField(
        DishType,
        related_name="specialty_cooks",
        blank=True
    )

    def __str__(self):
        specialties_list = ", ".join([
            specialty.name for specialty in self.specialties.all()
        ])
        return f"{self.first_name} {self.last_name}\n{specialties_list}"

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})


class Dish(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    dish_type = models.ForeignKey(
        DishType, on_delete=models.CASCADE, related_name="dishes"
    )
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="cooked_dishes"
    )

    def __str__(self):
        return (f"{self.name}, {self.dish_type.name}, "
                f"({self.price}\n{self.description})")
