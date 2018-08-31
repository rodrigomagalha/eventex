from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormValid(TestCase):
    def test_form_has_fields(self):
        """"Form must have 4 fields."""
        self.form = SubscriptionForm()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(self.form.fields))

    def test_cpf_is_digit(self):
        """CPF must only accept digits"""
        form = self.make_validated_form(cpf='ABCD9316003')
        self.assertFormErrorCode(form, 'cpf', 'CPFONLYNUMB')

    def test_cpf_has_11_digits(self):
        """"CPF must have 11 digits"""
        form = self.make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'CPF11DIGIT')

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        error_list = errors[field]
        exception = error_list[0]
        self.assertEqual(code, exception.code)

    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertListEqual([msg], errors_list)

    def make_validated_form(self, **kwargs):
        valid = dict(
                name='Rodrigo Magalhães',
                cpf='99789316003',
                email='rodrigo@magalhaes.com',
                phone='(88) 3520-8987')

        data = dict(valid, **kwargs)

        form = SubscriptionForm(data)
        form.is_valid()

        return form