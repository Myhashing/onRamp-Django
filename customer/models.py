from django.conf import settings
from django.db import models

from django.db import models
from django.contrib.auth.models import User


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_code = models.CharField(max_length=10)
    emergency_mobile = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    kyc_verified = models.BooleanField(default=False)  # Add this line

    def __str__(self):
        return self.user.username


class Address(models.Model):
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20, default='000000000')


class BirthCertificate(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    birth_cert_number = models.CharField(max_length=20, null=True)
    national_card_serial = models.CharField(max_length=20)
    birthdate = models.CharField(max_length=10, default='1300-01-01')  # To store dates like '1366-01-01'


class Account(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    iban = models.CharField(max_length=34)  # IBANs can be up to 34 characters
    card_number = models.CharField(max_length=19)  # Card numbers can be up to 19 digits


class Document(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_customer = models.BooleanField(default=False)
