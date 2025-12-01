from django.urls import path
from .views import InitiatePaymentView, PaymentCallbackView, PaymentSuccessView, PaymentFailedView, PaymentErrorView

app_name = 'checkout'  # Namespace for checkout URLs

urlpatterns = [
    # Entry aliases
    path('', InitiatePaymentView.as_view(), name='home'),
    path('pay/', InitiatePaymentView.as_view(), name='pay'),
    path('initiate/', InitiatePaymentView.as_view(), name='initiate_payment'),

    # Callback routes (alias included)
    path('callback/<int:attempt_id>/', PaymentCallbackView.as_view(), name='payment_callback'),
    path('pay/callback/<int:attempt_id>/', PaymentCallbackView.as_view(), name='payment_callback_alias'),

    # Result screens (aliases included)
    path('success/<int:attempt_id>/', PaymentSuccessView.as_view(), name='payment_success'),
    path('pay/success/<int:attempt_id>/', PaymentSuccessView.as_view(), name='payment_success_alias'),
    path('failed/<int:attempt_id>/', PaymentFailedView.as_view(), name='payment_failed'),
    path('pay/failed/<int:attempt_id>/', PaymentFailedView.as_view(), name='payment_failed_alias'),

    # Error screen
    path('error/', PaymentErrorView.as_view(), name='payment_error'),
    path('pay/error/', PaymentErrorView.as_view(), name='payment_error_alias'),
]
