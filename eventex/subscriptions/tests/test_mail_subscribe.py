from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Rodrigo Magalhães', cpf='99789316003', email='rodrigo@magalhaes.com', phone='(88) 3520-8987')
        self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de Inscrição de: Rodrigo Magalhães'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expected = 'contato@eventex.com.br'

        self.assertEqual(expected, self.email.from_email)

    def test_subscripton_email_to(self):
        expected = ['rodrigo@magalhaes.com', 'contato@eventex.com.br']

        self.assertEqual(expected, self.email.to)

    def test_subscription_email_body(self):

        contents = ('Rodrigo Magalhães', '99789316003', 'rodrigo@magalhaes.com', '(88) 3520-8987')

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
