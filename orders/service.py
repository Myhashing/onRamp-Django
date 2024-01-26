from orders.models import BookedRate, Order


def create_unpaid_order( uuid, user):
    # Fetch the booked rate using the provided uuid
    booked_rate = BookedRate.objects.get(tracking_number=uuid)

    # Create a new order instance
    order = Order()  # Assuming you have an Order model
    order.user = user
    order.amount = booked_rate.amount
    order.rate = booked_rate.rate
    order.status = 'unpaid'  # Set the initial status to 'unpaid'

    # Save the order to the database
    order.save()

    return order
