from django.urls import path

from . import views

urlpatterns = [
    path("api/menu-items/", views.MenuItemListCreateAPIView.as_view(), name="api_menu_item_list"),
    path(
        "api/menu-items/<int:pk>/",
        views.MenuItemDetailAPIView.as_view(),
        name="api_menu_item_detail",
    ),
    path(
        "api/menu-categories/",
        views.MenuCategoryListAPIView.as_view(),
        name="api_menu_category_list",
    ),
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("menu_list/", views.menu_list, name="menu_list"),
    path("menu/<int:pk>/", views.menu_detail, name="menu_detail"),
    path("menu-items/", views.menu_item_list, name="menu_item_list"),
    path("menu-items/add/", views.menu_item_create, name="menu_item_add"),
    path("menu-items/<int:pk>/", views.menu_item_detail, name="menu_item_detail"),
    path("menu-items/<int:pk>/edit/", views.menu_item_update, name="menu_item_edit"),
    path("menu-items/<int:pk>/delete/", views.menu_item_delete, name="menu_item_delete"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.category_create, name="category_add"),
    path("categories/<int:pk>/", views.category_detail, name="category_detail"),
    path("categories/<int:pk>/edit/", views.category_update, name="category_edit"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:pk>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:pk>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:pk>/", views.cart_remove, name="cart_remove"),
    path("about/", views.about, name="about"),
]
