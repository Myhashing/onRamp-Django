from django.contrib import admin

from customer.models import UserProfile, CustomerProfile, Address, BirthCertificate, Account, Document

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(CustomerProfile)
admin.site.register(Address)
admin.site.register(BirthCertificate)
admin.site.register(Account)
admin.site.register(Document)

