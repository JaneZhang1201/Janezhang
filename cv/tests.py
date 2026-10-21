from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Experience, Profile, Skill


class PageTests(TestCase):
    def test_pages_work_with_an_empty_database(self):
        for name in ("home", "cv", "contact", "blog:list"):
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_cv_shows_profile_experience_and_skills(self):
        Profile.objects.create(name="Jane Zhang", email="jane@example.com")
        Experience.objects.create(
            role="Brand Ambassador", organisation="Acme", start_date=date(2020, 8, 1),
            description="First point\n- Second point",
        )
        Skill.objects.create(name="Python")
        response = self.client.get(reverse("cv"))
        self.assertContains(response, "Jane Zhang")
        self.assertContains(response, "<li>Second point</li>", html=True)
        self.assertContains(response, "Present")
        self.assertContains(response, "Python")

    def test_navbar_links_are_relative(self):
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "pythonanywhere.com")
        self.assertContains(response, f'href="{reverse("cv")}"')
