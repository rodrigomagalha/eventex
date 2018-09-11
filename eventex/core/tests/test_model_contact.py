from django.core.exceptions import ValidationError
from django.test import TestCase

from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Rodrigo Magalhaes',
            slug='rodrigo-magalhaes',
            photo='http://placehold.it/300x300',
        )

    def test_email(self):
        contact = Contact.objects.create(speaker=self.speaker,kind=Contact.EMAIL,
                                         value='rmagalha@gmail.com'
        )
        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        contact = Contact.objects.create(speaker=self.speaker, kind=Contact.PHONE,
                                         value='4899999999')
        self.assertTrue(Contact.objects.exists())

    def test_choice(self):
        """Contact kind should be limited to E or P"""
        contact = Contact(speaker=self.speaker, kind='A', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker=self.speaker,kind=Contact.EMAIL,
                          value='rmagalha@gmail.com'
        )
        self.assertEqual('rmagalha@gmail.com', str(contact))


class ContactManagerTest(TestCase):
    def setUp(self):
        s = Speaker.objects.create(
            name='Rodrigo Magalhaes',
            slug='rodrigo-magalhaes',
            photo='http://placehold.it/300x300',
        )

        s.contact_set.create(kind=Contact.EMAIL, value='rmagalha@gmail.com')
        s.contact_set.create(kind=Contact.PHONE, value='4899999999')

    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ['rmagalha@gmail.com']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)

    def test_emails(self):
        qs = Contact.objects.phones()
        expected = ['4899999999']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)
