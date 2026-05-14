from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("menu_list/", views.menu_list, name="menu_list"),
    path("menu/<int:pk>/", views.menu_detail, name="menu_detail"),
    path("categories/", views.category_list, name="category_list"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:pk>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:pk>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:pk>/", views.cart_remove, name="cart_remove"),
    path("about/", views.about, name="about"),
]
