from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType, Dish

USERNAME = "test"
PASSWORD = "PASSWORD"
FIRST_NAME = "test_first"
LAST_NAME = "test_last"
SPECIALTY_NAME = "test"


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.specialty = DishType.objects.create(name=SPECIALTY_NAME)

        cls.cook = get_user_model().objects.create_user(
            username=USERNAME,
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            password=PASSWORD,
        )

        cls.cook.specialties.set([cls.specialty])

    def test_dish_type_str(self):
        dish_type = DishType.objects.create(name="test")
        self.assertEqual(str(dish_type), "test")

    def test_cook_str(self):
        cook = get_user_model().objects.get(id=self.cook.id)
        expected_str = f"{FIRST_NAME} {LAST_NAME}\n{SPECIALTY_NAME}"
        self.assertEqual(str(cook), expected_str)

    def test_cook_get_absolute_url(self):
        url = self.cook.get_absolute_url()
        expected_url = reverse(
            "kitchen:cook-detail", kwargs={"pk": self.cook.pk}
        )
        self.assertEqual(url, expected_url)

    def test_dish_str(self):
        dish_type = DishType.objects.create(name="test")
        cook = get_user_model().objects.get(id=self.cook.id)
        dish = Dish.objects.create(
            name="test", description="descr", dish_type=dish_type, price=100
        )
        dish.cooks.set([cook])
        expected_str = (f"{dish.name}, {dish.dish_type.name}, "
                        f"({dish.price}\n{dish.description})")
        self.assertEqual(str(dish), expected_str)

    def test_create_cook_with_specialties(self):
        cook = get_user_model().objects.get(id=self.cook.id)
        self.assertEqual(cook.username, USERNAME)
        self.assertTrue(cook.specialties.filter(id=self.specialty.id).exists())
        self.assertTrue(cook.check_password(PASSWORD))
