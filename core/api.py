from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Order
import json

@csrf_exempt
@require_POST
def update_location(request, order_id):
    """Update customer location for order tracking"""
    try:
        data = json.loads(request.body)
        order = get_object_or_404(Order, id=order_id)
        
        # Update location
        order.last_location_lat = data.get('lat')
        order.last_location_lng = data.get('lng')
        order.last_location_update = timezone.now()
        
        # Update status if customer is very close (within 100 meters)
        if data.get('distance') is not None and float(data.get('distance')) < 0.1:
            order.status = 'Arrived'
            if not order.notification_sent:
                send_arrival_notification(order)
                order.notification_sent = True
        elif order.status == 'Pending':
            order.status = 'On Way'
        
        order.save()
        
        return JsonResponse({
            'status': 'success',
            'order_status': order.status
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def send_arrival_notification(order):
    """Send notification to shopkeeper when customer arrives"""
    # You'll need to implement this using your preferred notification service
    # For example, using Firebase Cloud Messaging (FCM) or a similar service
    try:
        from firebase_admin import messaging
        
        message = messaging.Message(
            notification=messaging.Notification(
                title='Customer Has Arrived',
                body=f'Customer for Order #{order.id} has arrived to pick up {order.product.name}'
            ),
            token=order.product.shopkeeper.fcm_token,  # You'll need to add this field to your Shopkeeper model
        )
        response = messaging.send(message)
        print('Successfully sent notification:', response)
    except Exception as e:
        print('Error sending notification:', str(e))
