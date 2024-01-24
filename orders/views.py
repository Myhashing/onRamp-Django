from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from customer.models import CustomerProfile
from rate.service import fetch_rate
from .models import BookedRate
from .serializers import OrderInputSerializer, RateAcceptanceSerializer, UserRegistrationSerializer


class GetRateView(APIView):
    @swagger_auto_schema(request_body=OrderInputSerializer)
    def post(self, request, *args, **kwargs):
        serializer = OrderInputSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            rate = fetch_rate(amount)  # Replace with actual rate fetching logic

            booked_rate = BookedRate.objects.create(amount=amount, rate=rate)
            return Response({
                'amount': amount,
                'rate': rate,
                'tracking_number': booked_rate.tracking_number,
                'status': booked_rate.status,
                'created_at': booked_rate.created_at,
                'updated_at': booked_rate.updated_at
            })
        return Response(serializer.errors, status=400)


class RateAcceptanceView(APIView):
    @swagger_auto_schema(request_body=RateAcceptanceSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RateAcceptanceSerializer(data=request.data)
        if serializer.is_valid():
            uuid = serializer.validated_data['uuid']
            mobile = serializer.validated_data['mobile']

            user, created = User.objects.get_or_create(username=mobile)
            if created:
                # Ask for registration and KYC details
                return Response({'message': 'Please complete registration and KYC.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Check KYC status
            try:
                if user.customerprofile.kyc_verified:
                    # Check the validity of booked rate and proceed
                    try:
                        booked_rate = BookedRate.objects.get(tracking_number=uuid)
                        # Proceed to payment
                        # ...
                    except BookedRate.DoesNotExist:
                        return Response({'error': 'Invalid or expired rate.'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({'message': 'Please complete your KYC.'}, status=status.HTTP_401_UNAUTHORIZED)
            except CustomerProfile.DoesNotExist:
                return Response({'error': 'Customer profile not found.'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'message': 'Rate accepted. Proceed to payment.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(APIView):
    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Handle additional KYC data here
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
