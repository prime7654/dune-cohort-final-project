from django.test import TestCase, override_settings
from django.urls import reverse

from .models import MenuCategory, MenuItem


class MenuViewTests(TestCase):
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
            is_available=True,
        )

    def test_menu_list_renders_items(self):
        response = self.client.get(reverse("menu_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jollof Rice")
        self.assertContains(response, "In Stock")
        self.assertContains(response, "Add to Cart")
        self.assertTemplateUsed(response, "restaurants/menu_list.html")

    def test_menu_detail_renders_item_fields(self):
        response = self.client.get(reverse("menu_detail", args=[self.menu_item.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jollof Rice")
        self.assertContains(response, "2500.00")
        self.assertContains(response, "Rice")
        self.assertContains(response, "In Stock")
        self.assertTemplateUsed(response, "restaurants/menu_detail.html")

    def test_menu_detail_has_add_to_cart_form(self):
        response = self.client.get(reverse("menu_detail", args=[self.menu_item.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add to Cart")
        self.assertContains(response, reverse("cart_add", args=[self.menu_item.pk]))

    def test_category_list_renders_product_count(self):
        response = self.client.get(reverse("category_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rice")
        self.assertContains(response, "1")
        self.assertTemplateUsed(response, "restaurants/category_list.html")


class CartViewTests(TestCase):
    def setUp(self):
        self.category = MenuCategory.objects.create(name="Rice")
        self.menu_item = MenuItem.objects.create(
            category=self.category,
            name="Jollof Rice",
            description="Party-style jollof rice",
            price="2500.00",
            is_available=True,
        )

    def test_cart_starts_empty(self):
        response = self.client.get(reverse("cart_detail"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your cart is empty.")
        self.assertTemplateUsed(response, "restaurants/cart_detail.html")

    def test_add_item_to_cart(self):
        response = self.client.post(
            reverse("cart_add", args=[self.menu_item.pk]),
            {"quantity": "2", "next": reverse("cart_detail")},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jollof Rice")
        self.assertContains(response, "NGN 5000.00")
        self.assertEqual(
            self.client.session["cart"][str(self.menu_item.pk)],
            2,
        )

    def test_update_cart_quantity(self):
        session = self.client.session
        session["cart"] = {str(self.menu_item.pk): 1}
        session.save()

        response = self.client.post(
            reverse("cart_update", args=[self.menu_item.pk]),
            {"quantity": "3"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "NGN 7500.00")
        self.assertEqual(
            self.client.session["cart"][str(self.menu_item.pk)],
            3,
        )

    def test_remove_item_from_cart(self):
        session = self.client.session
        session["cart"] = {str(self.menu_item.pk): 1}
        session.save()

        response = self.client.post(
            reverse("cart_remove", args=[self.menu_item.pk]),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your cart is empty.")
        self.assertNotIn(str(self.menu_item.pk), self.client.session["cart"])

    def test_unavailable_item_cannot_be_added_to_cart(self):
        unavailable_item = MenuItem.objects.create(
            category=self.category,
            name="Sold Out Rice",
            price="3000.00",
            is_available=False,
        )

        response = self.client.post(
            reverse("cart_add", args=[unavailable_item.pk]),
            {"quantity": "1", "next": reverse("cart_detail")},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "currently unavailable")
        self.assertNotIn(
            str(unavailable_item.pk),
            self.client.session.get("cart", {}),
        )


class SitePageTests(TestCase):
    def test_home_renders_template(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HappyMeal Restaurant")
        self.assertTemplateUsed(response, "restaurants/home.html")

    def test_about_renders_template(self):
        response = self.client.get(reverse("about"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About HappyMeal Restaurant")
        self.assertTemplateUsed(response, "restaurants/about.html")

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
    def test_custom_404_renders_template(self):
        response = self.client.get("/missing-page/")

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Page Not Found", status_code=404)
        self.assertTemplateUsed(response, "restaurants/404.html")
