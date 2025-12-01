from django import forms
from .models import DeliveryRating, OrderComment

class DeliveryRatingForm(forms.ModelForm):
    """
    Formulario para la calificación de una entrega por parte del cliente.
    Permite seleccionar una puntuación del 1 al 5 y añadir un comentario opcional.
    """
    class Meta:
        model = DeliveryRating
        fields = ['score', 'comment']
        widgets = {
            'score': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': '¿Algún comentario o sugerencia?'}),
        }
        labels = {
            'score': 'Tu puntuación (1 es muy insatisfecho, 5 es muy satisfecho)',
            'comment': 'Comentarios (opcional)',
        }

    def clean_score(self):
        """
        Valida que el score esté en el rango de 1 a 5.
        """
        score = self.cleaned_data.get('score')
        if not (1 <= score <= 5):
            raise forms.ValidationError("La puntuación debe ser entre 1 y 5.")
        return score

class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = OrderComment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Escribe tu comentario (máx 300 caract.)'
            }),
        }
        labels = {
            'message': 'Comentario'
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')

        if not message or not message.strip():
            raise forms.ValidationError("El comentario no puede estar vacío.")

        if len(message) > 300:
            raise forms.ValidationError("El comentario no puede superar los 300 caracteres.")

        return message.strip()
