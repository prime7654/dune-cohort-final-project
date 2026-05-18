import json
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import MenuCategory, MenuItem

User = get_user_model()


class MenuItemAPITests(TestCase):
    client_class = APIClient

    def setUp(self):
        MenuCategory.objects.all().delete()
        self.owner = User.objects.create_user(
            username="chef",
            email="chef@example.com",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            username="server",
            email="server@example.com",
            password="StrongPass123!",
        )
        self.category = MenuCategory.objects.create(
            name="Rice",
            description="Rice meals",
        )
        self.drinks_category = MenuCategory.objects.create(
            name="Drinks",
            description="Cold drinks",
        )
        self.menu_item = MenuItem.objects.create(
            category=self.category,
            created_by=self.owner,
            name="Jollof Rice",
            description="Party-style jollof rice",
            price="2500.00",
            stock=12,
            is_available=True,
        )

    def menu_item_payload(self, **overrides):
        payload = {
            "menu_category_id": self.category.pk,
            "name": "Fried Rice",
            "description": "Vegetable fried rice",
            "price": "2800.00",
            "stock": 7,
            "is_available": True,
        }
        payload.update(overrides)
        return payload

    def test_menu_item_list_is_paginated_and_returns_nested_fields(self):
        response = self.client.get(reverse("api_menu_item_list"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertIsNone(data["next"])
        self.assertIsNone(data["previous"])
        menu_item = data["results"][0]
        self.assertEqual(menu_item["menu_category"]["name"], "Rice")
        self.assertEqual(menu_item["created_by"]["username"], "chef")

    def test_menu_item_list_uses_six_items_per_page(self):
        for index in range(6):
            MenuItem.objects.create(
                category=self.category,
                created_by=self.owner,
                name=f"Rice Bowl {index}",
                price="1500.00",
            )

        first_page = self.client.get(reverse("api_menu_item_list"))
        second_page = self.client.get(f"{reverse('api_menu_item_list')}?page=2")

        self.assertEqual(first_page.status_code, 200)
        self.assertEqual(first_page.json()["count"], 7)
        self.assertEqual(len(first_page.json()["results"]), 6)
        self.assertIsNotNone(first_page.json()["next"])
        self.assertIsNone(first_page.json()["previous"])
        self.assertEqual(second_page.status_code, 200)
        self.assertEqual(len(second_page.json()["results"]), 1)
        self.assertIsNotNone(second_page.json()["previous"])

    def test_menu_item_create_requires_authentication(self):
        response = self.client.post(
            reverse("api_menu_item_list"),
            data=json.dumps(self.menu_item_payload()),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)
        self.assertFalse(MenuItem.objects.filter(name="Fried Rice").exists())

    def test_menu_item_create_assigns_authenticated_user(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            reverse("api_menu_item_list"),
            data=json.dumps(self.menu_item_payload()),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        created_item = MenuItem.objects.get(name="Fried Rice")
        self.assertEqual(created_item.created_by, self.owner)
        self.assertEqual(response.json()["menu_category"]["name"], "Rice")
        self.assertEqual(response.json()["created_by"]["username"], "chef")
        self.assertNotIn("menu_category_id", response.json())

    def test_menu_item_detail_returns_single_menu_item(self):
        response = self.client.get(reverse("api_menu_item_detail", args=[self.menu_item.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Jollof Rice")
        self.assertEqual(response.json()["created_by"]["username"], "chef")

    def test_menu_item_put_requires_authentication(self):
        response = self.client.put(
            reverse("api_menu_item_detail", args=[self.menu_item.pk]),
            data=json.dumps(self.menu_item_payload(name="Jollof Rice Deluxe")),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    def test_menu_item_creator_can_update_menu_item(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.put(
            reverse("api_menu_item_detail", args=[self.menu_item.pk]),
            data=json.dumps(
                self.menu_item_payload(
                    name="Jollof Rice Deluxe",
                    description="Updated recipe",
                    price="3000.00",
                    stock=4,
                    is_available=False,
                )
            ),
            content_type="application/json",
        )

        self.menu_item.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.menu_item.name, "Jollof Rice Deluxe")
        self.assertEqual(str(self.menu_item.price), "3000.00")
        self.assertFalse(self.menu_item.is_available)

    def test_non_creator_cannot_update_menu_item(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.put(
            reverse("api_menu_item_detail", args=[self.menu_item.pk]),
            data=json.dumps(self.menu_item_payload(name="Server Rice")),
            content_type="application/json",
        )

        self.menu_item.refresh_from_db()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.menu_item.name, "Jollof Rice")

    def test_menu_item_delete_requires_authentication(self):
        response = self.client.delete(reverse("api_menu_item_detail", args=[self.menu_item.pk]))

        self.assertEqual(response.status_code, 401)
        self.assertTrue(MenuItem.objects.filter(pk=self.menu_item.pk).exists())

    def test_menu_item_creator_can_delete_menu_item(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(reverse("api_menu_item_detail", args=[self.menu_item.pk]))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(MenuItem.objects.filter(pk=self.menu_item.pk).exists())

    def test_non_creator_cannot_delete_menu_item(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.delete(reverse("api_menu_item_detail", args=[self.menu_item.pk]))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(MenuItem.objects.filter(pk=self.menu_item.pk).exists())

    def test_menu_item_list_filters_by_category_and_availability(self):
        MenuItem.objects.create(
            category=self.drinks_category,
            created_by=self.owner,
            name="Zobo Drink",
            price="900.00",
            is_available=False,
        )

        response = self.client.get(
            f"{reverse('api_menu_item_list')}?category={self.drinks_category.pk}&is_available=false"
        )

        self.assertEqual(response.status_code, 200)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Zobo Drink")

    def test_menu_item_list_searches_by_name(self):
        MenuItem.objects.create(
            category=self.category,
            created_by=self.owner,
            name="Coconut Rice",
            price="2600.00",
        )
        MenuItem.objects.create(
            category=self.drinks_category,
            created_by=self.owner,
            name="Chapman",
            price="1200.00",
        )

        response = self.client.get(f"{reverse('api_menu_item_list')}?search=rice")

        self.assertEqual(response.status_code, 200)
        names = {item["name"] for item in response.json()["results"]}
        self.assertEqual(names, {"Coconut Rice", "Jollof Rice"})

    def test_menu_item_list_orders_by_price(self):
        MenuItem.objects.create(
            category=self.category,
            created_by=self.owner,
            name="Beans Porridge",
            price="1800.00",
        )
        MenuItem.objects.create(
            category=self.drinks_category,
            created_by=self.owner,
            name="Chapman",
            price="1200.00",
        )

        response = self.client.get(f"{reverse('api_menu_item_list')}?ordering=price")

        self.assertEqual(response.status_code, 200)
        prices = [Decimal(item["price"]) for item in response.json()["results"]]
        self.assertEqual(prices, sorted(prices))


class JWTAuthTests(TestCase):
    client_class = APIClient

    def setUp(self):
        cache.clear()

    def test_single_auth_token_endpoint_returns_token(self):
        User.objects.create_user(
            username="chef",
            email="chef@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("api_auth_token"),
            {"username": "chef", "password": "StrongPass123!"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_single_auth_token_locks_after_five_failed_attempts(self):
        User.objects.create_user(
            username="chef",
            email="chef@example.com",
            password="StrongPass123!",
        )

        for _ in range(4):
            response = self.client.post(
                reverse("api_auth_token"),
                {"username": "chef", "password": "WrongPass123!"},
                format="json",
            )
            self.assertEqual(response.status_code, 400)

        locked_response = self.client.post(
            reverse("api_auth_token"),
            {"username": "chef", "password": "WrongPass123!"},
            format="json",
        )
        correct_password_response = self.client.post(
            reverse("api_auth_token"),
            {"username": "chef", "password": "StrongPass123!"},
            format="json",
        )

        self.assertEqual(locked_response.status_code, 429)
        self.assertEqual(correct_password_response.status_code, 429)

    def test_single_auth_token_can_create_menu_item(self):
        MenuCategory.objects.all().delete()
        category = MenuCategory.objects.create(name="Rice", description="Rice meals")
        User.objects.create_user(
            username="chef",
            email="chef@example.com",
            password="StrongPass123!",
        )
        token_response = self.client.post(
            reverse("api_auth_token"),
            {"username": "chef", "password": "StrongPass123!"},
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token_response.json()['token']}")

        response = self.client.post(
            reverse("api_menu_item_list"),
            {
                "menu_category_id": category.pk,
                "name": "Coconut Rice",
                "description": "Rice cooked with coconut milk",
                "price": "2600.00",
                "stock": 8,
                "is_available": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["created_by"]["username"], "chef")

    def test_token_and_refresh_endpoints_return_access_tokens(self):
        User.objects.create_user(
            username="chef",
            email="chef@example.com",
            password="StrongPass123!",
        )

        token_response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "chef", "password": "StrongPass123!"},
            format="json",
        )
        refresh_response = self.client.post(
            reverse("token_refresh"),
            {"refresh": token_response.json()["refresh"]},
            format="json",
        )

        self.assertEqual(token_response.status_code, 200)
        self.assertIn("access", token_response.json())
        self.assertIn("refresh", token_response.json())
        self.assertEqual(refresh_response.status_code, 200)
        self.assertIn("access", refresh_response.json())

    def test_jwt_token_endpoint_locks_after_five_failed_attempts(self):
        User.objects.create_user(
            username="chef",
            email="chef@example.com",
            password="StrongPass123!",
        )

        for _ in range(4):
            response = self.client.post(
                reverse("token_obtain_pair"),
                {"username": "chef", "password": "WrongPass123!"},
                format="json",
            )
            self.assertEqual(response.status_code, 401)

        locked_response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "chef", "password": "WrongPass123!"},
            format="json",
        )
        correct_password_response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "chef", "password": "StrongPass123!"},
            format="json",
        )

        self.assertEqual(locked_response.status_code, 429)
        self.assertEqual(correct_password_response.status_code, 429)


class MenuCategoryAPITests(TestCase):
    def test_menu_category_list_returns_menu_item_count_and_menu_items(self):
        MenuCategory.objects.all().delete()
        user = User.objects.create_user(username="chef", password="StrongPass123!")
        category = MenuCategory.objects.create(
            name="Rice",
            description="Rice meals",
        )
        MenuItem.objects.create(
            category=category,
            created_by=user,
            name="Jollof Rice",
            description="Party-style jollof rice",
            price="2500.00",
        )

        response = self.client.get(reverse("api_menu_category_list"))

        self.assertEqual(response.status_code, 200)
        data = next(item for item in response.json() if item["name"] == "Rice")
        self.assertEqual(data["name"], "Rice")
        self.assertEqual(data["menu_item_count"], 1)
        self.assertEqual(data["menu_items"][0]["name"], "Jollof Rice")
        self.assertEqual(data["menu_items"][0]["created_by"]["username"], "chef")


class CORSTests(TestCase):
    def test_api_responses_allow_all_origins(self):
        response = self.client.get(
            reverse("api_menu_item_list"),
            HTTP_ORIGIN="https://example.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["access-control-allow-origin"], "*")
