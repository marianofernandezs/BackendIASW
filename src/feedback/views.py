from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from .forms import DeliveryRatingForm
from .services import RatingService
from .models import Order, DeliveryRating
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import DeliveryRatingForm, OrderCommentForm
from .services import RatingService, OrderCommentService
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib import messages
from django.urls import reverse_lazy





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

class OrderCommentCreateView(LoginRequiredMixin, FormView):
            template_name = 'feedback/comment_form.html'
            form_class = OrderCommentForm

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                order_id = self.kwargs.get('order_id')
                context['order'] = get_object_or_404(Order, id=order_id)
                return context

            def form_valid(self, form):
                order_id = self.kwargs.get('order_id')
                message = form.cleaned_data['message']
                user = self.request.user

                try:
                    OrderCommentService.create_comment(
                        order_id=order_id,
                        user=user,
                        message=message
                    )
                    messages.success(self.request, "Comentario enviado correctamente.")
                    return redirect(reverse_lazy('feedback:comment_success', kwargs={'order_id': order_id}))

                except (ObjectDoesNotExist, ValidationError) as e:
                    messages.error(self.request, str(e))
                    return self.form_invalid(form)

            def form_invalid(self, form):
                messages.error(self.request, "Corrige los errores del formulario.")
                return super().form_invalid(form)


def comment_success_view(request, order_id):
                order = get_object_or_404(Order, id=order_id)
                return render(request, 'feedback/comment_success.html', {'order': order})
