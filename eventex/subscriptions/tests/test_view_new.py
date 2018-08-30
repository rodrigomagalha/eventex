
from django.core import mail
from django.shortcuts import resolve_url as r
from django .test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionsNewGet(TestCase):
    def setUp(self):
        self.response = self.client.get(r('subscriptions:new'))

    def test_get(self):
        """GET  / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """"Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1)
                )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """"Html must contain csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_hast_form(self):
        """"Context must have subscription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscriptionsNewPostValid(TestCase):
    def setUp(self):
        data = dict(name='Rodrigo Magalhães', cpf='997.893.160-03', email='rodrigo@magalhaes.com', phone='(88) 3520-8987')
        self.response = self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]

    def test_post(self):
        """"Valid POST should redirect to /inscricao/"""
        self.assertRedirects(self.response, r('subscriptions:detail', 1))

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionsNewInvalid(TestCase):
    def setUp(self):
        data = dict()
        self.response = self.client.post(r('subscriptions:new'), data)

    def test_post(self):
        """Invalid POST shuld not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())

