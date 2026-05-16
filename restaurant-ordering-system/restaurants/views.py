from decimal import Decimal
from functools import wraps
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from orders.models import Order

from .forms import MenuCategoryForm, MenuItemForm, RegistrationForm
from .models import MenuCategory, MenuItem

CART_SESSION_KEY = "cart"
MAX_CART_QUANTITY = 20


def staff_required(view_func=None, *, message="Only staff users can add, edit, or delete menu content."):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if not request.user.is_staff:
                messages.error(request, message)
                return redirect("menu_list")
            return func(request, *args, **kwargs)

        return wrapper

    if view_func is None:
        return decorator

    return decorator(view_func)


def _get_cart(request):
    return request.session.setdefault(CART_SESSION_KEY, {})


def _clean_quantity(value, default=1, maximum=MAX_CART_QUANTITY):
    try:
        quantity = int(value)
    except (TypeError, ValueError):
        quantity = default

    return max(1, min(quantity, maximum))


def _is_orderable(menu_item):
    return menu_item.is_available and menu_item.stock > 0


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


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account was created successfully.")
            return redirect("home")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})


@staff_required(message="Only staff users can view the dashboard.")
def dashboard(request):
    User = get_user_model()
    role_label = "Super Admin" if request.user.is_superuser else "Admin"
    total_menu_items = MenuItem.objects.count()
    available_menu_items = MenuItem.objects.filter(is_available=True, stock__gt=0).count()
    out_of_stock_items = MenuItem.objects.filter(stock=0).count()
    active_statuses = [
        Order.Status.PENDING,
        Order.Status.CONFIRMED,
        Order.Status.PREPARING,
        Order.Status.READY,
    ]

    context = {
        "role_label": role_label,
        "total_menu_items": total_menu_items,
        "available_menu_items": available_menu_items,
        "out_of_stock_items": out_of_stock_items,
        "total_categories": MenuCategory.objects.count(),
        "total_users": User.objects.count(),
        "admin_users": User.objects.filter(is_staff=True).count(),
        "customer_users": User.objects.filter(is_staff=False).count(),
        "superusers": User.objects.filter(is_superuser=True).count(),
        "recent_menu_items": MenuItem.objects.select_related("category").order_by("-created_at")[:5],
        "total_orders": Order.objects.count(),
        "active_orders": Order.objects.filter(status__in=active_statuses).count(),
        "delivered_orders": Order.objects.filter(status=Order.Status.DELIVERED).count(),
        "recent_orders": (
            Order.objects.select_related("customer")
            .prefetch_related("items__menu_item")
            .order_by("-created_at")[:8]
        ),
        "order_status_choices": Order.Status.choices,
    }
    return render(request, "restaurants/dashboard.html", context)


def menu_list(request):
    menu_items = MenuItem.objects.select_related("category").all()
    return render(
        request,
        "restaurants/menu_list.html",
        {"menu_items": menu_items},
    )


def menu_item_list(request):
    return menu_list(request)


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


def menu_item_detail(request, pk):
    return menu_detail(request, pk)


