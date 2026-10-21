from django.db import models
from django.urls import reverse


class VisibleProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)


class Project(models.Model):
    # Your own wording — imports from GitHub only fill these in when they're empty.
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    summary = models.CharField(max_length=300, blank=True, help_text="One or two sentences shown on the project card.")
    body = models.TextField(blank=True, help_text="Optional longer write-up. Blank lines start a new paragraph.")
    image = models.ImageField(upload_to="projects/", blank=True, help_text="Optional screenshot.")

    # Kept up to date by "Import from GitHub".
    repo_url = models.URLField(blank=True)
    homepage_url = models.URLField("live demo URL", blank=True)
    language = models.CharField(max_length=50, blank=True)
    topics = models.CharField(max_length=300, blank=True, help_text="Comma-separated tags.")
    stars = models.PositiveIntegerField(default=0)
    last_pushed_at = models.DateTimeField(null=True, blank=True)
    github_id = models.BigIntegerField(null=True, blank=True, unique=True, editable=False)

    # Your choices.
    is_visible = models.BooleanField("show on site", default=False)
    is_featured = models.BooleanField("feature on home page", default=False)
    order = models.PositiveSmallIntegerField(default=0, help_text="Lower numbers come first.")

    objects = models.Manager()
    visible = VisibleProjectManager()

    class Meta:
        ordering = ["order", "-last_pushed_at", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"slug": self.slug})

    def topic_list(self):
        return [topic.strip() for topic in self.topics.split(",") if topic.strip()]
