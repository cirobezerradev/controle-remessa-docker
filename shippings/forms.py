from django import forms
from .models import Shipping, ShippingItem
    
class CadastroRemessa(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ['cliente', 'nfe', 'data_emissao',
                  'data_limite', 'volumes', 'peso']
