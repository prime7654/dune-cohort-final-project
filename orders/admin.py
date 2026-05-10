from django.contrib import admin

from .models import Customer, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone_number", "email", "created_at")
    search_fields = ("full_name", "phone_number", "email")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "total_price", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer__full_name", "customer__phone_number")
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "menu_item", "quantity", "unit_price")
    list_filter = ("menu_item",)
