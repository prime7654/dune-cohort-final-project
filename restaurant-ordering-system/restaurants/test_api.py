import json
from django.test import TestCase
from django.urls import reverse

from .models import MenuCategory, MenuItem


class MenuItemAPITests(TestCase):
    def setUp(self):
        self.category = MenuCategory.objects.create(
            name="Rice",
            description="Rice meals",
        )
        self.menu_item = MenuItem.objects.create(
            category=self.category,
            name="Jollof Rice",
            description="Party-style jollof rice",
            price="2500.00",
            stock=12,
            is_available=True,
        )

    def test_menu_item_list_returns_nested_menu_category(self):
        response = self.client.get(reverse("api_menu_item_list"))

        self.assertEqual(response.status_code, 200)
        menu_item = next(item for item in response.json() if item["name"] == "Jollof Rice")
        self.assertEqual(menu_item["menu_category"]["name"], "Rice")

    def test_menu_item_create_uses_menu_category_id_and_returns_menu_category_object(self):
        response = self.client.post(
            reverse("api_menu_item_list"),
            data=json.dumps(
                {
                    "menu_category_id": self.category.pk,
                    "name": "Fried Rice",
                    "description": "Vegetable fried rice",
                    "price": "2800.00",
                    "stock": 7,
                    "is_available": True,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(MenuItem.objects.filter(name="Fried Rice").exists())
        self.assertEqual(response.json()["menu_category"]["name"], "Rice")
        self.assertNotIn("menu_category_id", response.json())

    def test_menu_item_detail_returns_single_menu_item(self):
        response = self.client.get(reverse("api_menu_item_detail", args=[self.menu_item.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Jollof Rice")

    def test_menu_item_put_fully_updates_menu_item(self):
        response = self.client.put(
            reverse("api_menu_item_detail", args=[self.menu_item.pk]),
            data=json.dumps(
                {
                    "menu_category_id": self.category.pk,
                    "name": "Jollof Rice Deluxe",
                    "description": "Updated recipe",
                    "price": "3000.00",
                    "stock": 4,
                    "is_available": False,
                }
            ),
            content_type="application/json",
        )

        self.menu_item.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.menu_item.name, "Jollof Rice Deluxe")
        self.assertEqual(str(self.menu_item.price), "3000.00")
        self.assertFalse(self.menu_item.is_available)

    def test_menu_item_delete_removes_menu_item(self):
        response = self.client.delete(reverse("api_menu_item_detail", args=[self.menu_item.pk]))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(MenuItem.objects.filter(pk=self.menu_item.pk).exists())


class MenuCategoryAPITests(TestCase):
    def test_menu_category_list_returns_menu_item_count_and_menu_items(self):
        category = MenuCategory.objects.create(
            name="Rice",
            description="Rice meals",
        )
        MenuItem.objects.create(
            category=category,
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
