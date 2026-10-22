import shutil
import tempfile
from datetime import date

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
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

    def test_404_page_renders(self):
        response = self.client.get("/no-such-page/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Page not found", status_code=404)

    def test_navbar_links_are_relative(self):
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "pythonanywhere.com")
        self.assertContains(response, f'href="{reverse("cv")}"')


TEMP_MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class CvPdfTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)

    def test_uploaded_pdf_is_embedded_and_downloadable(self):
        pdf = SimpleUploadedFile("cv.pdf", b"%PDF-1.4 test", content_type="application/pdf")
        profile = Profile.objects.create(name="Jane", cv_file=pdf)
        response = self.client.get(reverse("cv"))
        self.assertContains(response, f'<iframe class="cv-pdf-frame" src="{profile.cv_file.url}#view=FitH"')
        self.assertContains(response, "Download CV (PDF)")

    def test_no_pdf_means_no_viewer(self):
        Profile.objects.create(name="Jane")
        self.assertNotContains(self.client.get(reverse("cv")), "cv-pdf-frame")

    def test_site_may_frame_its_own_pages(self):
        # DENY (Django's default) would stop the CV page from embedding the PDF.
        response = self.client.get(reverse("cv"))
        self.assertEqual(response.headers.get("X-Frame-Options"), "SAMEORIGIN")

    def test_only_pdfs_are_accepted(self):
        profile = Profile(name="Jane", cv_file=SimpleUploadedFile("cv.docx", b"not a pdf"))
        with self.assertRaises(ValidationError):
            profile.full_clean()
