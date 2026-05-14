from decimal import Decimal

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .models import MenuCategory, MenuItem

CART_SESSION_KEY = "cart"
MAX_CART_QUANTITY = 20


def _get_cart(request):
    return request.session.setdefault(CART_SESSION_KEY, {})


def _clean_quantity(value, default=1):
    try:
        quantity = int(value)
    except (TypeError, ValueError):
        quantity = default

    return max(1, min(quantity, MAX_CART_QUANTITY))


def _redirect_after_cart_action(request):
    next_url = request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
    ):
        return redirect(next_url)
    return redirect("cart_detail")


def home(request):
    return render(request, "restaurants/home.html")


def menu_list(request):
    menu_items = MenuItem.objects.select_related("category").all()
    return render(
        request,
        "restaurants/menu_list.html",
        {"menu_items": menu_items},
    )


def menu_detail(request, pk):
    menu_item = get_object_or_404(
        MenuItem.objects.select_related("category"),
        pk=pk,
    )
    return render(
        request,
        "restaurants/menu_detail.html",
        {"menu_item": menu_item},
    )


def category_list(request):
    categories = MenuCategory.objects.annotate(
        product_count=Count("menu_items"),
    )
    return render(
        request,
        "restaurants/category_list.html",
        {"categories": categories},
    )


def about(request):
    return render(request, "restaurants/about.html")


def cart_detail(request):
    cart = request.session.get(CART_SESSION_KEY, {})
    menu_items = MenuItem.objects.select_related("category").filter(
        pk__in=cart.keys(),
    )
    menu_items_by_id = {str(item.pk): item for item in menu_items}
    cart_items = []
    subtotal = Decimal("0.00")

    for item_id, quantity in cart.items():
        menu_item = menu_items_by_id.get(item_id)
        if not menu_item:
            continue

        quantity = int(quantity)
        line_total = menu_item.price * quantity
        subtotal += line_total
        cart_items.append(
            {
                "menu_item": menu_item,
                "quantity": quantity,
                "line_total": line_total,
            }
        )

    return render(
        request,
        "restaurants/cart_detail.html",
        {
            "cart_items": cart_items,
            "subtotal": subtotal,
        },
    )


def cart_add(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)

    if request.method != "POST":
        return redirect("menu_detail", pk=pk)

    if not menu_item.is_available:
        messages.warning(request, f"{menu_item.name} is currently unavailable.")
        return _redirect_after_cart_action(request)

    cart = _get_cart(request)
    item_key = str(menu_item.pk)
    quantity = _clean_quantity(request.POST.get("quantity"))
    current_quantity = int(cart.get(item_key, 0))
    cart[item_key] = min(current_quantity + quantity, MAX_CART_QUANTITY)
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True

    messages.success(request, f"{menu_item.name} was added to your cart.")
    return _redirect_after_cart_action(request)


def cart_update(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)

    if request.method != "POST":
        return redirect("cart_detail")

    cart = _get_cart(request)
    item_key = str(menu_item.pk)
    quantity = _clean_quantity(request.POST.get("quantity"))
    cart[item_key] = quantity
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True

    messages.success(request, f"{menu_item.name} quantity was updated.")
    return redirect("cart_detail")


def cart_remove(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)

    if request.method != "POST":
        return redirect("cart_detail")

    cart = _get_cart(request)
    cart.pop(str(menu_item.pk), None)
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True

    messages.info(request, f"{menu_item.name} was removed from your cart.")
    return redirect("cart_detail")


def custom_404(request, exception):
    return render(request, "restaurants/404.html", status=404)
