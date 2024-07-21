from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType, Dish


HOME_URL = reverse("kitchen:index")
DISH_TYPE_LIST_URL = reverse("kitchen:dish-type-list")
DISH_TYPE_CREATE_URL = reverse("kitchen:dish-type-create")
DISH_LIST_URL = reverse("kitchen:dish-list")
DISH_CREATE_URL = reverse("kitchen:dish-create")
COOK_LIST_URL = reverse("kitchen:cook-list")
COOK_CREATE_URL = reverse("kitchen:cook-create")


class LoginRequiredTest(TestCase):
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
        self.cook.cooked_dishes.set([self.dish1])
        self.cook.specialties.set([self.dish_type])

    def test_login_required_dish_type_create(self):
        res = self.client.get(DISH_TYPE_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_dish_type_update(self):
        res = self.client.get(reverse(
            "kitchen:dish-type-update",
            args=[self.dish_type.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_dish_type_delete(self):
        res = self.client.get(reverse(
            "kitchen:dish-type-delete",
            args=[self.dish_type.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_cook_create(self):
        res = self.client.get(COOK_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_cook_detail(self):
        res = self.client.get(reverse(
            "kitchen:cook-detail",
            args=[self.cook.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_cook_update(self):
        res = self.client.get(reverse(
            "kitchen:cook-update",
            args=[self.cook.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_cook_delete(self):
        res = self.client.get(reverse(
            "kitchen:cook-delete",
            args=[self.cook.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_dish_create(self):
        res = self.client.get(DISH_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_dish_update(self):
        res = self.client.get(reverse(
            "kitchen:dish-update",
            args=[self.dish1.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_dish_delete(self):
        res = self.client.get(reverse(
            "kitchen:dish-delete",
            args=[self.dish1.id]
        ))
        self.assertNotEqual(res.status_code, 200)


class IndexViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="PASSWORD"
        )
        self.client.force_login(self.user)

    def test_index(self):
        response = self.client.get(HOME_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/index.html")


class DishTypeListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(
            name="Test",
        )
        self.dish_type2 = DishType.objects.create(
            name="abc",
        )

    def test_dish_type_list_view(self):
        DishType.objects.create(name="Test3")
        response = self.client.get(DISH_TYPE_LIST_URL)
        dish_types = DishType.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_type_list.html")
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dish_types)
        )

    def test_dish_type_list_view_search(self):
        response = self.client.get(DISH_TYPE_LIST_URL, {"name": "Test"})
        self.assertContains(response, self.dish_type.name)
        self.assertNotContains(response, self.dish_type2.name)


class DishTypeCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)

    def test_dish_type_create_view(self):
        response = self.client.get(DISH_TYPE_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "kitchen/dish_type_form.html"
        )

    def test_dish_type_create(self):
        test_data = {"name": "test11"}
        response = self.client.post(DISH_TYPE_CREATE_URL, data=test_data)
        self.assertEqual(response.status_code, 302)
        new_dish_type = DishType.objects.get(name=test_data["name"])
        self.assertEqual(new_dish_type.name, test_data["name"])


class DishTypeUpdateDeleteViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(
            name="Test"
        )

    def test_dish_type_update(self):
        url = reverse("kitchen:dish-type-update", args=[self.dish_type.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_type_form.html")

    def test_dish_type_delete(self):
        url = reverse("kitchen:dish-type-delete", args=[self.dish_type.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "kitchen/dishtype_confirm_delete.html"
        )


class DishListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(
            name="Test"
        )
        self.dish = Dish.objects.create(
            name="Test dish",
            description="Test dish description",
            price=10,
            dish_type=self.dish_type
        )
        self.dish.cooks.set([self.user])
        self.dish1 = Dish.objects.create(
            name="Rest dish 1",
            description="Test dish description 1",
            price=10,
            dish_type=self.dish_type
        )
        self.dish1.cooks.set([self.user])

    def test_dish_list_view(self):
        response = self.client.get(DISH_LIST_URL)
        dishes = Dish.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["dish_list"]), list(dishes))
        self.assertTemplateUsed(response, "kitchen/dish_list.html")

    def test_dish_list_view_search(self):
        response = self.client.get(DISH_LIST_URL, {"name": "Test"})
        self.assertContains(response, self.dish.name)
        self.assertNotContains(response, self.dish1.name)


class DishCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(
            name="Test",
            )
        self.cook = get_user_model().objects.create_user(
            username="testuser1",
            password="password",
        )
        self.cook.specialties.set([self.dish_type])

    def test_dish_create_view(self):
        response = self.client.get(DISH_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_form.html")

    def test_dish_create(self):
        form_data = {
            "name": "Test Dish",
            "description": "Test dish description 1",
            "price": 10,
            "dish_type": self.dish_type.id,
            "cooks": self.cook.id
        }
        response = self.client.post(DISH_CREATE_URL, data=form_data)
        self.assertEqual(response.status_code, 302)
        new_dish = Dish.objects.get(name=form_data["name"])

        self.assertEqual(new_dish.name, form_data["name"])
        self.assertEqual(new_dish.dish_type.id, form_data["dish_type"])
        self.assertIn(self.cook, new_dish.cooks.all())


class DishUpdateDeleteViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(
            name="Test Dish Type"
        )
        self.cook = get_user_model().objects.create_user(
            username="testuser1",
            password="password",
        )
        self.cook.specialties.set([self.dish_type])
        self.dish = Dish.objects.create(
            name="Rest dish 1",
            description="Test dish description 1",
            price=10,
            dish_type=self.dish_type
        )
        self.dish.cooks.set([self.cook])

    def test_dish_update(self):
        test_data = {
            "name": "carbonara",
            "description": "Test carbonara description",
            "price": 10,
            "dish_type": self.dish.dish_type.id,
            "cooks": self.cook.id
        }
        url = reverse("kitchen:dish-update", args=[self.dish.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_form.html")

        response = self.client.post(url, test_data)
        self.assertEqual(response.status_code, 302)

        self.dish.refresh_from_db()
        self.assertEqual(self.dish.name, test_data["name"])

    def test_dish_delete(self):
        url = reverse("kitchen:dish-delete", args=[self.dish.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_confirm_delete.html")


class CookListViewTests(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(
            name="Test Dish Type"
        )
        self.dish = Dish.objects.create(
            name="Rest dish 1",
            description="Test dish description 1",
            price=10,
            dish_type=self.dish_type
        )

        self.cook1 = get_user_model().objects.create_user(
            username="testuser1",
            password="password",
        )
        self.dish.cooks.set([self.cook1])
        self.cook1.specialties.set([self.dish_type])

        self.cook1.cooked_dishes.set([self.dish])

        self.cook2 = get_user_model().objects.create_user(
            username="testuser2",
            password="testpassword2",
        )
        self.cook2.cooked_dishes.set([self.dish])
        self.cook2.specialties.set([self.dish_type])

        self.client.force_login(self.cook1)

    def test_cook_list_view(self):
        response = self.client.get(COOK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.cook1.username)
        self.assertContains(response, self.cook2.username)

    def test_cook_list_view_search(self):
        response = self.client.get(COOK_LIST_URL, {"username": "testuser1"})
        self.assertContains(response, self.cook1.username)
        self.assertNotContains(response, self.cook2.username)

    def test_cook_list_view_no_results(self):
        response = self.client.get(COOK_LIST_URL, {
            "username": "nonexistent_driver"
        })
        self.assertContains(response, "There are no cooks")


class CookDetailViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(
            name="Test Dish Type"
        )
        self.dish = Dish.objects.create(
            name="Rest dish 1",
            description="Test dish description 1",
            price=10,
            dish_type=self.dish_type
        )

        self.cook = get_user_model().objects.create_user(
            username="testuser1",
            password="password",
        )
        self.dish.cooks.set([self.cook])
        self.cook.specialties.set([self.dish_type])
        self.cook.cooked_dishes.set([self.dish])

    def test_cook_detail_view(self):
        response = self.client.get(reverse(
            "kitchen:cook-detail",
            args=[self.cook.id]
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cook_detail.html")
        self.assertIn("cook", response.context)


class CookUpdateDeleteTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(
            name="Test Dish Type"
        )
        self.dish = Dish.objects.create(
            name="Rest dish 1",
            description="Test dish description 1",
            price=10,
            dish_type=self.dish_type
        )

        self.cook = get_user_model().objects.create_user(
            username="testuser1",
            password="password",
        )
        self.dish.cooks.set([self.cook])
        self.cook.specialties.set([self.dish_type])
        self.cook.cooked_dishes.set([self.dish])

    def test_cook_update(self):
        url = reverse("kitchen:cook-update", args=[self.cook.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cook_form.html")

    def test_cook_delete(self):
        url = reverse("kitchen:cook-delete", args=[self.cook.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "kitchen/cook_confirm_delete.html"
        )
