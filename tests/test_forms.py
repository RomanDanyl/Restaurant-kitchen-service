from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.forms import CookCreationForm
from kitchen.models import Dish, DishType


User = get_user_model()


class CookCreationFormTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Cook Creation")
        self.cook = get_user_model().objects.create_user(
            username="testuser12",
            first_name="Test",
            last_name="User",
            password="6hH00kkhY}t",
        )
        self.dish1 = Dish.objects.create(
            name="Dish 1",
            price=10,
            dish_type=self.dish_type,
        )
        self.dish1.cooks.set([self.cook])
        self.cook.specialties.set([self.dish_type])

    def test_cook_creation_form_with_specialties_and_cooked_dishes(self):
        form_data = {
            "username": "testuser112",
            "password1": "6hH00kkhY}t",
            "password2": "6hH00kkhY}t",
            "first_name": "Test",
            "last_name": "User",
            "specialties": [self.dish_type.id],
            "cooked_dishes": [self.dish1.id],
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

        self.assertEqual(self.cook.username, "testuser12")
        self.assertTrue(self.cook.check_password("6hH00kkhY}t"))
        self.assertEqual(self.cook.first_name, "Test")
        self.assertEqual(self.cook.last_name, "User")
        self.assertEqual(list(self.cook.specialties.all()), [self.dish_type])
        self.assertEqual(list(self.cook.cooked_dishes.all()), [self.dish1])
