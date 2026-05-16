from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from restaurants.models import MenuCategory, MenuItem

from .models import Customer, Order, OrderItem

User = get_user_model()


class CheckoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password="StrongPass123!",
        )
        self.category = MenuCategory.objects.create(name="Rice")
        self.menu_item = MenuItem.objects.create(
            category=self.category,
            name="Jollof Rice",
            description="Party-style jollof rice",
            price="2500.00",
            stock=5,
            is_available=True,
        )

    def _add_item_to_cart(self, quantity=2):
        session = self.client.session
        session["cart"] = {str(self.menu_item.pk): quantity}
        session.save()

    def test_checkout_requires_login(self):
        self._add_item_to_cart()

        response = self.client.get(reverse("checkout"))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('checkout')}")

    def test_checkout_creates_order_and_connects_customer_to_user(self):
        self.client.force_login(self.user)
        self._add_item_to_cart(quantity=2)

        response = self.client.post(
            reverse("checkout"),
            {
                "full_name": "Customer One",
                "phone_number": "08012345678",
                "email": "customer@example.com",
                "delivery_address": "12 Lagos Street",
                "notes": "No pepper",
            },
            follow=True,
        )

        order = Order.objects.get()
        customer = Customer.objects.get()
        order_item = OrderItem.objects.get(order=order)
        self.menu_item.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(customer.user, self.user)
        self.assertEqual(order.customer, customer)
        self.assertEqual(order.delivery_address, "12 Lagos Street")
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(str(order_item.unit_price), "2500.00")
        self.assertEqual(self.menu_item.stock, 3)
        self.assertEqual(self.client.session["cart"], {})
        self.assertContains(response, f"Order #{order.pk} was placed successfully.")
        self.assertTemplateUsed(response, "orders/order_detail.html")

    def test_checkout_rejects_unavailable_cart_item(self):
        self.client.force_login(self.user)
        self.menu_item.stock = 0
        self.menu_item.is_available = False
        self.menu_item.save(update_fields=["stock", "is_available"])
        self._add_item_to_cart(quantity=1)

        response = self.client.post(
            reverse("checkout"),
            {
                "full_name": "Customer One",
                "phone_number": "08012345678",
                "email": "customer@example.com",
                "delivery_address": "12 Lagos Street",
                "notes": "",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Order.objects.exists())
        self.assertContains(response, "is no longer available in that quantity.")


class OrderHistoryTests(TestCase):
    def setUp(self):
        self.category = MenuCategory.objects.create(name="Rice")
        self.menu_item = MenuItem.objects.create(
            category=self.category,
            name="Jollof Rice",
            price="2500.00",
            stock=5,
            is_available=True,
        )
        self.user = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="StrongPass123!",
        )
        self.staff_user = User.objects.create_user(
            username="manager",
            email="manager@example.com",
            password="StrongPass123!",
            is_staff=True,
        )
        self.customer = Customer.objects.create(
            user=self.user,
            full_name="Customer One",
            phone_number="08012345678",
            email="customer@example.com",
            address="12 Lagos Street",
        )
        self.other_customer = Customer.objects.create(
            user=self.other_user,
            full_name="Customer Two",
            phone_number="08087654321",
            email="other@example.com",
            address="4 Abuja Street",
        )
        self.order = Order.objects.create(
            customer=self.customer,
            delivery_address="12 Lagos Street",
        )
        OrderItem.objects.create(order=self.order, menu_item=self.menu_item, quantity=1)
        self.other_order = Order.objects.create(
            customer=self.other_customer,
            delivery_address="4 Abuja Street",
        )
        OrderItem.objects.create(order=self.other_order, menu_item=self.menu_item, quantity=1)

    def test_order_history_shows_only_current_user_orders(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("order_history"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Order #{self.order.pk}")
        self.assertNotContains(response, f"Order #{self.other_order.pk}")
        self.assertTemplateUsed(response, "orders/order_history.html")

    def test_order_detail_blocks_other_customers_orders(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("order_detail", args=[self.other_order.pk]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You can only view your own orders.")
        self.assertTemplateUsed(response, "orders/order_history.html")

    def test_staff_can_view_customer_order_and_update_status(self):
        self.client.force_login(self.staff_user)

        detail_response = self.client.get(reverse("order_detail", args=[self.order.pk]))
        update_response = self.client.post(
            reverse("order_status_update", args=[self.order.pk]),
            {"status": Order.Status.READY, "next": reverse("dashboard")},
            follow=True,
        )

        self.order.refresh_from_db()
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Customer One")
        self.assertEqual(self.order.status, Order.Status.READY)
        self.assertContains(update_response, f"Order #{self.order.pk} status was updated.")

    def test_customer_cannot_update_order_status(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("order_status_update", args=[self.order.pk]),
            {"status": Order.Status.READY, "next": reverse("dashboard")},
            follow=True,
        )

        self.order.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.order.status, Order.Status.PENDING)
        self.assertContains(response, "Only staff users can update orders.")
