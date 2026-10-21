from django.test import TestCase
from django.urls import reverse

from .models import Message


class ContactFormTests(TestCase):
    url = reverse("contact")

    def test_valid_message_is_saved_and_redirects(self):
        response = self.client.post(self.url, {"name": "Ann", "message": "Nice site!"}, follow=True)
        self.assertRedirects(response, self.url)
        self.assertContains(response, "Thanks for your message")
        self.assertEqual(Message.objects.count(), 1)

    def test_invalid_message_shows_errors_and_is_not_saved(self):
        response = self.client.post(self.url, {"name": "", "message": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        self.assertEqual(Message.objects.count(), 0)

    def test_honeypot_blocks_bots(self):
        self.client.post(self.url, {"name": "Bot", "message": "spam", "website": "http://spam.example"})
        self.assertEqual(Message.objects.count(), 0)
