def cart_processor(request):
    if not request.user.is_authenticated:
        return {'cart_count': 0}
        
    try:
        cart = request.session.get('cart', {})
        cart_count = sum(cart.values())
    except:
        cart_count = 0
        
    return {'cart_count': cart_count}


from django.conf import settings


def maps_api_key(request):
    """Expose Google Maps API key to templates.

    Returns both uppercase and lowercase keys because some templates/views
    expect different variable names. Value is taken from environment (settings).
    """
    api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
    return {
        'GOOGLE_MAPS_API_KEY': api_key,
        'google_maps_api_key': api_key,
    }
