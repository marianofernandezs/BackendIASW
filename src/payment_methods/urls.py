from django.urls import path
from payment_methods import views

app_name = 'payment_methods'

# URLs para las vistas tradicionales (HTML)
urlpatterns = [
    path('', views.PaymentMethodListView.as_view(), name='list'),
    path('<int:pk>/delete/', views.PaymentMethodDeleteView.as_view(), name='delete'),
    path('<int:pk>/set-default/', views.PaymentMethodSetDefaultView.as_view(), name='set_default'),
    # Nota: El guardado real del método de pago (POST) se manejará a través de la API
    # ya que requiere el token de una pasarela de pago y es parte de un flujo de checkout.
]

# URLs para la API de métodos de pago
urls_api = [
    path('save/', views.PaymentMethodSaveAPIView.as_view(), name='api_save'),
    path('list/', views.PaymentMethodListAPIView.as_view(), name='api_list'),
    path('<int:pk>/delete/', views.PaymentMethodDeleteAPIView.as_view(), name='api_delete'),
]
