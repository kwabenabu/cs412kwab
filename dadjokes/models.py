from django.db import models


class Joke(models.Model):
    """A dad joke with text and contributor information."""
    text = models.TextField()
    contributor = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class Picture(models.Model):
    """A funny picture/GIF with URL and contributor information."""
    image_url = models.URLField()
    contributor = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_url

