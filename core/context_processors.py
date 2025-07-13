def cart_processor(request):
    if not request.user.is_authenticated:
        return {'cart_count': 0}
        
    try:
        cart = request.session.get('cart', {})
        cart_count = sum(cart.values())
    except:
        cart_count = 0
        
    return {'cart_count': cart_count}
