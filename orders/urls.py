from django.urls import path
from .views import GetRateView, RateAcceptanceView, UserRegistrationView

urlpatterns = [
    path('get-rate/', GetRateView.as_view(), name='get-rate'),
    path('accept-rate/', RateAcceptanceView.as_view(), name='accept-rate'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),

]
