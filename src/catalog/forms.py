from django import forms
from .models import Category

class ProductFilterForm(forms.Form):
    """
    Formulario para filtrar productos por categoría y término de búsqueda.
    """
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Todas las categorías",
        required=False,
        label="Categoría"
    )
    search_term = forms.CharField(
        max_length=100,
        required=False,
        label="Buscar",
        widget=forms.TextInput(attrs={'placeholder': 'Buscar productos...'})
    )
    page = forms.IntegerField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['search_term'].widget.attrs.update({'class': 'form-control'})
