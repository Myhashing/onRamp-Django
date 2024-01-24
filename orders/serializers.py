from django.contrib.auth.models import User
from rest_framework import serializers

from customer.models import UserProfile, CustomerProfile, BirthCertificate


class OrderInputSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=100, decimal_places=0)


class RateAcceptanceSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=True)
    mobile = serializers.CharField(required=True, max_length=15)


class UserRegistrationSerializer(serializers.ModelSerializer):
    national_code = serializers.CharField(write_only=True)
    emergency_mobile = serializers.CharField(write_only=True, required=False)
    national_card_serial = serializers.CharField(write_only=True)
    birthdate = serializers.CharField(write_only=True)  # Persian birthdate

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name',
                  'national_code', 'emergency_mobile', 'national_card_serial', 'birthdate']
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'required': False}}

    def create(self, validated_data):
        # Extract and pop optional fields if they exist
        email = validated_data.pop('email', None)
        emergency_mobile = validated_data.pop('emergency_mobile', None)
        birthdate = validated_data.pop('birthdate')
        national_card_serial = validated_data.pop('national_card_serial')

        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, is_customer=True)
        customer_profile = CustomerProfile.objects.create(user=user, national_code=validated_data.get('national_code'), emergency_mobile=emergency_mobile)
        BirthCertificate.objects.create(customer=customer_profile, national_card_serial=national_card_serial, birthdate=birthdate)

        return user


