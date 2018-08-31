from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(
            name='Rodrigo Magalhães',
            cpf='99789316003',
            email='rodrigo@magalhaes.com',
            phone='(88) 3520-8987'
        )
        self.response = self.client.get(r('subscriptions:detail',self.obj.pk))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_detail.html')

    def test_context(self):
        subscription = self.response.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        contents = (self.obj.name, self.obj.cpf, self.obj.email, self.obj.phone)

        for expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected)


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.response = self.client.get(r('subscriptions:detail',0))

    def test_not_found(self):
        self.assertEquals(404, self.response.status_code)
