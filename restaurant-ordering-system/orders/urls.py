from django.urls import path

from . import views

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_history, name="order_history"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
    path(
        "dashboard/orders/<int:pk>/status/",
        views.order_status_update,
        name="order_status_update",
    ),
]
