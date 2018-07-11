from django.core import mail
from django .test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """GET  / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """"Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """"Html must contain csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_hast_form(self):
        """"Context must have subscription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """"Form must have 4 fields."""
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Rodrigo Magalhães', cpf='997.893.160-03', email='rodrigo@magalhaes.com', phone='(88) 3520-8987')
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_post(self):
        """"Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.response.status_code)

    def test_send_sbscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        expect = 'Confirmacao de inscricao de: Rodrigo Magalhães'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expected = 'contato@eventex.com.br'

        self.assertEqual(expected, self.email.from_email)

    def test_subscripton_email_to(self):
        expected = ['rodrigo@magalhaes.com', 'contato@eventex.com.br']

        self.assertEqual(expected, self.email.to)

    def test_subscription_email_body(self):
        self.assertIn('Rodrigo Magalhães', self.email.body)
        self.assertIn('997.893.160-03', self.email.body)
        self.assertIn('rodrigo@magalhaes.com', self.email.body)
        self.assertIn('(88) 3520-8987', self.email.body)


class SubscribeInvalidPostTest(TestCase):
    def setUp(self):
        data = dict()
        self.response = self.client.post('/inscricao/', data)

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

class SubscribeSucessMessageTest(TestCase):
    def test_message(self):
        data = dict(name='Rodrigo Magalhães', cpf='997.893.160-03', email='rodrigo@magalhaes.com',
                    phone='(88) 3520-8987')

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')
