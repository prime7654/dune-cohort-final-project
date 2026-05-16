from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from restaurants.models import MenuItem
from restaurants.views import CART_SESSION_KEY, _is_orderable, staff_required

from .forms import CheckoutForm, OrderStatusForm
from .models import Customer, Order, OrderItem


def _cart_items_from_session(request):
    cart = request.session.get(CART_SESSION_KEY, {})
    menu_items = MenuItem.objects.select_related("category").filter(pk__in=cart.keys())
    menu_items_by_id = {str(item.pk): item for item in menu_items}
    cart_items = []

    for item_id, quantity in cart.items():
        menu_item = menu_items_by_id.get(item_id)
        if not menu_item:
            continue
        cart_items.append(
            {
                "menu_item": menu_item,
                "quantity": int(quantity),
                "line_total": menu_item.price * int(quantity),
            }
        )

    return cart_items


@login_required
def checkout(request):
    cart_items = _cart_items_from_session(request)
    if not cart_items:
        messages.info(request, "Your cart is empty.")
        return redirect("cart_detail")

    if request.method == "POST":
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            with transaction.atomic():
                locked_items = MenuItem.objects.select_for_update().filter(
                    pk__in=[item["menu_item"].pk for item in cart_items],
                )
                locked_items_by_id = {item.pk: item for item in locked_items}

                for cart_item in cart_items:
                    menu_item = locked_items_by_id.get(cart_item["menu_item"].pk)
                    quantity = cart_item["quantity"]
                    if not menu_item or not _is_orderable(menu_item) or menu_item.stock < quantity:
                        messages.error(
                            request,
                            f"{cart_item['menu_item'].name} is no longer available in that quantity.",
                        )
                        return redirect("cart_detail")

                customer, _ = Customer.objects.get_or_create(
                    user=request.user,
                    defaults={
                        "full_name": form.cleaned_data["full_name"],
                        "phone_number": form.cleaned_data["phone_number"],
                        "email": form.cleaned_data["email"],
                        "address": form.cleaned_data["delivery_address"],
                    },
                )
                customer.full_name = form.cleaned_data["full_name"]
                customer.phone_number = form.cleaned_data["phone_number"]
                customer.email = form.cleaned_data["email"]
                customer.address = form.cleaned_data["delivery_address"]
                customer.save()

                order = Order.objects.create(
                    customer=customer,
                    delivery_address=form.cleaned_data["delivery_address"],
                    notes=form.cleaned_data["notes"],
                )

                for cart_item in cart_items:
                    menu_item = locked_items_by_id[cart_item["menu_item"].pk]
                    quantity = cart_item["quantity"]
                    OrderItem.objects.create(
                        order=order,
                        menu_item=menu_item,
                        quantity=quantity,
                        unit_price=menu_item.price,
                    )
                    menu_item.stock -= quantity
                    if menu_item.stock == 0:
                        menu_item.is_available = False
                    menu_item.save(update_fields=["stock", "is_available"])

            request.session[CART_SESSION_KEY] = {}
            request.session.modified = True
            messages.success(request, f"Order #{order.pk} was placed successfully.")
            return redirect("order_detail", pk=order.pk)
    else:
        form = CheckoutForm(user=request.user)

    subtotal = sum((item["line_total"] for item in cart_items), start=0)
    return render(
        request,
        "orders/checkout.html",
        {
            "cart_items": cart_items,
            "form": form,
            "subtotal": subtotal,
        },
    )


@login_required
def order_history(request):
    orders = (
        Order.objects.filter(customer__user=request.user)
        .select_related("customer")
        .prefetch_related("items__menu_item")
    )
    return render(request, "orders/order_history.html", {"orders": orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.select_related("customer").prefetch_related("items__menu_item"),
        pk=pk,
    )
    if not request.user.is_staff and order.customer.user_id != request.user.pk:
        messages.error(request, "You can only view your own orders.")
        return redirect("order_history")

    return render(request, "orders/order_detail.html", {"order": order})


@staff_required(message="Only staff users can update orders.")
def order_status_update(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method != "POST":
        return redirect("dashboard")

    form = OrderStatusForm(request.POST, instance=order)
    if form.is_valid():
        form.save()
        messages.success(request, f"Order #{order.pk} status was updated.")
    else:
        messages.error(request, "Choose a valid order status.")

    return redirect(request.POST.get("next") or "dashboard")
