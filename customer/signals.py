from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import CustomerProfile, UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_or_update_customer_profile(sender, instance, **kwargs):
    # Ensure the user profile exists
    user_profile, _ = UserProfile.objects.get_or_create(user=instance)
    # Check if the user is a customer
    if user_profile.is_customer:
        CustomerProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=UserProfile)
def save_user_profile(sender, instance, **kwargs):
    # Check if the save operation is already in progress to avoid recursion
    if not kwargs.get('raw', False):
        instance.save_base(raw=True)
