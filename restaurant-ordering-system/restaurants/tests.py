from unittest.mock import patch

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .admin import MenuItemAdmin
from .models import MenuCategory, MenuItem

User = get_user_model()


class MenuViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password="StrongPass123!",
        )
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

    def test_menu_list_renders_items(self):
        response = self.client.get(reverse("menu_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jollof Rice")
        self.assertContains(response, "In Stock")
        self.assertContains(response, "12 available")
        self.assertContains(response, "Login to Order")
        self.assertTemplateUsed(response, "restaurants/menu_list.html")

    def test_menu_detail_renders_item_fields(self):
        response = self.client.get(reverse("menu_detail", args=[self.menu_item.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jollof Rice")
        self.assertContains(response, "2500.00")
        self.assertContains(response, "Rice")
        self.assertContains(response, "In Stock")
        self.assertContains(response, "12 available")
        self.assertTemplateUsed(response, "restaurants/menu_detail.html")

    def test_menu_detail_prompts_anonymous_users_to_login_before_cart(self):
        response = self.client.get(reverse("menu_detail", args=[self.menu_item.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login to Add to Cart")
        self.assertNotContains(response, reverse("cart_add", args=[self.menu_item.pk]))

    def test_menu_detail_has_add_to_cart_form_for_logged_in_users(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("menu_detail", args=[self.menu_item.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add to Cart")
        self.assertContains(response, reverse("cart_add", args=[self.menu_item.pk]))

    def test_menu_list_uses_uploaded_image_thumbnail(self):
        self.menu_item.image = "menu_items/jollof.jpg"
        self.menu_item.save(update_fields=["image"])

        response = self.client.get(reverse("menu_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'src="/media/menu_items/jollof.jpg"')

    def test_menu_detail_uses_uploaded_full_image(self):
        self.menu_item.image = "menu_items/jollof-detail.jpg"
        self.menu_item.save(update_fields=["image"])

        response = self.client.get(reverse("menu_detail", args=[self.menu_item.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'src="/media/menu_items/jollof-detail.jpg"')

    def test_category_list_renders_menu_item_count(self):
        response = self.client.get(reverse("category_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rice")
        self.assertContains(response, "1")
        self.assertTemplateUsed(response, "restaurants/category_list.html")


class AccountAuthTests(TestCase):
    def test_login_page_uses_custom_template(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertContains(response, "Create Account")
        self.assertTemplateUsed(response, "registration/login.html")

    def test_registration_creates_user_and_logs_them_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "password": "StrongPass123!",
                "password_confirm": "StrongPass123!",
            },
            follow=True,
        )

        user = User.objects.get(email="ada@example.com")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.first_name, "Ada Lovelace")
        self.assertEqual(user.username, "ada-lovelace")
        self.assertContains(response, "Your account was created successfully.")
        self.assertTrue(response.context["user"].is_authenticated)

    def test_registration_rejects_duplicate_email(self):
        User.objects.create_user(
            username="ada",
            email="ada@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("register"),
            {
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "password": "StrongPass123!",
                "password_confirm": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertContains(response, "An account with this email already exists.")

    def test_registration_requires_matching_password_confirmation(self):
        response = self.client.post(
            reverse("register"),
            {
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "password": "StrongPass123!",
                "password_confirm": "WrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email="ada@example.com").exists())
        self.assertContains(response, "Passwords do not match.")

    def test_login_accepts_email_address(self):
        User.objects.create_user(
            username="ada-lovelace",
            email="ada@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("login"),
            {
                "username": "ada@example.com",
                "password": "StrongPass123!",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertEqual(response.context["user"].username, "ada-lovelace")

    def test_logout_redirects_to_home(self):
        user = User.objects.create_user(
            username="ada",
            email="ada@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("home"))

    def test_navbar_shows_auth_links_for_logged_out_users(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, 'href="/accounts/login/"')
        self.assertContains(response, 'href="/accounts/register/"')
        self.assertNotContains(response, "Logout")

    def test_navbar_shows_username_and_logout_for_logged_in_users(self):
        user = User.objects.create_user(
            username="ada",
            email="ada@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("home"))

        self.assertContains(response, "Hi, ada")
        self.assertContains(response, 'action="/accounts/logout/"')
        self.assertContains(response, "Logout")
        self.assertNotContains(response, 'href="/accounts/login/"')

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_sends_email(self):
        User.objects.create_user(
            username="ada",
            email="ada@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("password_reset"),
            {"email": "ada@example.com"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password Reset Sent")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("HappyMeal password reset", mail.outbox[0].subject)


class DashboardTests(TestCase):
    def setUp(self):
        self.category = MenuCategory.objects.create(name="Rice")
        self.menu_item = MenuItem.objects.create(
            category=self.category,
            name="Jollof Rice",
            description="Party-style jollof rice",
            price="2500.00",
            stock=0,
            is_available=False,
        )
        self.customer_user = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password="StrongPass123!",
        )
        self.staff_user = User.objects.create_user(
            username="manager",
            email="manager@example.com",
            password="StrongPass123!",
            is_staff=True,
        )

    def test_dashboard_requires_login(self):
        url = reverse("dashboard")
        response = self.client.get(url)

        self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_dashboard_is_hidden_and_blocked_for_customer_users(self):
        self.client.force_login(self.customer_user)

        home_response = self.client.get(reverse("home"))
        self.assertNotContains(home_response, 'href="/dashboard/"')

        response = self.client.get(reverse("dashboard"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Only staff users can view the dashboard.")
        self.assertNotContains(response, "Staff dashboard")
        self.assertNotContains(response, 'href="/dashboard/"')

    def test_dashboard_renders_staff_role_and_user_breakdown(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Staff dashboard")
        self.assertContains(response, "You are signed in as Admin.")
        self.assertContains(response, "Customers")
        self.assertContains(response, "Admins")
        self.assertContains(response, "Jollof Rice")
        self.assertContains(response, 'href="/dashboard/"')
        self.assertTemplateUsed(response, "restaurants/dashboard.html")


class MenuItemCrudTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="chef",
            email="chef@example.com",
            password="StrongPass123!",
            is_staff=True,
        )
        self.client.force_login(self.staff_user)
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

    def test_menu_item_write_views_require_login(self):
        self.client.logout()
        protected_urls = [
            reverse("menu_item_add"),
            reverse("menu_item_edit", args=[self.menu_item.pk]),
            reverse("menu_item_delete", args=[self.menu_item.pk]),
        ]

        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_add_menu_item_form_renders(self):
        response = self.client.get(reverse("menu_item_add"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(reverse("menu_item_add"), "/menu-items/add/")
        self.assertContains(response, "Add Menu Item")
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertTemplateUsed(response, "restaurants/menu_item_form.html")

    def test_add_menu_item_creates_item_and_shows_success_message(self):
        response = self.client.post(
            reverse("menu_item_add"),
            {
                "category": self.category.pk,
                "name": "Grilled Turkey",
                "description": "Smoky turkey with pepper sauce",
                "price": "4500.00",
                "stock": "8",
                "is_available": "on",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        created_item = MenuItem.objects.get(name="Grilled Turkey")
        self.assertEqual(created_item.stock, 8)
        self.assertContains(response, "Grilled Turkey was created successfully.")

    def test_add_menu_item_validates_required_and_price_fields(self):
        response = self.client.post(
            reverse("menu_item_add"),
            {
                "category": "",
                "name": "",
                "description": "",
                "price": "0.00",
                "stock": "0",
                "is_available": "on",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(MenuItem.objects.filter(price="0.00").exists())
        self.assertContains(response, "This field is required.")
        self.assertContains(response, "Price must be at least 0.01.")
        self.assertContains(response, "Set stock above 0 or mark this menu item as unavailable.")

    def test_edit_menu_item_form_is_prefilled(self):
        response = self.client.get(reverse("menu_item_edit", args=[self.menu_item.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            reverse("menu_item_edit", args=[self.menu_item.pk]),
            f"/menu-items/{self.menu_item.pk}/edit/",
        )
        self.assertContains(response, "Edit Menu Item")
        self.assertContains(response, 'value="Jollof Rice"')
        self.assertContains(response, 'value="10"')
        self.assertContains(response, "Party-style jollof rice")
        self.assertTemplateUsed(response, "restaurants/menu_item_form.html")

    def test_edit_menu_item_saves_changes_and_shows_success_message(self):
        response = self.client.post(
            reverse("menu_item_edit", args=[self.menu_item.pk]),
            {
                "category": self.category.pk,
                "name": "Jollof Rice Deluxe",
                "description": "Updated party-style jollof rice",
                "price": "3000.00",
                "stock": "14",
                "is_available": "on",
            },
            follow=True,
        )

        self.menu_item.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.menu_item.name, "Jollof Rice Deluxe")
        self.assertEqual(str(self.menu_item.price), "3000.00")
        self.assertEqual(self.menu_item.stock, 14)
        self.assertContains(response, "Jollof Rice Deluxe was updated successfully.")

    def test_delete_menu_item_confirmation_does_not_delete_on_get(self):
        response = self.client.get(reverse("menu_item_delete", args=[self.menu_item.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            reverse("menu_item_delete", args=[self.menu_item.pk]),
            f"/menu-items/{self.menu_item.pk}/delete/",
        )
        self.assertTrue(MenuItem.objects.filter(pk=self.menu_item.pk).exists())
        self.assertContains(response, "Delete menu item?")
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertTemplateUsed(response, "restaurants/confirm_delete.html")

    def test_non_staff_user_cannot_manage_menu_items(self):
        user = User.objects.create_user(
            username="server",
            email="server@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)
        protected_urls = [
            reverse("menu_item_add"),
            reverse("menu_item_edit", args=[self.menu_item.pk]),
            reverse("menu_item_delete", args=[self.menu_item.pk]),
        ]

        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                self.assertContains(
                    response,
                    "Only staff users can add, edit, or delete menu content.",
                )

        response = self.client.post(
            reverse("menu_item_delete", args=[self.menu_item.pk]),
            follow=True,
        )
        self.assertContains(
            response,
            "Only staff users can add, edit, or delete menu content.",
        )
        self.assertTrue(MenuItem.objects.filter(pk=self.menu_item.pk).exists())

    def test_delete_menu_item_deletes_on_post_and_shows_success_message(self):
        response = self.client.post(
            reverse("menu_item_delete", args=[self.menu_item.pk]),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(MenuItem.objects.filter(pk=self.menu_item.pk).exists())
        self.assertContains(response, "Jollof Rice was deleted successfully.")

    def test_admin_action_marks_menu_items_out_of_stock(self):
        menu_item_admin = MenuItemAdmin(MenuItem, AdminSite())

        with patch.object(menu_item_admin, "message_user") as message_user:
            menu_item_admin.mark_as_out_of_stock(
                None,
                MenuItem.objects.filter(pk=self.menu_item.pk),
            )

        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.stock, 0)
        self.assertFalse(self.menu_item.is_available)
        message_user.assert_called_once()


class CategoryCrudTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="chef",
            email="chef@example.com",
            password="StrongPass123!",
            is_staff=True,
        )
        self.client.force_login(self.staff_user)
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

    def test_category_detail_renders_category_and_menu_items(self):
        response = self.client.get(reverse("category_detail", args=[self.category.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rice")
        self.assertContains(response, "Jollof Rice")
        self.assertTemplateUsed(response, "restaurants/category_detail.html")

    def test_category_write_views_require_login(self):
        self.client.logout()
        protected_urls = [
            reverse("category_add"),
            reverse("category_edit", args=[self.category.pk]),
            reverse("category_delete", args=[self.category.pk]),
        ]

        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_non_staff_user_cannot_manage_categories(self):
        user = User.objects.create_user(
            username="server",
            email="server@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)
        protected_urls = [
            reverse("category_add"),
            reverse("category_edit", args=[self.category.pk]),
            reverse("category_delete", args=[self.category.pk]),
        ]

        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                self.assertContains(
                    response,
                    "Only staff users can add, edit, or delete menu content.",
                )

        response = self.client.post(
            reverse("category_delete", args=[self.category.pk]),
            follow=True,
        )
        self.assertContains(
            response,
            "Only staff users can add, edit, or delete menu content.",
        )
        self.assertTrue(MenuCategory.objects.filter(pk=self.category.pk).exists())

    def test_add_category_form_renders(self):
        response = self.client.get(reverse("category_add"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add Category")
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertTemplateUsed(response, "restaurants/category_form.html")

    def test_add_category_creates_category_and_shows_success_message(self):
        response = self.client.post(
            reverse("category_add"),
            {
                "name": "Desserts",
                "description": "Sweet treats",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(MenuCategory.objects.filter(name="Desserts").exists())
        self.assertContains(response, "Desserts was created successfully.")

    def test_add_category_validates_required_name(self):
        response = self.client.post(
            reverse("category_add"),
            {
                "name": "",
                "description": "Missing name",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(MenuCategory.objects.filter(description="Missing name").exists())
        self.assertContains(response, "This field is required.")

    def test_edit_category_form_is_prefilled(self):
        response = self.client.get(reverse("category_edit", args=[self.category.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Category")
        self.assertContains(response, 'value="Rice"')
        self.assertContains(response, "Rice meals")
        self.assertTemplateUsed(response, "restaurants/category_form.html")

    def test_edit_category_saves_changes_and_shows_success_message(self):
        response = self.client.post(
            reverse("category_edit", args=[self.category.pk]),
            {
                "name": "Main Rice",
                "description": "Updated rice meals",
            },
            follow=True,
        )

        self.category.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.category.name, "Main Rice")
        self.assertEqual(self.category.description, "Updated rice meals")
        self.assertContains(response, "Main Rice was updated successfully.")

    def test_delete_category_confirmation_does_not_delete_on_get(self):
        response = self.client.get(reverse("category_delete", args=[self.category.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(MenuCategory.objects.filter(pk=self.category.pk).exists())
        self.assertContains(response, "Delete category?")
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertTemplateUsed(response, "restaurants/confirm_delete.html")

    def test_delete_category_deletes_on_post_and_shows_success_message(self):
        response = self.client.post(
            reverse("category_delete", args=[self.category.pk]),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(MenuCategory.objects.filter(pk=self.category.pk).exists())
        self.assertFalse(MenuItem.objects.filter(pk=self.menu_item.pk).exists())
        self.assertContains(response, "Rice was deleted successfully.")


class CartViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(self.user)
        self.category = MenuCategory.objects.create(name="Rice")
        self.menu_item = MenuItem.objects.create(
            category=self.category,
            name="Jollof Rice",
            description="Party-style jollof rice",
            price="2500.00",
            is_available=True,
        )

    def test_cart_views_require_login(self):
        self.client.logout()
        protected_requests = [
            ("get", reverse("cart_detail"), None),
            ("post", reverse("cart_add", args=[self.menu_item.pk]), {"quantity": "1"}),
            ("post", reverse("cart_update", args=[self.menu_item.pk]), {"quantity": "2"}),
            ("post", reverse("cart_remove", args=[self.menu_item.pk]), None),
        ]

        for method, url, data in protected_requests:
            with self.subTest(url=url):
                request_method = getattr(self.client, method)
                response = request_method(url, data or {})
                self.assertRedirects(response, f"{reverse('login')}?next={url}")

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

    def test_add_item_to_cart_is_capped_by_stock(self):
        self.menu_item.stock = 3
        self.menu_item.save(update_fields=["stock"])

        response = self.client.post(
            reverse("cart_add", args=[self.menu_item.pk]),
            {"quantity": "9", "next": reverse("cart_detail")},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "NGN 7500.00")
        self.assertEqual(
            self.client.session["cart"][str(self.menu_item.pk)],
            3,
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

    def test_out_of_stock_item_cannot_be_added_to_cart(self):
        out_of_stock_item = MenuItem.objects.create(
            category=self.category,
            name="Finished Rice",
            price="3000.00",
            stock=0,
            is_available=False,
        )

        response = self.client.post(
            reverse("cart_add", args=[out_of_stock_item.pk]),
            {"quantity": "1", "next": reverse("cart_detail")},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "currently unavailable")
        self.assertNotIn(
            str(out_of_stock_item.pk),
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
