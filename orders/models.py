from django.db import models
from django.contrib.auth.models import User
import uuid

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=6)
    uuid = models.UUIDField(unique=True, editable=False)
    status = models.CharField(max_length=50)  # e.g., 'pending', 'completed', 'failed'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=50)  # e.g., 'payment', 'payout'
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)  # e.g., 'success', 'pending', 'failed'
    timestamp = models.DateTimeField(auto_now_add=True)


class BookedRate(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=6)
    tracking_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=20, default='booked')  # e.g., 'booked', 'expired'
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)