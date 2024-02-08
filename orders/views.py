from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from kyc.service import perform_kyc_verification
from payment.zarinpal import send_request
from rate.service import fetch_rate
from .models import BookedRate
from .serializers import OrderInputSerializer, UserRegistrationSerializer, \
    ExtendedRateAcceptanceSerializer
from .service import create_unpaid_order


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
    @swagger_auto_schema(request_body=ExtendedRateAcceptanceSerializer)
    def post(self, request, *args, **kwargs):
        serializer = ExtendedRateAcceptanceSerializer(data=request.data)
        if serializer.is_valid():
            uuid = serializer.validated_data['uuid']
            national_code = serializer.validated_data.get('national_code')
            # Check if national code exists and user exists
            user = User.objects.filter(username=national_code).first()
            if user:
                # Verify KYC status and proceed
                if user.customerprofile.kyc_verified or perform_kyc_verification(user):
                    order = create_unpaid_order(uuid, user)
                    return self.process_payment(order)
                else:
                    return Response({'error': 'KYC not verified.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # Handle user registration
                registration_serializer = UserRegistrationSerializer(data=serializer.validated_data)
                if registration_serializer.is_valid():
                    user = registration_serializer.save()
                    # Perform KYC and other verifications here
                    if perform_kyc_verification(user):
                        order = create_unpaid_order(uuid, user)
                        return self.process_payment(order)
                    else:
                        return Response({'error': 'KYC verification failed.'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response(registration_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def process_payment(self, order):
        try:
            booked_rate = BookedRate.objects.get(tracking_number=order.uuid)

            # Prepare payment details
            amount = booked_rate.amount
            description = f"Payment for Order ID: {order.id}"
            
            # Initiate payment process
            payment_response = send_request(amount, description)

            if payment_response.get('status'):
                # Redirect user to payment URL or process further
                payment_url = payment_response.get('url')
                return Response({'message': 'Proceed to payment.', 'payment_url': payment_url},
                                status=status.HTTP_200_OK)
            else:
                # Handle payment initiation failure
                return Response({'error': payment_response.get('error', 'Payment initiation failed.')},
                                status=status.HTTP_400_BAD_REQUEST)

        except BookedRate.DoesNotExist:
            return Response({'error': 'Invalid or expired rate.'}, status=status.HTTP_404_NOT_FOUND)


class UserRegistrationView(APIView):
    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Handle additional KYC data here
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
