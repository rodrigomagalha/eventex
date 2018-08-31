from django import forms
from django.core.exceptions import ValidationError


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('CPF deve conter apenas números.', 'CPFONLYNUMB')
    if len(value) != 11:
        raise ValidationError('CPF deve conter 11 números.','CPF11DIGIT')


class SubscriptionForm(forms.Form):
    """Baby setps muito longo, como fazer mais curto"""
    name = forms.CharField(label='Nome')
    cpf = forms.CharField(label='CPF', validators=[validate_cpf])
    email = forms.EmailField(label='E-Mail')
    phone = forms.CharField(label='Telefone')

    def clean_name(self):
        name = self.cleaned_data['name']
        words = [w.capitalize() for w in name.split()]

        return ' '.join(words)
