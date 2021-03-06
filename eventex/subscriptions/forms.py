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
    email = forms.EmailField(label='E-Mail', required=False)
    phone = forms.CharField(label='Telefone', required=False)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        words = [w.capitalize() for w in name.split()]

        return ' '.join(words)

    def clean(self):
        if not self.cleaned_data.get('email') and not self.cleaned_data.get('phone'):
            raise ValidationError('Informe seu e-mail ou telefone')
