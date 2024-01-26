from django.contrib import admin
from orders.models import Order, Transaction, BookedRate

# Register your models here.
admin.site.register(Order)
admin.site.register(Transaction)
admin.site.register(BookedRate)