"""Forms for the mini_insta app.

Contains ModelForms for creating posts and updating profiles.
"""

# author Kwabena
# file forms.py
#description Forms for the mini_insta app
#django forms for creating and editing posts

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """ModelForm to create a Post with a caption."""
    class Meta:
        model = Post
        fields = ['caption']  


class UpdateProfileForm(forms.ModelForm):
    """ModelForm to update editable Profile fields."""
    class Meta:
        model = Profile
        # Exclude non-editable fields; allow editing display fields
        fields = ['display_name', 'profile_image_url', 'bio_text']


class CreateProfileForm(forms.ModelForm):
    """ModelForm to create a Profile without exposing the `user` field."""
    class Meta:
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']
