from django.db import models


class Message(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    liked_site = models.BooleanField("I like this site", default=False)
    message = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.created_at:%Y-%m-%d})"
