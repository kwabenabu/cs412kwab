from django.contrib import admin
from .models import Joke, Picture


@admin.register(Joke)
class JokeAdmin(admin.ModelAdmin):
    list_display = ["text", "contributor", "created"]
    list_filter = ["contributor", "created"]
    search_fields = ["text", "contributor"]


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ["image_url", "contributor", "created"]
    list_filter = ["contributor", "created"]
    search_fields = ["image_url", "contributor"]

