from django.urls import path
from .views import RateDeliveryView, RatingConfirmationView

app_name = 'feedback' # Nombre del namespace de la app

urlpatterns = [
    # URL para que el cliente califique una entrega específica
    path('rate/<uuid:order_id>/', RateDeliveryView.as_view(), name='rate_delivery'),
    # URL para la página de confirmación después de calificar o omitir
    path('confirmation/<uuid:order_id>/', RatingConfirmationView.as_view(), name='rating_confirmation'),
]
