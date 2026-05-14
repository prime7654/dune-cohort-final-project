def cart_summary(request):
    cart = request.session.get("cart", {})
    cart_item_count = sum(int(quantity) for quantity in cart.values())

    return {"cart_item_count": cart_item_count}
