from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Rodrigo Magalhães',
            cpf='997.893.160-03',
            email='rodrigo@magalhaes.com',
            phone='(88) 3520-8987'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_cretate_at(self):
        """"Subscription must have an auto created_at attr."""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Rodrigo Magalhães', str(self.obj))

    def test_paid_default_to_false(self):
        """By default paid muist be false"""
        self.assertEqual(False, self.obj.paid)
