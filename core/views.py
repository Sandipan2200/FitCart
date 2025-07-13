from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import (
    ShopkeeperRegistrationForm, 
    ProductForm, 
    OrderStatusForm, 
    ShopkeeperProfileForm,
    CustomerRegistrationForm,
    CustomerProfileForm
)
from .models import Shopkeeper, Product, Order, Customer
from math import radians, sin, cos, sqrt, atan2
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to add items to cart.')
        return redirect('login')
        
    # Check if user is a shopkeeper
    try:
        shopkeeper = Shopkeeper.objects.get(user=request.user)
        messages.error(request, 'Shopkeepers cannot add products to cart.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except Shopkeeper.DoesNotExist:
        pass

    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        
        # Check if product belongs to the same shop
        current_shop_id = request.session.get('current_shop_id')
        if current_shop_id is None:
            request.session['current_shop_id'] = product.shopkeeper.id
        elif current_shop_id != product.shopkeeper.id:
            messages.error(request, 'You can only add products from the same shop to your cart.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart
        messages.success(request, f'{product.name} added to cart.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('index')

def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    shop_location = None
    
    if cart:
        first_product_id = list(cart.keys())[0]
        product = Product.objects.get(id=first_product_id)
        shop_location = {
            'lat': product.shopkeeper.latitude,
            'lng': product.shopkeeper.longitude
        }
        
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'shop_location': shop_location
    }
    
    return render(request, 'core/cart.html', context)

def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        
        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            cart.pop(str(product_id), None)
            
        request.session['cart'] = cart
        messages.success(request, 'Cart updated successfully.')
        
    return redirect('view_cart')

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart.pop(str(product_id), None)
        request.session['cart'] = cart
        messages.success(request, 'Item removed from cart.')
        
    return redirect('view_cart')

def register(request):
    return render(request, 'core/register_choice.html')

from django.conf import settings

def register_shopkeeper(request):
    if request.method == 'POST':
        form = ShopkeeperRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Shopkeeper.objects.create(
                user=user,
                shop_name=form.cleaned_data['shop_name'],
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone'],
                latitude=form.cleaned_data['latitude'],
                longitude=form.cleaned_data['longitude']
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Registration failed. Please check the form.')
    else:
        form = ShopkeeperRegistrationForm()
    
    from django.conf import settings
    context = {
        'form': form,
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
        'debug': settings.DEBUG
    }
    if not context['GOOGLE_MAPS_API_KEY']:
        messages.warning(request, 'Google Maps API key is not configured. Location selection may not work properly.')
    return render(request, 'core/register_shopkeeper.html', context)

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(
                user=user,
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone'],
                latitude=form.cleaned_data['latitude'],
                longitude=form.cleaned_data['longitude']
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('index')
        else:
            messages.error(request, 'Registration failed. Please check the form.')
    else:
        form = CustomerRegistrationForm()
    
    from django.conf import settings
    return render(request, 'core/register_customer.html', {
        'form': form,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        try:
            shopkeeper = Shopkeeper.objects.get(user=request.user)
            return redirect('shopkeeper_dashboard')
        except Shopkeeper.DoesNotExist:
            try:
                customer = Customer.objects.get(user=request.user)
                return redirect('customer_dashboard')
            except Customer.DoesNotExist:
                messages.error(request, "No profile found.")
                return redirect('login')
    return redirect('login')

@login_required
def customer_dashboard(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found.")
        return redirect('login')
        
    orders = Order.objects.filter(customer=customer).order_by('-created_at')
    favorite_shops = customer.favorite_shops.all()
    
    context = {
        'customer': customer,
        'orders': orders,
        'favorite_shops': favorite_shops
    }
    return render(request, 'core/customer_dashboard.html', context)

@login_required
def shopkeeper_dashboard(request):
    try:
        shopkeeper = Shopkeeper.objects.get(user=request.user)
    except Shopkeeper.DoesNotExist:
        messages.error(request, "Shopkeeper profile not found.")
        return redirect('login')
    
    products = shopkeeper.products.all().order_by('-id')
    orders = Order.objects.filter(product__shopkeeper=shopkeeper).order_by('-created_at')
    
    context = {
        'shopkeeper': shopkeeper,
        'products': products,
        'orders': orders
    }
    return render(request, 'core/shopkeeper_dashboard.html', context)

@login_required
def edit_shop_profile(request):
    try:
        shopkeeper = Shopkeeper.objects.get(user=request.user)
    except Shopkeeper.DoesNotExist:
        messages.error(request, "Shopkeeper profile not found.")
        return redirect('login')
    
    if request.method == 'POST':
        form = ShopkeeperProfileForm(request.POST, request.FILES, instance=shopkeeper)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shop profile has been updated.')
            return redirect('shopkeeper_dashboard')
    else:
        form = ShopkeeperProfileForm(instance=shopkeeper)
    
    return render(request, 'core/shop_profile_form.html', {'form': form})

@login_required
def customer_profile(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('customer_dashboard')
    else:
        form = CustomerProfileForm(instance=customer)
    
    return render(request, 'core/customer_profile_form.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('customer_dashboard' if hasattr(request.user, 'customer') else 'shopkeeper_dashboard')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'core/change_password.html', {'form': form})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shopkeeper = request.user.shopkeeper
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failed to add product. Please check the form.')
    else:
        form = ProductForm()
    return render(request, 'core/product_form.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, shopkeeper=request.user.shopkeeper)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failed to update product. Please check the form.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'core/product_form.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, shopkeeper=request.user.shopkeeper)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('dashboard')
    return render(request, 'core/product_confirm_delete.html', {'product': product})

@login_required
def order_list(request):
    orders = Order.objects.filter(product__shopkeeper=request.user.shopkeeper)
    return render(request, 'core/order_list.html', {'orders': orders})

@login_required
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk, product__shopkeeper=request.user.shopkeeper)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order status updated!')
            return redirect('order_list')
        else:
            messages.error(request, 'Failed to update order status.')
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'core/order_status_form.html', {'form': form, 'order': order})

from django.conf import settings

def index(request):
    # Get all shops with products in stock
    shops = Shopkeeper.objects.filter(products__stock__gt=0).distinct()
    
    # Get user's location (if logged in and is a customer)
    user_location = None
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            user_location = {
                'lat': customer.latitude,
                'lng': customer.longitude
            }
        except Customer.DoesNotExist:
            pass

    # Prepare context with API key and debug info
    context = {
        'shops': shops,
        'user_location': user_location,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'debug': settings.DEBUG
    }

    # Warn if API key is not set
    if not settings.GOOGLE_MAPS_API_KEY:
        messages.warning(request, 'Google Maps API key is not configured. Map features may not work properly.')

    return render(request, 'core/index.html', context)

def search_products(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query, stock__gt=0)
        shops = Shopkeeper.objects.filter(products__in=products).distinct()
        return render(request, 'core/search_results.html', {
            'shops': shops,
            'query': query,
            'GOOGLE_MAPS_API_KEY': 'YOUR_GOOGLE_MAPS_API_KEY'  # Replace with your API key
        })
    return redirect('index')

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return round(distance, 2)  # Returns distance in kilometers

from django.conf import settings

def shop_detail(request, shopkeeper_id):
    from django.conf import settings
    shopkeeper = get_object_or_404(Shopkeeper, id=shopkeeper_id)
    products = Product.objects.filter(shopkeeper=shopkeeper, stock__gt=0)
    
    distance = None
    user_location = None
    
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            if customer.latitude and customer.longitude:
                if shopkeeper.latitude and shopkeeper.longitude:
                    distance = calculate_distance(
                        customer.latitude, customer.longitude,
                        shopkeeper.latitude, shopkeeper.longitude
                    )
                    user_location = {
                        'lat': float(customer.latitude),
                        'lng': float(customer.longitude)
                    }
        except Customer.DoesNotExist:
            pass
    
    context = {
        'shop': shopkeeper,
        'products': products,
        'distance': distance,
        'user_location': user_location,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'debug': settings.DEBUG
    }
    return render(request, 'core/shop_detail.html', context)

@login_required
def shopkeeper_profile(request):
    shopkeeper = get_object_or_404(Shopkeeper, user=request.user)
    if request.method == 'POST':
        form = ShopkeeperProfileForm(request.POST, instance=shopkeeper)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failed to update profile. Please check the form.')
    else:
        form = ShopkeeperProfileForm(instance=shopkeeper)
    return render(request, 'core/shopkeeper_profile.html', {
        'form': form,
        'shopkeeper': shopkeeper,
        'GOOGLE_MAPS_API_KEY': 'YOUR_GOOGLE_MAPS_API_KEY'  # Replace with your API key
    })