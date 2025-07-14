from django.urls import path
from . import views, api

urlpatterns = [
    # API endpoints
    path('api/update-location/<int:order_id>/', api.update_location, name='update_location'),
    path('api/active-orders-location/', views.active_orders_location, name='active_orders_location'),
    
    # Main routes
    path('register/', views.register, name='register'),
    path('register/shopkeeper/', views.register_shopkeeper, name='register_shopkeeper'),
    path('register/customer/', views.register_customer, name='register_customer'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/profile/', views.customer_profile, name='customer_profile'),
    path('shopkeeper/dashboard/', views.shopkeeper_dashboard, name='shopkeeper_dashboard'),
    path('shopkeeper/profile/', views.edit_shop_profile, name='edit_shop_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('orders/', views.order_list, name='order_list'),
    path('order/update/<int:pk>/', views.update_order_status, name='update_order_status'),
    path('search/', views.search_products, name='search_products'),
    path('shops/<int:shopkeeper_id>/', views.shop_detail, name='shop_detail'),
    path('profile/', views.shopkeeper_profile, name='shopkeeper_profile'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/place-order/', views.place_order, name='place_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('shopkeeper/order-tracking/', views.order_tracking, name='order_tracking'),
    path('shop/<int:shop_id>/review/', views.review_shop, name='review_shop'),
    path('', views.index, name='index'),
]