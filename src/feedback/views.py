from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from .forms import DeliveryRatingForm
from .services import RatingService
from .models import Order, DeliveryRating


class RateDeliveryView(View):
    """
    Vista para manejar la calificación de una entrega por parte del cliente.
    """

    template_name = 'feedback/rate_delivery.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        # Si ya fue calificado, no debería volver a mostrarse el formulario
        if DeliveryRating.objects.filter(order=order).exists():
            return redirect(
                reverse('feedback:rating_confirmation', kwargs={'order_id': order.id})
            )

        form = DeliveryRatingForm()
        return render(request, self.template_name, {'form': form, 'order': order})

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        # Omitir calificación
        if 'skip_rating' in request.POST:
            RatingService.mark_order_as_skipped(order.id)
            return redirect(
                reverse('feedback:rating_confirmation', kwargs={'order_id': order.id})
            )

        # Enviar calificación
        form = DeliveryRatingForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data['score']
            comment = form.cleaned_data.get('comment')

            RatingService.create_delivery_rating(order.id, score, comment)

            return redirect(
                reverse('feedback:rating_confirmation', kwargs={'order_id': order.id})
            )

        return render(request, self.template_name, {'form': form, 'order': order})


class RatingConfirmationView(View):
    """
    Confirmación de que el feedback fue procesado.
    """

    template_name = 'feedback/rating_confirmation.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        was_rated = DeliveryRating.objects.filter(order=order).exists()

        return render(
            request,
            self.template_name,
            {
                'order': order,
                'was_rated': was_rated
            }
        )
