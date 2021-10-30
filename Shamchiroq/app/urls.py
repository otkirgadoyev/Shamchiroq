from django.urls import path

from . import views

urlpatterns = [
    path('audio/', views.Audiolist.as_view(), name='audio-list'),
    path('audios/<int:pk>/', views.AudioDetail.as_view(), name='audio-detail'),
    path('user-register/', views.UserRegisterSerializerView.as_view(), name='user-register'),
    path('user-verify/', views.UserVerifySerializerView.as_view(), name='user-verify'),
    path('price-send/', views.PriceSendSerializerView.as_view(), name='price-send'),
    path('card-number-send/', views.SendCardNumberSerializerView.as_view(), name='card_number-send'),
    path('payment-verify/', views.PaymentVerifySerializerView.as_view(), name='payment-verify'),
    path('change-phone-number/', views.SendChangePhoneNumberSerializerView.as_view(), name='change-phone-number')
]
