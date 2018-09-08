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