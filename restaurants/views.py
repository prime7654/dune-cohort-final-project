from django.http import HttpResponse


def home(request):
    return HttpResponse(
        "Welcome to HappyMeal Restaurant. Order fresh meals, explore our menu, "
        "and enjoy quick service from our restaurant ordering system."
    )


def menu_list(request):
    return HttpResponse(
        "HappyMeal Menu: Jollof rice, grilled chicken, veggie pasta, classic "
        "burgers, fresh salads, and chilled drinks are available today."
    )


def about(request):
    return HttpResponse(
        "About HappyMeal Restaurant: we prepare tasty, affordable meals and make "
        "ordering simple for customers, kitchen staff, and delivery teams."
    )


def custom_404(request, exception):
    return HttpResponse(
        "404 - Page not found. The HappyMeal page you requested does not exist; "
        "please return home or check the menu list.",
        status=404,
    )
