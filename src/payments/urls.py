from django.urls import path
from payments.views import (
    PaymentInitiateView,
    PaymentConfirmView,
    SavedPaymentMethodListView,
    SavedPaymentMethodDetailView
)

urlpatterns = [
    # URL para iniciar un nuevo pago
    path('initiate/', PaymentInitiateView.as_view(), name='payment-initiate'),
    
    # URL para la confirmación de pagos (ej. webhooks de pasarela)
    path('confirm/', PaymentConfirmView.as_view(), name='payment-confirm'),
    
    # URL para listar los métodos de pago guardados de un usuario
    # Requiere el user_id para filtrar
    path('saved_methods/<str:user_id>/', SavedPaymentMethodListView.as_view(), name='saved-payment-method-list'),
    
    # URL para eliminar un método de pago guardado por su ID
    path('saved_methods/<uuid:method_id>/', SavedPaymentMethodDetailView.as_view(), name='saved-payment-method-detail'),
]
