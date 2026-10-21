from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True, published_at__lte=timezone.now())


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text="Used in the post's URL.")
    summary = models.CharField(max_length=300, blank=True, help_text="Short teaser shown on the blog list.")
    body = models.TextField(help_text="Blank lines start a new paragraph.")
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedPostManager()

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})
