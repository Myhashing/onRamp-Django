from django.db import IntegrityError
from django.http import JsonResponse
from orders.models import BookedRate, Order
import uuid

def create_unpaid_order(tracking_uuid, user):
    try:
        # Fetch the booked rate using the provided uuid
        booked_rate = BookedRate.objects.get(tracking_number=tracking_uuid)

        # Create a new order instance with a new UUID
        order = Order(
            uuid=uuid.uuid4(),  # Ensure this generates a unique UUID for each order
            user=user,
            amount=booked_rate.amount,
            rate=booked_rate.rate,
            status='unpaid'
        )

        # Save the order to the database
        order.save()

        return order
    except BookedRate.DoesNotExist:
        return JsonResponse({'error': 'Booked rate not found.'}, status=404)
    except IntegrityError as e:
        return JsonResponse({'error': 'An order with this UUID already exists.'}, status=400)

