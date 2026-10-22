from django.core.validators import FileExtensionValidator
from django.db import models


class Profile(models.Model):
    """The site owner's details. Only the first profile is used."""

    name = models.CharField(max_length=100)
    headline = models.CharField(max_length=200, blank=True, help_text="One line under your name, e.g. 'Computer Science graduate'.")
    intro = models.TextField(blank=True, help_text="Shown on the home page.")
    summary = models.TextField(blank=True, help_text="Professional summary shown on the CV page.")
    hobbies = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    photo = models.ImageField(upload_to="profile/", blank=True)
    cv_file = models.FileField(
        "CV (PDF)",
        upload_to="cv/",
        blank=True,
        validators=[FileExtensionValidator(["pdf"])],
        help_text="The PDF exported from Overleaf. It is shown on the CV page and can be downloaded. "
        "Upload a new file to replace it.",
    )

    def __str__(self):
        return self.name


class Experience(models.Model):
    role = models.CharField(max_length=150)
    organisation = models.CharField(max_length=150)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave empty if current.")
    description = models.TextField(blank=True, help_text="One bullet point per line.")

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.role} at {self.organisation}"

    def bullet_points(self):
        return [line.strip("•- ").strip() for line in self.description.splitlines() if line.strip()]


class Education(models.Model):
    qualification = models.CharField(max_length=150)
    subject = models.CharField(max_length=150, blank=True)
    institution = models.CharField(max_length=150)
    location = models.CharField(max_length=100, blank=True)
    start_year = models.PositiveSmallIntegerField(null=True, blank=True)
    end_year = models.PositiveSmallIntegerField(null=True, blank=True)
    grade = models.CharField(max_length=100, blank=True, help_text="e.g. Merit, Upper Second Class Honours")
    details = models.TextField(blank=True, help_text="e.g. main courses.")

    class Meta:
        ordering = ["-end_year", "-start_year"]
        verbose_name_plural = "education"

    def __str__(self):
        return f"{self.qualification}, {self.institution}"


class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True, help_text="Skills are grouped by this, e.g. 'Programming languages'.")
    order = models.PositiveSmallIntegerField(default=0, help_text="Lower numbers come first; a category's position follows its first skill.")

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