@staff_required
def menu_item_create(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save()
            messages.success(request, f"{menu_item.name} was created successfully.")
            return redirect("menu_item_detail", pk=menu_item.pk)
    else:
        form = MenuItemForm()

    return render(
        request,
        "restaurants/menu_item_form.html",
        {
            "form": form,
            "page_title": "Add Menu Item",
            "submit_label": "Create Menu Item",
        },
    )


@staff_required
def menu_item_update(request, pk):
    menu_item = get_object_or_404(MenuItem.objects.select_related("category"), pk=pk)

    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            menu_item = form.save()
            messages.success(request, f"{menu_item.name} was updated successfully.")
            return redirect("menu_item_detail", pk=menu_item.pk)
    else:
        form = MenuItemForm(instance=menu_item)

    return render(
        request,
        "restaurants/menu_item_form.html",
        {
            "form": form,
            "page_title": "Edit Menu Item",
            "menu_item": menu_item,
            "submit_label": "Save Changes",
        },
    )


@staff_required
def menu_item_delete(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)

    if request.method == "POST":
        menu_item_name = menu_item.name
        menu_item.delete()
        messages.success(request, f"{menu_item_name} was deleted successfully.")
        return redirect("menu_item_list")

    return render(
        request,
        "restaurants/confirm_delete.html",
        {
            "cancel_url": reverse("menu_item_detail", args=[menu_item.pk]),
            "object": menu_item,
            "object_type": "menu item",
        },
    )


def category_list(request):
    categories = MenuCategory.objects.annotate(
        menu_item_count=Count("menu_items"),
    )
    return render(
        request,
        "restaurants/category_list.html",
        {"categories": categories},
    )


def category_detail(request, pk):
    category = get_object_or_404(
        MenuCategory.objects.prefetch_related("menu_items"),
        pk=pk,
    )
    return render(
        request,
        "restaurants/category_detail.html",
        {"category": category},
    )


@staff_required
def category_create(request):
    if request.method == "POST":
        form = MenuCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"{category.name} was created successfully.")
            return redirect("category_detail", pk=category.pk)
    else:
        form = MenuCategoryForm()

    return render(
        request,
        "restaurants/category_form.html",
        {
            "form": form,
            "page_title": "Add Category",
            "submit_label": "Create Category",
        },
    )


@staff_required
def category_update(request, pk):
    category = get_object_or_404(MenuCategory, pk=pk)

    if request.method == "POST":
        form = MenuCategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"{category.name} was updated successfully.")
            return redirect("category_detail", pk=category.pk)
    else:
        form = MenuCategoryForm(instance=category)

    return render(
        request,
        "restaurants/category_form.html",
        {
            "category": category,
            "form": form,
            "page_title": "Edit Category",
            "submit_label": "Save Changes",
        },
    )


@staff_required
def category_delete(request, pk):
    category = get_object_or_404(MenuCategory, pk=pk)

    if request.method == "POST":
        category_name = category.name
        category.delete()
        messages.success(request, f"{category_name} was deleted successfully.")
        return redirect("category_list")

    return render(
        request,
        "restaurants/confirm_delete.html",
        {
            "cancel_url": reverse("category_detail", args=[category.pk]),
            "object": category,
            "object_type": "category",
        },
    )


def about(request):
    return render(request, "restaurants/about.html")


@login_required
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


@login_required
def cart_add(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)

    if request.method != "POST":
        return redirect("menu_detail", pk=pk)

    if not _is_orderable(menu_item):
        messages.warning(request, f"{menu_item.name} is currently unavailable.")
        return _redirect_after_cart_action(request)

    cart = _get_cart(request)
    item_key = str(menu_item.pk)
    quantity = _clean_quantity(
        request.POST.get("quantity"),
        maximum=min(MAX_CART_QUANTITY, menu_item.stock),
    )
    current_quantity = int(cart.get(item_key, 0))
    cart[item_key] = min(current_quantity + quantity, MAX_CART_QUANTITY, menu_item.stock)
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True

    messages.success(request, f"{menu_item.name} was added to your cart.")
    return _redirect_after_cart_action(request)


@login_required
def cart_update(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)

    if request.method != "POST":
        return redirect("cart_detail")

    cart = _get_cart(request)
    item_key = str(menu_item.pk)
    if not _is_orderable(menu_item):
        cart.pop(item_key, None)
        request.session[CART_SESSION_KEY] = cart
        request.session.modified = True
        messages.warning(request, f"{menu_item.name} is currently unavailable.")
        return redirect("cart_detail")

    quantity = _clean_quantity(
        request.POST.get("quantity"),
        maximum=min(MAX_CART_QUANTITY, menu_item.stock),
    )
    cart[item_key] = quantity
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True

    messages.success(request, f"{menu_item.name} quantity was updated.")
    return redirect("cart_detail")


@login_required
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
