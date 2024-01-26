from django.contrib.auth.models import User
from rest_framework import serializers

from customer.models import UserProfile, CustomerProfile, BirthCertificate


class OrderInputSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=100, decimal_places=0)


class RateAcceptanceSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=True)
    mobile = serializers.CharField(required=True, max_length=15)


class UserRegistrationSerializer(serializers.ModelSerializer):

    mobile = serializers.CharField(required=False)
    national_code = serializers.CharField(write_only=True, required=True)
    emergency_mobile = serializers.CharField(write_only=True, required=False)
    national_card_serial = serializers.CharField(write_only=True)
    birthdate = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'email', 'first_name', 'last_name',
                  'national_code', 'emergency_mobile', 'national_card_serial', 'birthdate', 'mobile']
        # 'mobile' is added to the list of fields
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'required': False}}

    def create(self, validated_data):
        # Extract CustomerProfile and BirthCertificate data
        mobile = validated_data.get('mobile', 'Default value')

        customer_data = {
            'national_code': validated_data.pop('national_code'),
            'emergency_mobile': validated_data.pop('emergency_mobile', None),
            'mobile': mobile
        }
        birthdate = validated_data.pop('birthdate')
        national_card_serial = validated_data.pop('national_card_serial')

        # Create or get the User using national_code as username
        user, created = User.objects.get_or_create(
            username=customer_data['national_code'],
            defaults={'first_name': validated_data.get('first_name', ''),
                      'last_name': validated_data.get('last_name', ''),
                      'email': validated_data.get('email', '')}
        )

        if created:
            user.set_password(validated_data.get('password'))
            user.save()

            # Create CustomerProfile and BirthCertificate
            customer_profile = CustomerProfile.objects.create(user=user, **customer_data)
            BirthCertificate.objects.create(customer=customer_profile,
                                            national_card_serial=national_card_serial,
                                            birthdate=birthdate)

            # Set user as a customer in UserProfile
            user_profile = user.userprofile
            user_profile.is_customer = True
            user_profile.save()

        return user


class ExtendedRateAcceptanceSerializer(serializers.Serializer):
    # Fields from RateAcceptanceSerializer
    uuid = serializers.UUIDField(required=True)
    mobile = serializers.CharField(required=True, max_length=15)

    # Additional fields for user registration
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False, max_length=30)
    last_name = serializers.CharField(required=False, max_length=150)
    national_code = serializers.CharField(required=True)  # National code is required for new users
    emergency_mobile = serializers.CharField(required=False)
    national_card_serial = serializers.CharField(required=False)
    birthdate = serializers.CharField(required=False)

    # Validations and additional methods as needed
