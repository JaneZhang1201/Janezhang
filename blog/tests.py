from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Post


class PostViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.live = Post.objects.create(title="Live", slug="live", body="Hello\n\nWorld", is_published=True)
        cls.draft = Post.objects.create(title="Draft", slug="draft", body="Secret", is_published=False)
        cls.scheduled = Post.objects.create(
            title="Scheduled", slug="scheduled", body="Later", is_published=True,
            published_at=timezone.now() + timedelta(days=1),
        )

    def test_list_shows_only_published_posts(self):
        response = self.client.get(reverse("blog:list"))
        self.assertContains(response, "Live")
        self.assertNotContains(response, "Draft")
        self.assertNotContains(response, "Scheduled")

    def test_detail_renders_paragraphs(self):
        response = self.client.get(self.live.get_absolute_url())
        self.assertContains(response, "<p>Hello</p>", html=True)

    def test_unpublished_posts_return_404(self):
        for post in (self.draft, self.scheduled):
            self.assertEqual(self.client.get(post.get_absolute_url()).status_code, 404)

    def test_empty_blog_does_not_crash(self):
        Post.objects.all().delete()
        self.assertContains(self.client.get(reverse("blog:list")), "No posts yet")
